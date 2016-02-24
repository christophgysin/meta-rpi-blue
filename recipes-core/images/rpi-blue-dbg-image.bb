include rpi-blue-image.bb

IMAGE_ROOTFS_SIZE = "1900000"

IMAGE_FEATURES += "package-management"

IMAGE_INSTALL_append += " alsa-utils-aplay"
IMAGE_INSTALL_append += " alsa-utils-alsamixer"
IMAGE_INSTALL_append += " pulseaudio-module-native-protocol-tcp"
