FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += "file://modules-load.conf"

do_install:append() {
    install -d ${D}/etc/modules-load.d
    install -m 0644 ${WORKDIR}/modules-load.conf ${D}/etc/modules-load.d/wl18xx.conf
}