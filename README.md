# traintraintrain scanner [![Build Status](https://travis-ci.com/datagovsg/ttt-scanner.svg?token=CA62Uz9gfaZnQ7Cyx7yy&branch=master)](https://travis-ci.com/datagovsg/ttt-scanner)

Locate trains with wifi data

## Setup and Resin.io managed deployments (preferred)

### Prepare the resinOS

1. Download the resinOS from the Resin Dashboard (application: `traintraintrain`)
2. Using a disk-imaging editor like [WinImage](http://www.winimage.com/), add `config.txt` to `/resin-boot` (partition 0). Also add `cellular` to `/resin-boot/system-connections`. These configuration files are found in `resinos_config/`. Remember to save the image.

You may skip these steps by downloading the preconfigured image [here](https://drive.google.com/file/d/1P0_dPqboi5iRATjyisaK08Qc3DJ4Yxy2/view?usp=sharing).

### Initial Raspberry Pi setup

1. Use an image flasher like [Etcher](https://etcher.io/) to flash the image.
2. Insert the microSD card into the Rpi and connect an ethernet cable which provides an internet connection.
3. During the first bootup, resinOS will connect to resin.io servers and register the device to the `traintraintrain` application.
4. Resin.io will deploy the docker image to the device.
5. Test and ensure that the app is successfully running on the device.
6. Switch the device off and disconnect the ethernet cable. Connect the GSM dongle.

Internet connection via ethernet cable is preferred as the initial deployment will fetch the entire docker image which can be large. Subsequent deployments fetches only the new docker image layers.

Repeat steps for all the Rpis needed to be setup.

### Application deployment

This is an automated step done by Travis whenever a PR is merged into the `master` branch.

### What to do if `resin_supervisor` container becomes unhealthy

Symptoms of a problematic resin supervisor:
- You cannot reach your resin device via the resin APIs/dashboard (e.g. reboot or restart)
- Resin.io does not push a new release to your device
- No logs shown on the resin device dashboard

The issue is described in detail here: https://forums.resin.io/t/no-logs-found-error/2917/4?u=chrissng

From the resin device's host OS,
```bash
cd /resin-data/resin-supervisor
mv database.sqlite database.sqlite.bak  # or to something else if it exists
balena restart resin_supervisor
```

## Setup (Docker on Raspberry Pi)

This assumes Raspbian (host OS) is installed.

### Configure Host OS on Rpi

- Using `raspi-config`, set Locale to en-US UTF-8, use the US keyboard, and use Singapore time zone
- Disable wlan soft block and power save (see HOW-TOs below)

### Fetch repo

```bash
git clone git@github.com:datagovsg/mrt-location.git
```

### Configure AWS credentials and train ID
Credentials are stored in `scrape/mrtScanner/config.ini`.

Configure the credentials according to the following the template:
```
[default]
train_id = < unique_train_device_id >

[firebase]

[aws]
region_name = < aws_region_name >
aws_secret_access_key = < aws_secret_access_key >
aws_access_key_id = < aws_access_key_id >
```

### Download Docker
```
curl -sSL https://get.docker.com | sh
```

### Build and start docker container

```bash
sudo docker build -t traintraintrain .
sudo docker run --net=host --privileged --restart=always --name=ttt -d --env-file=env.list traintraintrain
```

## Setup (Docker-based development)

Follow the docker setup steps in the previous section

### Mounting the scripts

To make development easy without having to rebuild the image every time scripts are modified.

```bash
sudo docker run ... --volume scrape:/mrt:ro ...
```

## Setup (Local development)

### First, clone the repo and set up virtualenv

We recommend virtualenv. For instructions: http://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv

```
git clone git@github.com:datagovsg/mrt-location.git
cd mrt-location
virtualenv -p python2 env
source env/bin/activate
```

### Install libraries

```
pip install -r requirements.txt
```

### Running scraper on Mac

```
python scrapeMac.py
```

## Raspberry Pi HOW-TOs

### Undo wlan soft block and disable power save mode on Rpi 3B+

1. Add `country=SG` as the first line in `/etc/wpa_supplicant/wpa_supplicant.conf`
2. Add `iwconfig wlan0 power off` in `/etc/rc.local`

### Firmware to patch raspberry pi wifi modules for monitor mode
https://github.com/seemoo-lab/nexmon

### Setting up usb modem on raspberry pi
https://nicovddussen.wordpress.com/2014/11/12/setting-up-your-raspberry-pi-to-work-with-a-3g-dongle/
https://www.thefanclub.co.za/how-to/how-setup-usb-3g-modem-raspberry-pi-using-usbmodeswitch-and-wvdial

### Enable SSH on startup
Create an empty file named `ssh` in the `/boot` directory on the Pi. This only needs to be done once.

```bash
sudo touch /boot/ssh
```

### Boot script on startup
The script in `/etc/rc.local` script has been modified to include the following
1. Add monitoring mode to the wireless adapter
2. Run `python scrapePi.py`
* The `&` on the second last lime is required to prevent the pi from hanging

```bash
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

sudo su
iw phy phy0 interface add mon0 type monitor
ifconfig mon0 up
cd /home/pi/mrt-location/scrape/
python scrapePi.py &
exit 0
```
