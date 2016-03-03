HOMEPAGE = "https://github.com/christophgysin/bluetrust"
SUMMARY = "Webinterface to trust bluetooth devices"

SRC_URI = "https://github.com/christophgysin/bluetrust.git"

SRCREV = "${AUTOREV}"
S = "${WORKDIR}/git"
PV = "0+git${SRCPV}"

LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://${S}/COPYING;md5=b234ee4d69f5fce4486a80fdaf4a4263"

inherit distutils

RDEPENDS_${PN} += "python-core"
RDEPENDS_${PN} += "python-dbus"
RDEPENDS_${PN} += "python-pygobject"
RDEPENDS_${PN} += "python-twisted"
