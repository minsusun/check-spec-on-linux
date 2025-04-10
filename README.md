# Check Spec On Linux

**Don't waste too much time on identifying specs on multiple linux machines!**

This scripts collects specs on multiple linux machines with only one line of script execution!

## Requirements

```text
# Host Machine
python 3.9
sshpass(if you don't want to type password, check below)

# Remote Machine
# (Most of linux distributions will have belows as default)
dmidecode
lshw
```

## Execution

```shell
./get-system-info.sh
```

## Execution without typing same passwords multiple times

If you have same passwords for all the hosts you want to inspect, you can use sshpass not to type passwords everytime you enter ssh session to gather info. **Unless, you have to type passwords 4 times per host since script will have two ssh sessions and sudo command per each host.** You can use sshpass by un-commenting variable `password` like below and set up your own password. Once you entered your password on script, you don't also have to type passwords for sudo commands. If you want details, check script `get-system-info.sh`.

```diff
--- ./get-system-info.sh
+++ ./get-system-info.sh

-# password="ThisIsActualMyPasswordEnjoy"
+password="ThisIsActualMyPasswordEnjoy"
```

## Result Example

```text
# hostname of inspection
hostname1

# Manufacturer, Model Name
ASUSTeK COMPUTER INC. ESC4000 G4

# Number: Model Name(Current Speed)
0: Intel(R) Xeon(R) Gold 6226R CPU @ 2.90GHz(Current Speed: 2900 MHz)
1: Intel(R) Xeon(R) Gold 6226R CPU @ 2.90GHz(Current Speed: 2900 MHz)
Total Processors: 2

# Manufacturer, Mainboard Model Name
ASUSTeK COMPUTER INC. Z11PG-D16 Series

# Slot #(Locator/Bank Locator): Manufacturer, Type, Product Code, Size, Speed, Configured Memory Speed
Slot 00(DIMM_A1/NODE 1): Samsung DDR4 M393A4K40CB2-CTD 32 GB, 2666 MT/s(2666 MT/s)
Slot 01(DIMM_A2/NODE 1): Not Installed
Slot 02(DIMM_B1/NODE 1): Not Installed
Slot 03(DIMM_C1/NODE 1): Not Installed
Slot 04(DIMM_D1/NODE 1): Samsung DDR4 M393A4K40CB2-CTD 32 GB, 2666 MT/s(2666 MT/s)
Slot 05(DIMM_D2/NODE 1): Not Installed
Slot 06(DIMM_E1/NODE 1): Not Installed
Slot 07(DIMM_F1/NODE 1): Not Installed
Slot 08(DIMM_G1/NODE 2): Samsung DDR4 M393A4K40CB2-CTD 32 GB, 2666 MT/s(2666 MT/s)
Slot 09(DIMM_G2/NODE 2): Not Installed
Slot 10(DIMM_H1/NODE 2): Not Installed
Slot 11(DIMM_J1/NODE 2): Not Installed
Slot 12(DIMM_K1/NODE 2): Samsung DDR4 M393A4K40CB2-CTD 32 GB, 2666 MT/s(2666 MT/s)
Slot 13(DIMM_K2/NODE 2): Not Installed
Slot 14(DIMM_L1/NODE 2): Not Installed
Slot 15(DIMM_M1/NODE 2): Not Installed

# Vendor, Product, Clock (Gpus from vendors which are on the list)
NVIDIA Corporation TU102 [TITAN RTX] 33000000 Hz
NVIDIA Corporation TU102 [TITAN RTX] 33000000 Hz
NVIDIA Corporation TU102 [TITAN RTX] 33000000 Hz
NVIDIA Corporation TU102 [TITAN RTX] 33000000 Hz

# Vendor, Product, Clock (Gpus from vendors which are not on the list)
ASPEED Technology, Inc. ASPEED Graphics Family 33000000 Hz
```
