#! /bin/sh
# /etc/init.d/noip 

### BEGIN INIT INFO
# Provides:          noip
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Simple script to start a program at boot
# Description:       A simple script from www.stuffaboutcode.com which will start / stop a program a boot / shutdown.
### END INIT INFO
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
sudo service ntp stop
sudo ntpd -gq
sudo service ntp start
cd /home/pi/Desktop
sudo git clone https://github.com/DexterInd/GrovePi
cd /home/pi/Desktop/GrovePi/Script
sudo chmod +x install.sh
sudo ./install.sh
sudo pip install paho-mqtt
sudo apt-get update
sudo locale-gen en_US.UTF-8
sudo update-locale
cd /home/pi/Desktop
git clone https://ser_unimelb@bitbucket.org/fdojurado/stem-project.git
cd /home/pi/Desktop/stem-project/DVDR_Client-master/Deployment
sudo cp superscript /etc/init.d/
sudo chmod 755 /etc/init.d/superscript
sudo update-rc.d superscript defaults
sudo apt-get update
echo "set your time zone"
sudo dpkg-reconfigure tzdata
echo "Deployment finish pls restart the raspberry pi"