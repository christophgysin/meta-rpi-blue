PR .= ".0"

EXTRA_OECONF := "${@oe_filter_out('--disable-coredump', '${EXTRA_OECONF}', d)}"

PACKAGECONFIG += "coredump"
PACKAGECONFIG[coredump] = "--enable-coredump,--disable-coredump"

FILES_${PN} += '${bindir}/coredumpctl'
