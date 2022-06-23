#!/bin/bash
sudo apt-get update
sudo apt-get install python3-pip -y
sudo apt-get install screen -y
sudo apt-get install nano -y
pip3 install console-menu
pip3 install boto3
pip3 install pexpect
pip install six

# ROS2 Humble Install
sudo apt update && sudo apt install curl gnupg lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop
source ~/opt/ros/humble/setup.bash

# Rosdep Install
sudo apt install python3-rosdep2
rosdep update
sudo apt install python3-colcon-common-extensions

python3 ~/rover_tools_ros2/menu/menu_main.py --cf ${cf}
source ~/opt/ros/humble/setup.bash
source ~/rover_workspace/install/setup.sh
