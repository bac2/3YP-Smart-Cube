#!/bin/bash
unset number
for(( i=1; i<=6; i++)) do

	number=$number$(( $RANDOM/3276 ))
done

#Set the cube code
echo 'Generate Cube Code'
sed 's/Cube(\"[0-9]*\")/Cube\("'$number'"\)/' < cube/run.py >/dev/null

apt-get -y install i2c-tools

#Enable i2c
echo 'Enabled i2c loading'
awk '{ if ($0 == "i2c-dev") { print ""; } else { print $0; } }' < /etc/modules | sudo tee /etc/modules 1>/dev/null
echo 'i2c-dev' | sudo tee -a /etc/modules 1>/dev/null
sudo adduser pi i2c

awk '{ if ($0 ~ /^blacklist i2c-bcm2708/ ){print "#",$0} else { print $0;} }' < /etc/modprobe.d/raspi-blacklist.conf | sudo tee /etc/modprobe.d/raspi-blacklist.conf 1>/dev/null
echo 'Unblocked i2c driver'
apt-get -y install python-smbus
apt-get -y install python-pip
pip install requests
easy_install -U bottle
#sudo shutdown -r now

