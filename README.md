# modern-sla-timelapse-mk1

# Setup
### Raspberry Pi
* Download the latest [Raspberry Pi OS](https://www.raspberrypi.org/software/operating-systems/) and flash it to an SD card using [Balena Etcher](https://www.balena.io/etcher/)
* Create a blank, extension-less file on that new `boot` drive called `ssh`
* Create a new file on the `boot` drive called `wpa_supplicant.conf` with the following contents
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
  ssid="YOUR_WIFI_NETWORK"
  scan_ssid=1
  psk="YOUR_WIFI_PASSWORD"
  key_mgmt=WPA-PSK
}
```
* Boot up the Pi, and SSH into it
```
ssh pi@<your-ip-address>
```
* Configure the pi to Auto-login at boot
```
sudo raspi-config
```
  * Navigate to System Options -> Boot/ Auto Login -> CLI Autologin
  * Save and exit raspi-config
* Clone this repository in the `home/pi` directory
```
cd 
git clone https://github.com/modern-hobbyist/modern-sla-timelapse-mk1.git
```
* Configure script to run at boot by editing `/etc/rc.local`
```
sudo nano /etc/rc.local
```
```
//Add the following line prior to the 'exit 0' line
sudo python /home/pi/modern-sla-timelapse-mk1/slaTimelapse.py &
```

* Wire the light sensor to the Pi
  * VCC -> RPi's 3.3v output
  * GND -> RPi's GND
  * D0  -> RPi's GPIO Pin 4
* Plug the camera into the Pi via USB and reboot!
```
sudo reboot
```


# Scripts
I will update this as the project evolves, but currently it is made up of 4 different scripts:
* install-gphoto2.sh
* initialize-camera-save-to-sd.sh
* trigger-snapshot.sh
* slaTimelapse.py

### Install-gphoto2.sh
This script, once run will execute everything needed in order to install GPhoto2. I got this script from FormerLurker in his [OctoLapse](https://github.com/FormerLurker/Octolapse/wiki/V0.4---Configuring-a-DSLR-With-No-Download) repository, since OctoLapse uses GPhoto2 as well. You will need to run this script first after SSHing into the Pi.
```shell
./modern-sla-timelapse-mk1/install-gphoto2.sh
```

### Initialize-camera-save-to-sd.sh
This script does a little bit of setup for GPhoto2 to correctly set the capture target, which will cause the picture to be correctly saved onto the camera's SD card. This is executed by the slaTimelapse.py script which we will configure to run at boot.

### trigger-snapshotsh
This script is the one that actually triggers the snapshot to occur, and it is also executed by slaTimelapse.py when it detects a flash of light. 

### slaTimelapse.py
This is the main script of this project. It is a pretty simple python script that reads the input of pin 4 on the Pi zero. If the input from pin 4 is low, then the light sensor is reporting that it sees light. Since an SLA printer only exposes the new layer of resin for a brief period of time, the script will trigger one snapshot, and it won't trigger another snapshot until the sensor has reported darkness and the next flash of light. This script executes `initialize-camera-save-to-sd.sh` once at the beginning of the script, and `trigger-snapshot.sh` each time a pulse of light is detected.
