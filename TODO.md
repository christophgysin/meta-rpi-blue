smart config?
# smart channel -y --add all type=rpm-md baseurl=http://ezekiel/rpm/all
# smart channel -y --add arm1176jzfshf_vfp type=rpm-md baseurl=http://ezekiel/rpm/arm1176jzfshf_vfp
# smart channel -y --add raspberrypi type=rpm-md baseurl=http://ezekiel/rpm/raspberrypi
# smart update

# modprobe snd-bcm2835
autoload?

/etc/dbus-1/system.d/bluetooth.conf
<policy user="pulse">
  <allow send_destination="org.bluez"/>
</policy>

/etc/pulse/system.pa:

load-module module-bluetooth-discover
load-module module-bluetooth-policy
#load-module module-native-protocol-unix auth-anonymous=1
#load-module module-native-protocol-tcp auth-anonymous=1

# pulseaudio --system
service?


/etc/udev/rules.d/10-local.rules
# Set bluetooth power up
ACTION=="add", KERNEL=="hci0", RUN+="/usr/bin/hciconfig hci0 up"

# bluetoothctl
connect
