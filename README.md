# robotics133


Some ROS installation errors:


ROS2 on Fedora Errors so far using tavie/ROS2:

-rviz not displaying properly
	> due to wayland, need to use x
	> add `export QT_QPA_PLATFORM=xcb` to .bashrc

-need to always source ros
	> add `source usr/lib64/ros2-humble/setup.bash` to .bashrc
	
-need to always source the install folder after buildling
	> source `pathtorobotws/robotws/install/setup.bash`

you can actually ignore this one, it just gives a warning

-setup.py does not work on python 3.12
	> first use a virtual environment on python 3.10
	
	> set setuptools version to 58.2.0
	https://answers.ros.org/question/396439/setuptoolsdeprecationwarning-setuppy-install-is-deprecated-use-build-and-pip-and-other-standards-based-tools/
	
	> build using venv https://github.com/ros2/ros2/issues/1094#issuecomment-1503725544
	
	
