#!/bin/bash
sudo apt-get update
sudo apt-get install python3-pip -y
sudo apt-get install screen -y
sudo apt-get install nano -y
pip3 install console-menu
pip3 install boto3
pip3 install pexpect
pip install six
cwd=$(pwd)
cf="${cwd}/../credentials.json"
python3 ~/rover_tools_ros2/menu/menu_main.py --cf ${cf}
source /opt/ros/humble/setup.bash
source ~/rover_workspace/install/setup.sh
