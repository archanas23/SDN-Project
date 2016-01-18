import os
os.system("gnome-terminal -e 'bash -c \"PYTHONPATH=. ./bin/ryu-manager --verbose --observe-links ryu/app/bestpath.py ./ryu/app/ofctl_rest.py; exec bash\" ' ")


