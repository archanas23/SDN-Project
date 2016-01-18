import os 
os.system("gnome-terminal -e 'bash -c \"PYTHONPATH=. ./bin/ryu-manager ryu/app/simple_switch.py; exec bash\" ' ")

