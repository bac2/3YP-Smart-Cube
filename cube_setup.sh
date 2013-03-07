#!/bin/bash
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
sed 's/Cube(\"[0-9]*\")/Cube\("'$number'"\)/' < cube/run.py >temp
cp temp cube/run.py
rm temp

sed "s/SECRET_CODE = '.*'$/SECRET_CODE = '"$code"'/" <cube/cube.py >temp
cp temp cube/cube.py
rm temp

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
easy_install supervisor
curl https://raw.github.com/gist/176149/88d0d68c4af22a7474ad1d011659ea2d27e35b8d/supervisord.sh > supervisord
chmod +x supervisord
mv supervisord /etc/init.d/supervisord
update-rc.d supervisord defaults

echo_supervisor_conf > /etc/supervisord.conf
/etc/init.d/supervisord start

echo [include] >> /etc/supervisord.conf
echo files=/etc/supervisord/*.conf >> etc/supervisord.conf
mkdir /etc/supervisord
echo [program:cube] > /etc/supervisord/cube.conf
echo command=/home/pi/3YP/cube/run.py start >> /etc/supervisord/cube.conf
echo "" >> /etc/supervisord/cube.conf
echo [program:wifi] >> /etc/supervisord/cube.conf
echo command=/home/pi/3YP/wifi.py >> /etc/supervisord/cube.conf

echo Installing noip client...
cd /usr/local/src
wget https://www.noip.com/client/linux/noip-duc-linux.tar.gz
tar -xzf noip-duc-linux.tar.gz
cd no-ip-2.1.9-1
make
make install

sed 's/^exit 0/\/usr\/local\/bin\/noip2\
\
&/' /etc/rc.local > temp
cp temp /etc/rc.local
rm temp

supervisorctl reload
echo 'Installation Complete'
