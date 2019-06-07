```
#!/bin/bash
#获取当前ip
oldip=$(ip addr | awk '/^[0-9]+: / {}; /inet.*global/ {print gensub(/(.*)\/(.*)/, "\\1", "g", $2)}')
echo '当前系统的IP为:'$oldip
echo -n '请输入要修改的IP:'
read newip
sed -i "s/${oldip}/${newip}/g" /etc/sysconfig/network-scripts/ifcfg-ens33
echo -n '请输入hostname:'
read hostname
echo $hostname > /etc/hostname
service network restart
```

