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
