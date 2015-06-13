# qpn
pptp vpn with qingcloud autoconfig tool

# 安装说明
1. 注册[青云](https://www.qingcloud.com/)
2. 建立一个[亚太区路由](https://console.qingcloud.com/ap1/routers/)
3. 为该路由[开通PPTP服务](https://docs.qingcloud.com/guide/vpn.html#id4)
4. 获取青云[api密钥](https://console.qingcloud.com/access_keys/)
5. 安装青云api Python SDK `sudo pip install qingcloud-sdk`
6. 配置config.json填写相关信息

# 命令说明
1. `python qpn.py on [setting name]` 启动vpn
2. `python qpn.py off` 关闭 vpn

# 关于vpn设置
建议使用config.json中设置的host_name为目标地址,程序会在启动vpn的时候修改hosts文件，将其指向获取的ip地址，这样就不用每次都修改vpn配置了.
