#! /bin/bash
PORT=6666
kill -9  $(lsof -t -i:$PORT) > /dev/null 2>&1
if [ $? -eq 0 ];then
    echo "Kill $PORT port successfully!"
else
    echo "Fail to kill $PORT port"
fi
NAME=~/frp-info/log/server.log
uwsgi uwsgi_frp-info.ini -d $NAME > /dev/null 2>&1
if [ $? -eq 0 ];then
    echo "Restart successfully!"
else
    echo "Fail to restart"
fi
