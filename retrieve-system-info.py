import re
import xml.etree.ElementTree as ET

gpu_vendor_filter_list = ["NVIDIA Corporation"]
leftover_gpus = []

class DMIParse:
    """
    dmidecode information parsing object
    requires dmidecode output as input string
    """

    def __init__(self, dmidecode_output, default="n/a"):
        self.default = default
        self.data = self.dmidecode_parse(dmidecode_output)

    def get(self, type_id):
        if isinstance(type_id, str):
            for type_num, type_str in self.type2str.items():
                if type_str == type_id:
                    type_id = type_num

        result = list()
        for entry in self.data.values():
            if entry["DMIType"] == type_id:
                result.append(entry)
        return result

    def manufacturer(self):
        return self.get("System")[0].get("Manufacturer", self.default)

    def model(self):
        return self.get("System")[0].get("Product Name", self.default)

    def mainboard_name(self):
        return self.get("Baseboard")[0].get("Product Name", self.default)

    def model_report(self):
        manufacturer = self.manufacturer().strip()
        model = self.model().strip()
        if manufacturer != self.default or model != self.default:
            return manufacturer + " " + model

    def cpu_report(self):
        report = []
        for cpu in self.get("Processor"):
            if cpu.get("Core Enabled"):
                report.append(
                    f"{len(report)}: {cpu.get('Version').strip()}(Current Speed: {cpu.get('Current Speed').strip()})")
        report.append(f"Total Processors: {len(report)}")
        return "\n".join(report)

    def mainboard_report(self):
        manufacturer = self.get("Baseboard")[0].get(
            "Manufacturer", self.default).strip()
        model = self.get("Baseboard")[0].get(
            "Product Name", self.default).strip()
        if manufacturer != self.default or model != self.default:
            return manufacturer + " " + model

    def memory_report(self):
        report = []
        slots = self.get("Memory Device")
        for slot in slots:
            bank_locator = slot.get("Bank Locator")
            locator = slot.get("Locator")
            part_number = slot.get("Part Number")
            slot_info = f"Slot {len(report):02d}({locator.strip()}/{bank_locator.strip()}): "
            if part_number:
                slot_info += f"{slot.get('Manufacturer').strip()} {slot.get('Type').strip()} {slot.get('Part Number').strip()} {slot.get('Size').strip()}, {slot.get('Speed').strip()}({slot.get('Configured Memory Speed').strip()})"
            else:
                slot_info += "Not Installed"
            report.append(slot_info)
        return "\n".join(report)

    handle_re = re.compile(
        "^Handle\\s+(.+),\\s+DMI\\s+type\\s+(\\d+),\\s+(\\d+)\\s+bytes$")
    in_block_re = re.compile("^\\t\\t(.+)$")
    record_re = re.compile("\\t(.+):\\s+(.+)$")
    record2_re = re.compile("\\t(.+):$")

    type2str = {
        0: "BIOS",
        1: "System",
        2: "Baseboard",
        3: "Chassis",
        4: "Processor",
        5: "Memory Controller",
        6: "Memory Module",
        7: "Cache",
        8: "Port Connector",
        9: "System Slots",
        10: "On Board Devices",
        11: "OEM Strings",
        12: "System Configuration Options",
        13: "BIOS Language",
        14: "Group Associations",
        15: "System Event Log",
        16: "Physical Memory Array",
        17: "Memory Device",
        18: "32-bit Memory Error",
        19: "Memory Array Mapped Address",
        20: "Memory Device Mapped Address",
        21: "Built-in Pointing Device",
        22: "Portable Battery",
        23: "System Reset",
        24: "Hardware Security",
        25: "System Power Controls",
        26: "Voltage Probe",
        27: "Cooling Device",
        28: "Temperature Probe",
        29: "Electrical Current Probe",
        30: "Out-of-band Remote Access",
        31: "Boot Integrity Services",
        32: "System Boot",
        33: "64-bit Memory Error",
        34: "Management Device",
        35: "Management Device Component",
        36: "Management Device Threshold Data",
        37: "Memory Channel",
        38: "IPMI Device",
        39: "Power Supply",
        40: "Additional Information",
        41: "Onboard Devices Extended Information",
        42: "Management Controller Host Interface",
    }

    def dmidecode_parse(self, buffer):  # noqa: C901
        data = {}
        #  Each record is separated by double newlines
        split_output = buffer.split("\n\n")

        for record in split_output:
            record_element = record.splitlines()

            #  Entries with less than 3 lines are incomplete / inactive
            #  skip them
            if len(record_element) < 3:
                continue

            handle_data = self.handle_re.findall(record_element[0])

            if not handle_data:
                continue
            handle_data = handle_data[0]

            dmi_handle = handle_data[0]

            data[dmi_handle] = {}
            data[dmi_handle]["DMIType"] = int(handle_data[1])
            data[dmi_handle]["DMISize"] = int(handle_data[2])

            #  Okay, we know 2nd line == name
            data[dmi_handle]["DMIName"] = record_element[1]

            in_block_elemet = ""
            in_block_list = ""

            #  Loop over the rest of the record, gathering values
            for i in range(2, len(record_element), 1):
                if i >= len(record_element):
                    break
                #  Check whether we are inside a \t\t block
                if in_block_elemet != "":
                    in_block_data = self.in_block_re.findall(record_element[i])

                    if in_block_data:
                        if not in_block_list:
                            in_block_list = [in_block_data[0]]
                        else:
                            in_block_list.append(in_block_data[0])

                        data[dmi_handle][in_block_elemet] = in_block_list

                        continue
                    else:
                        # We are out of the \t\t block; reset it again, and let
                        # the parsing continue
                        in_block_elemet = ""

                record_data = self.record_re.findall(record_element[i])

                #  Is this the line containing handle identifier, type, size?
                if record_data:
                    data[dmi_handle][record_data[0][0]] = record_data[0][1]
                    continue

                #  Didn't findall regular entry, maybe an array of data?
                record_data2 = self.record2_re.findall(record_element[i])

                if record_data2:
                    #  This is an array of data - let the loop know we are
                    #  inside an array block
                    in_block_elemet = record_data2[0]
                    continue
        return data

    def size_to_gb(self, value):
        """Convert dmidecode memory size description to GB"""
        nb = re.search("[0-9]+", value)
        if nb:
            nb = int(re.search("[0-9]+", value).group())
        else:
            return 0
        if "MB" in value:
            return nb / 1024 if nb else 0
        elif "GB" in value:
            return nb
        else:
            return 0


with open("dmide.raw") as f:
    dmideData = DMIParse(f.read())

lshwData = ET.parse("lshw.xml")

print(dmideData.model_report())
print()
print(dmideData.cpu_report())
print()
print(dmideData.mainboard_report())
print()
print(dmideData.memory_report())
print()

gpus = lshwData.findall('node')
for idx, child in enumerate(gpus):
    vendor = child.find('vendor')
    product = child.find('product')
    clock = child.find('clock')
    if vendor.text not in gpu_vendor_filter_list:
        leftover_gpus.append(f"{vendor.text} {product.text} {clock.text} {clock.attrib.get('units')}")
        continue
    print(f"{idx}: {vendor.text} {product.text} {clock.text} {clock.attrib.get('units')}")
if len(gpus) > 0:
    print()

for entry in leftover_gpus:
    print(entry)
