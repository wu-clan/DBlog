import os

# 开机自启动脚本
uwsgi_files = os.listdir("/home/DBlog/")
os.system("uwsgi --ini /home/DBlog/uwsgi.ini")
