#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This must be run by root! Did you use sudo?"
	exit 1
fi

unset number
for(( i=1; i<=6; i++)) do

	number=$number$(( $RANDOM/3276 ))
done

#Set the cube code
echo 'Generated Cube Code - ' $number
echo 'import hashlib' > temp
echo 'print hashlib.sha224(str('$number')).hexdigest()' >> temp
code=`python temp`
rm temp

echo 'Generated Secret Code - ' $code 
echo [cube] > temp
echo code = $number >> temp
echo secret = $code >> temp
echo XPos = [59, 50, 26] >> temp
echo XNeg = [64, 78, 0] >> temp
echo YPos = [44, 60, 4] >> temp
echo YNeg = [79, 69, 20] >> temp
echo ZPos = [70, 51, 0] >> temp
echo ZNeg = [53, 77, 24] >> temp
cp temp cube/cube.conf
rm temp
echo 'Created config file in cube.conf...'

echo 'Installing i2c-tools...'
apt-get -y install i2c-tools >/dev/null

#Enable i2c
echo 'Enabled i2c loading...'
awk '{ if ($0 == "i2c-dev") { print ""; } else { print $0; } }' < /etc/modules | sudo tee /etc/modules 1>/dev/null
echo 'i2c-dev' | sudo tee -a /etc/modules 1>/dev/null
sudo adduser pi i2c >/dev/null

awk '{ if ($0 ~ /^blacklist i2c-bcm2708/ ){print "#",$0} else { print $0;} }' < /etc/modprobe.d/raspi-blacklist.conf | sudo tee /etc/modprobe.d/raspi-blacklist.conf 1>/dev/null
echo 'Unblocked i2c driver...'
echo 'Installing python-smbus...'
apt-get -y install python-smbus >/dev/null
echo 'Installing python-pip...'
apt-get -y install python-pip >/dev/null
echo 'Installing python requests...'
pip install requests >/dev/null
echo 'Installing python bottle...'
easy_install -U bottle >/dev/null
echo 'Installing python supervisor...'
easy_install supervisor >/dev/null
curl https://raw.github.com/gist/176149/88d0d68c4af22a7474ad1d011659ea2d27e35b8d/supervisord.sh 1> supervisord 2>/dev/null
chmod +x supervisord
mv supervisord /etc/init.d/supervisord
update-rc.d supervisord defaults >/dev/null

echo_supervisord_conf > /etc/supervisord.conf
/etc/init.d/supervisord start 2>/dev/null 1>/dev/null

echo [include] >> /etc/supervisord.conf
echo files=/etc/supervisord/*.conf >> /etc/supervisord.conf
mkdir /etc/supervisord 2>/dev/null
echo [program:cube] > /etc/supervisord/cube.conf
echo command=/home/pi/3YP/cube/run.py start >> /etc/supervisord/cube.conf
echo "" >> /etc/supervisord/cube.conf
echo [program:wifi] >> /etc/supervisord/cube.conf
echo command=/home/pi/3YP/wifi.py >> /etc/supervisord/cube.conf

echo Installing noip client...
cd /usr/local/src
wget https://www.noip.com/client/linux/noip-duc-linux.tar.gz 1>/dev/null 2>/dev/null
tar -xzf noip-duc-linux.tar.gz >/dev/null
cd noip-2.1.9-1
make 2>/dev/null
make install 

sed 's/^exit 0/\/usr\/local\/bin\/noip2\
\
&/' /etc/rc.local > temp
cp temp /etc/rc.local
rm temp

supervisorctl reload >/dev/null
echo 'Installation Complete'
