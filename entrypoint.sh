#! /bin/bash

# 若uwsgi的配置文件设置了非默认的端口，需要在此处改回6666
# 因为dockerfile中的EXPOSE指令已经暴露了6666端口
sed -i 's|http[[:blank:]]\{0,\}=.*|http = 0.0.0.0:6666|Ig' /frp/uwsgi_frp-info.ini

# 删除uwsgi的虚拟环境配置，因为这是一个单独的容器，不需要虚拟环境
sed -i 's|virtualenv[[:blank:]]\{0,\}=.*||Ig' /frp/uwsgi_frp-info.ini
sed -i 's|home[[:blank:]]\{0,\}=.*||Ig' /frp/uwsgi_frp-info.ini

uwsgi --ini /frp/uwsgi_frp-info.ini