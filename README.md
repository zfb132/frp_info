# frp插件开发
本代码运行在特定端口用于监听frp的RPC消息
## 运行代码
首先在当前项目主目录下创建虚拟环境  
`python3 -m venv venv`  
然后**激活虚拟环境**并在其中安装`requirements.txt`文件的依赖  
`pip install -r requirements.txt`  
然后输入以下命令启动uwsgi：  
`source venv/bin/activate && uwsgi --ini uwsgi_frp-info.ini -d /dev/null && deactivate`  
再添加以下内容到文件`frps.ini`  
```conf
[plugin.frp-info]
addr = 127.0.0.1:6666
path = /handler
ops = Login,NewProxy,NewWorkConn,NewUserConn
```
最后重启frps服务`service frps restart`即可实现插件的安装配置
## 修改配置
用户可以更改`uwsgi_frp-info.ini`文件来配置uwsgi启动参数  
更改`frp-info.service`来修改启动路径和配置文件路径  
更改`config.py`来修改flask安全秘钥以及钉钉群机器人的安全秘钥和接口秘钥  
## 添加自启动
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
重载服务后台：`sudo systemctl daemon-reload`  
启动开机自启功能：`systemctl enable frp-info`  
手动运行服务：`service frp-info start`  
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
重新启动系统，则`frps`和`frp-info`的service都会启动