#!/bin/bash

mkdir /home/analog/git
cd /home/analog/git

# Uninstall existing pyadi, reinstall from source:

sudo pip3 uninstall -y pyadi-iio
git clone https://github.com/analogdevicesinc/pyadi-iio.git
cd pyadi-iio
git checkout master
sudo python3 setup.py install
cd /home/analog/git


# Install libiio with HWMON support (and other goodies)

git clone https://github.com/analogdevicesinc/libiio.git
cd libiio
git checkout master
mkdir build && cd build && cmake -DWITH_SYSTEMD=ON -DWITH_HWMON=ON -DWITH_EXAMPLES=ON ../ && make && sudo make install
cd /home/analog

# Install USB gadget service. DON'T forget to add

git clone https://github.com/analogdevicesinc/linux_image_ADI-scripts.git
cd linux_image_ADI-scripts/usb-gadget-service
sudo ./install_gt.sh
cd /home/analog/git

git clone https://github.com/mthoren-adi/gnuradio_projects.git

cd /home/analog/

echo "installed USB gadget, don't forget to add dtoverlay=dwc2 to config.txt and modules-load=dwc2 to cmdline.txt"

echo "Grabbing edited config_act_2022.txt, renaming, copying to /boot/"
wget https://raw.githubusercontent.com/mthoren-adi/devicetree_overlays/main/config_act_2022.txt?raw=true
mv config_act_2022.txt config.txt
sudo mv /boot/config.txt /boot/config_orig.txt
sudo cp config.txt /boot/

echo "Grabbing lm75 overlay and copying to root..."
wget https://github.com/mthoren-adi/devicetree_overlays/blob/main/rpi-lm75.dtbo?raw=true
sudo cp rpi-lm75.dtbo /boot/overlays

