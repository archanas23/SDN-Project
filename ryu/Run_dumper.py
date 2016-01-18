import os
os.system("gnome-terminal -e 'bash -c \"PYTHONPATH=. ./bin/ryu-manager --verbose --observe-links ryu/topology/dumper.py ./ryu/controller/controller.py; exec bash\" ' ")

