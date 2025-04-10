# password="ThisIsActualMyPasswordEnjoy"

mkdir -p result

for host in `cat host`; do
    echo "$host\n" | tee "result/$host.log"

    if [ -z $password ]; then
        ssh $host -t "sudo -S dmidecode 2>/dev/null | tr -d '\r'" | tee dmide.raw
        ssh $host -t "sudo -S lshw -C display -xml 2>/dev/null | tr -d '\r'" | tee lshw.xml
    else
        sshpass -p $password ssh $host -t "sudo -S <<< $password dmidecode 2>/dev/null | tr -d '\r'" | tee dmide.raw
        sshpass -p $password ssh $host -t "sudo -S <<< $password lshw -C display -xml 2>/dev/null | tr -d '\r'" | tee lshw.xml
    fi

    python retrieve-system-info.py | tee -a "result/$host.log"
done

rm dmide.raw
rm lshw.xml