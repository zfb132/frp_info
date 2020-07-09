# frp服务端插件开发
本代码运行在特定端口用于监听frp的RPC消息并进行处理。frp服务端插件的工作原理见[server_plugin_zh.md](https://github.com/fatedier/frp/blob/master/doc/server_plugin_zh.md)。简单来说就是我们创建的插件需要提供一个web服务，frp会在收到指定操作时把相关信息通过POST请求来发送给特定的url，而插件收到请求后可以根据内容来决定frp如何处理相关操作。若文件`frps.ini`添加以下内容  
```conf
[plugin.frp-info]
addr = 127.0.0.1:6666
path = /handler
ops = Login,NewProxy,NewWorkConn,NewUserConn
```
这表明frp会在收到`Login,NewProxy,NewWorkConn,NewUserConn`中的任意一种操作时将该操作的相关信息发送给插件，由插件决定是否进行下一步操作，插件的工作步骤如下：  
* 监听127.0.0.1:6666
* 创建/handler路由
* 接收frp的post请求发来的json数据
* 根据数据决定返回值
* 返回json数据

示例中的**监听端口、路由名称、操作类型**均可以自定义，开发插件也可以使用任何喜欢的编程语言，由于本人对Go语言不甚熟悉，所以采用python编写代码
## 1. frp-info插件使用说明
### 1.1 创建虚拟环境
插件基于python3编写，搭建flask服务（运行在虚拟环境），在当前项目主目录下创建虚拟环境并安装库：  
```bash
#! /bin/bash
# 自动安装venv管理虚拟环境
sudo apt-get install python3-venv -y
# 创建虚拟环境venv
python3 -m venv venv
# 激活虚拟环境并安装库
source venv/bin/activate && pip install  -r requirements.txt && deactivate
```
### 1.2 修改配置文件
1. 修改`frps.ini`文件,添加以下内容  
```conf
[plugin.frp-info]
addr = 127.0.0.1:6666
path = /handler
ops = Login,NewProxy,NewWorkConn,NewUserConn
```
2. 修改`uwsgi_frp-info.ini`文件来配置uwsgi启动参数，保证http监听端口与步骤1设置一致
3. 更改`config.py`来修改flask安全秘钥以及钉钉群机器人的安全秘钥和接口秘钥

### 1.3 运行代码
然后**在项目主目录下**输入以下命令测试启动uwsgi及插件frp-info：  
`source venv/bin/activate && uwsgi --ini uwsgi_frp-info.ini -d /dev/null && deactivate`  
此时可通过`cat ./log/frp-info.log`查看日志，或通过`lsof -i:6666`查看端口占用  
最后重启frps服务`service frps restart`即可实现插件的安装配置
## 2. 添加插件自启动
修改`frp-info.service`文件的uwsgi路径和配置文件路径为本机的路径，修改用户为本机的用户名  
```conf
[Unit]
Description=Frp-info service
After=network.target

[Service]
Type=simple
User=ubuntu
Restart=on-failure
RestartSec=5s
WorkingDirectory=/home/ubuntu/frp-info
ExecStart=/home/ubuntu/frp-info/venv/bin/uwsgi --ini /home/ubuntu/frp-info/uwsgi_frp-info.ini

[Install]
WantedBy=multi-user.target
```
然后将此文件移动到系统服务目录：`sudo mv ./frp-info.service /etc/systemd/system/`  
启动开机自启功能：`systemctl enable frp-info`  
手动运行服务：`service frp-info start`  
则所有配置完成，插件已正常工作，若重新启动系统，则`frps`和`frp-info`的service都会启动

## 3. 服务管理的命令
重载服务后台（手动修改service文件后执行）：`sudo systemctl daemon-reload`  
关闭服务：`service frp-info stop`  
手动重启服务：`service frp-info restart`  
查看开机自启的服务：`systemctl list-unit-files --type=service|grep enabled`   
```txt
ubuntu@VM-16-13-ubuntu:~/$ systemctl status frp-info.service
● frp-info.service - Frp-info service
   Loaded: loaded (/etc/systemd/system/frp-info.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2020-07-08 23:33:29 CST; 4min 41s ago
 Main PID: 5040 (uwsgi)
    Tasks: 14 (limit: 2122)
   CGroup: /system.slice/frp-info.service
           ├─5040 /home/ubuntu/frp-info/venv/bin/uwsgi --ini /home/ubuntu/frp-info/uwsgi_frp-info.ini
           ├─5057 /home/ubuntu/frp-info/venv/bin/uwsgi --ini /home/ubuntu/frp-info/uwsgi_frp-info.ini
           ├─5058 /home/ubuntu/frp-info/venv/bin/uwsgi --ini /home/ubuntu/frp-info/uwsgi_frp-info.ini
           ├─5059 /home/ubuntu/frp-info/venv/bin/uwsgi --ini /home/ubuntu/frp-info/uwsgi_frp-info.ini
           ├─5060 /home/ubuntu/frp-info/venv/bin/uwsgi --ini /home/ubuntu/frp-info/uwsgi_frp-info.ini
           └─5063 /home/ubuntu/frp-info/venv/bin/uwsgi --ini /home/ubuntu/frp-info/uwsgi_frp-info.ini

Jul 08 23:35:43 VM-16-13-ubuntu uwsgi[5040]: [pid: 5059|app: 0|req: 3/13] 127.0.0.1 () {34 vars in ...
ubuntu@VM-16-13-ubuntu:~/$
```