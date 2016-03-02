# Copyright (C) 2016 Christoph Gysin <christoph.gysin@gmail.com>
# Released under the MIT license (see COPYING.MIT for the terms)

DESCRIPTION = "Webinterface to trust bluetooth devices"
HOMEPAGE = "http://localhost"
LICENSE = "GPLv2"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI = "file://bluetrust.py"

PV = "0"

do_install() {
    install -D -m 755 "${WORKDIR}"/bluetrust.py "${bindir}"/bluetrust.py
}

RDEPENDS_${PN} += "bluez5"
RDEPENDS_${PN} += "python-dbus"
RDEPENDS_${PN} += "python-pygobject"
RDEPENDS_${PN} += "python-twisted"
