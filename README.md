# frp插件开发
本代码运行在特定端口用于监听frp的RPC消息
## 运行代码
首先在当前项目主目录下创建虚拟环境  
`python3 -m venv venv`  
然后安装`requirements.txt`文件的依赖  
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