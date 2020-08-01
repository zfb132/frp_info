#! /bin/bash
# 插件监听的端口
PORT=6666
# 强制停止监听PORT端口的进程
kill -9  $(lsof -t -i:$PORT) > /dev/null 2>&1
# 判断上一个命令是否执行成功
if [ $? -eq 0 ];then
    echo "Kill $PORT port successfully!"
else
    echo "Fail to kill $PORT port"
fi
# 日志文件的路径和名称
NAME=~/frp-info/log/server.log
# 后台启动uwsgi
uwsgi uwsgi_frp-info.ini -d $NAME > /dev/null 2>&1
if [ $? -eq 0 ];then
    echo "Restart successfully!"
else
    echo "Fail to restart"
fi
