FROM fateryu/ros2_humble_openvino

USER root

# create workspace
RUN mkdir -p /ros_ws/src
WORKDIR /ros_ws/

# clone projects (forked)
RUN cd src && git clone https://github.com/Blue474/rm_auto_aim --depth=1 && \
    git clone https://github.com/Blue474/rm_buff --depth=1 && \
    git clone https://github.com/Blue474/ros2_hik_camera --depth=1 && \
    git clone https://github.com/Blue474/rm_gimbal_description --depth=1 && \
    git clone https://github.com/Blue474/rm_serial_driver --depth=1 && \
    git clone https://github.com/Blue474/rm_vision --depth=1 && \
    git clone https://github.com/Blue474/rm_auto_record --depth=1

# Sketchy AI code that theoretically updates an APT key 
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc \
    | gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu jammy main" \
    > /etc/apt/sources.list.d/ros2.list
# Even sketchier AI code
RUN rm -f /etc/apt/sources.list.d/ros2-latest.list && \
    apt-get update && \
    rosdep install --from-paths src --ignore-src -r -y && \
    apt-get install -y ros-humble-foxglove-bridge wget htop vim nano && \
    rm -rf /var/lib/apt/lists/*


# install dependencies and some tools
RUN apt-get update && rosdep install --from-paths src --ignore-src -r -y && \
    apt-get install ros-humble-foxglove-bridge wget htop vim nano -y && \
    rm -rf /var/lib/apt/lists/*




# build
RUN . /opt/ros/humble/setup.sh && colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

# setup .zshrc
RUN echo 'source /ros_ws/install/setup.zsh' >> /root/.zshrc
RUN echo 'eval "$(register-python-argcomplete3 ros2)"' >> /root/.zshrc
RUN echo 'eval "$(register-python-argcomplete3 colcon)"' >> /root/.zshrc

CMD ["bash","~/ros_ws/src/rm_vision/setupFix.sh"]

