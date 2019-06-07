### 虚拟机修改ip

执行命令如下：
```
vi /etc/sysconfig/network-scripts/ifcfg-eth0

```
修改内容如下：

```
DEVICE=eth2
TYPE=Ethernet
ONBOOT=yes
NM_CONTROLLED=yes
BOOTPROTO=none
IPADDR=192.168.188.3
PREFIX=24
GATEWAY=192.168.188.254
DNS1=10.100.1.12
```
执行保存退出 

```
service network restart
```
