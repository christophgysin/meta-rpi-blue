FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

EXTRA_OECONF += "--disable-ldconfig"
PACKAGECONFIG += "networkd resolved"
CFLAGS_append_arm = " -fno-lto"

SRC_URI += "file://eth.network"

FILES_${PN} += "{sysconfdir}/systemd/network/*"

do_install_append() {
    install -d ${D}${sysconfdir}/systemd/network/
    install -m 0644 ${WORKDIR}/*.network ${D}${sysconfdir}/systemd/network/
}
