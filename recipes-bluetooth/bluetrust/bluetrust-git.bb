HOMEPAGE = "https://github.com/christophgysin/bluetrust"
SUMMARY = "Webinterface to trust bluetooth devices"

SRC_URI = "git://github.com/christophgysin/bluetrust.git;protocol=https"

SRCREV = "${AUTOREV}"
S = "${WORKDIR}/git"

LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://${S}/COPYING;md5=b234ee4d69f5fce4486a80fdaf4a4263"

inherit distutils

RPROVIDES_${PN} = "bluetrust"

RDEPENDS_${PN} += "python-core"
RDEPENDS_${PN} += "python-dbus"
RDEPENDS_${PN} += "python-pygobject"
RDEPENDS_${PN} += "python-twisted-web"
