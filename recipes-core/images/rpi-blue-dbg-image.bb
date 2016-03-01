include rpi-blue-image.bb

IMAGE_ROOTFS_SIZE = "1900000"

IMAGE_FEATURES += "package-management"

IMAGE_INSTALL_append += " alsa-utils-aplay"
IMAGE_INSTALL_append += " alsa-utils-alsamixer"
IMAGE_INSTALL_append += " pulseaudio-module-native-protocol-tcp"
IMAGE_INSTALL_append += " pulseaudio-module-zeroconf-publish"

ROOTFS_POSTPROCESS_COMMAND_append += "load_pulseaudio_modules; "
load_pulseaudio_modules() {
    cat >> ${IMAGE_ROOTFS}/etc/pulse/system.pa <<EOF

load-module module-native-protocol-tcp auth-anonymous=1
load-module module-zeroconf-publish
EOF
}

