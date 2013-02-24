apt-get -y install i2c-tools
echo 'i2c-dev' | sudo tee -a /etc/modules 
sudo adduser pi i2c

awk '{ if ($0 ~ /^blacklist i2c-bcm2708/ ){print "#",$0} else { print $0;} }' < /etc/modprobe.d/raspi-blacklist.conf | sudo tee /etc/modprobe.d/raspi-blacklist.conf 1>/dev/null
echo 'Unblocked i2c driver'
apt-get -y install python-smbus
apt-get -y install python-pip
pip install requests
easy_install -U bottle
sudo shutdown -r now
