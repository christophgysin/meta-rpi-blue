include rpi-blue-image.bb

IMAGE_ROOTFS_SIZE = "1900000"

IMAGE_FEATURES += "package-management"

IMAGE_INSTALL_append += " alsa-utils-aplay"
IMAGE_INSTALL_append += " alsa-utils-alsamixer"
IMAGE_INSTALL_append += " pulseaudio-module-native-protocol-tcp"

enable_pulseaudio_protocols() {
    cat >> ${IMAGE_ROOTFS}/etc/pulse/system.pa <<EOF

# enable protocols
load-module module-native-protocol-unix auth-anonymous=1
load-module module-native-protocol-tcp auth-anonymous=1
EOF
}

ROOTFS_POSTPROCESS_COMMAND_append += "enable_pulseaudio_protocols; "
