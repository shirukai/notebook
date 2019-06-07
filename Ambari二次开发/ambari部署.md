# amber部署
## web页面手动部署
 * ### 将deployer-inspur文件部署到/opt目录下
    利用Xshell工具将文件复制到目录
 * ### 切换到/opt/deployer-inspur目录
        [root@localhost opt]# cd /opt/deployer-inspur
 * ### 在Manager所在的节点执行以下命令查看ip
        [root@localhost deployer-inspur]# ifconfig
 * ### 获取ip信息
        ens33: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.188.101  netmask 255.255.255.0  broadcast 192.168.188.255
        inet6 fe80::83ba:1dde:a208:bf28  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:d3:76:5c  txqueuelen 1000  (Ethernet)
        RX packets 1938  bytes 144789 (141.3 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2406  bytes 711258 (694.5 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
    ip地址为：192.168.188.101
 * ### 在此目录执行如下命令，根据提示输入ip，启动服务
        [root@localhost deployer-inspur]# bash env.sh
        Enter ipaddress of this machine: 192.168.188.101
        Enter ipaddress of this machine again: 192.168.188.101

 * ### 访问http://ip地址:8000/index.html,查看服务是否正常启动
