# Inexplicable fix that makes this build file work. Sourced from gemini
rm /etc/apt/sources.list.d/ros2-latest.list
rm /etc/apt/sources.list.d/ros2.list
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" > /etc/apt/sources.list.d/ros2.list
apt update
apt install ros-humble-robot-state-publisher -y

# source the files to bash
echo "source /opt/ros/humble/setup.sh" >> ~/.bashrc
echo "source /ros_ws/install/setup.sh" >> ~/.bashrc
source ~/.bashrc