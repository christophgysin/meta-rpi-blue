HOMEPAGE = "https://github.com/christophgysin/bluetrust"
SUMMARY = "Webinterface to trust bluetooth devices"

SRC_URI = "git://github.com/christophgysin/bluetrust.git;protocol=https"

SRCREV = "${AUTOREV}"
PV = "0.${SRCPV}"
S = "${WORKDIR}/git"

LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://${S}/COPYING;md5=b234ee4d69f5fce4486a80fdaf4a4263"

inherit distutils

RDEPENDS_${PN} += "bluez5"
RDEPENDS_${PN} += "python-core"
RDEPENDS_${PN} += "python-dbus"
RDEPENDS_${PN} += "python-json"
RDEPENDS_${PN} += "python-pygobject"
RDEPENDS_${PN} += "python-twisted-web"

do_install_append() {
    install -D -m 644 "${S}/${PN}.service" \
        "${D}${systemd_system_unitdir}/${PN}.service"
    install -D -m 644 "${S}/${PN}.socket" \
        "${D}${systemd_system_unitdir}/${PN}.socket"
}

inherit systemd
SYSTEMD_PACKAGES = "${PN}"
SYSTEMD_SERVICE_${PN} = "${PN}.socket"
