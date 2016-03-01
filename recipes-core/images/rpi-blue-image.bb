include recipes-core/images/rpi-hwup-image.bb

IMAGE_FEATURES += "ssh-server-dropbear"

IMAGE_INSTALL_append += " bluez5"
IMAGE_INSTALL_append += " pulseaudio-server"
IMAGE_INSTALL_append += " pulseaudio-module-alsa-card"
IMAGE_INSTALL_append += " pulseaudio-module-alsa-sink"
IMAGE_INSTALL_append += " pulseaudio-module-bluetooth-discover"
IMAGE_INSTALL_append += " pulseaudio-module-bluetooth-policy"
IMAGE_INSTALL_append += " pulseaudio-module-bluez5-device"
IMAGE_INSTALL_append += " pulseaudio-module-bluez5-discover"
IMAGE_INSTALL_append += " pulseaudio-module-loopback"
IMAGE_INSTALL_append += " python-dbus"
IMAGE_INSTALL_append += " python-pygobject"

ROOTFS_POSTPROCESS_COMMAND_append += "add_pulseaudio_system_service; "
add_pulseaudio_system_service() {
    cat > ${IMAGE_ROOTFS}/etc/systemd/system/pulseaudio-system.service <<EOF
[Unit]
Description=Sound Service

[Service]
ExecStart=/usr/bin/pulseaudio --system

[Install]
Also=pulseaudio-system.socket
WantedBy=default.target
EOF
    cat > ${IMAGE_ROOTFS}/etc/systemd/system/pulseaudio-system.socket <<EOF
[Unit]
Description=Sound System

[Socket]
Priority=6
Backlog=5
ListenStream=%t/pulse/native

[Install]
WantedBy=sockets.target
EOF
}

ROOTFS_POSTPROCESS_COMMAND_append += "add_bluetooth_config; "
add_bluetooth_config() {
    cat > ${IMAGE_ROOTFS}/etc/udev/rules.d/bluetooth.rules <<EOF
# Set bluetooth power up
ACTION=="add", KERNEL=="hci0", RUN+="/usr/bin/hciconfig hci0 up"
EOF

    cat > ${IMAGE_ROOTFS}/etc/dbus-1/system.d/pulseaudio-bluetooth.conf <<EOF
<!DOCTYPE busconfig PUBLIC "-//freedesktop//DTD D-BUS Bus Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd">
<busconfig>

  <!-- allow pulseaudio to communicate with bluetoothd -->
  <policy user="pulse">
    <allow send_destination="org.bluez"/>
  </policy>

</busconfig>
EOF

    cat >> ${IMAGE_ROOTFS}/etc/pulse/system.pa <<EOF

# enable bluetooth
load-module module-bluetooth-discover
load-module module-bluetooth-policy
EOF
}
