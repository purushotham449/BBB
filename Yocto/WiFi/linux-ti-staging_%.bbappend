do_configure:append() {
    echo "CONFIG_CFG80211=y" >> ${B}/.config
    echo "CONFIG_MAC80211=y" >> ${B}/.config
    echo "CONFIG_WLCORE=m" >> ${B}/.config
    echo "CONFIG_WLCORE_SDIO=m" >> ${B}/.config
    echo "CONFIG_WL18XX=m" >> ${B}/.config
}

KERNEL_DEVICETREE:append = " am335x-boneblack-wireless.dtb"

SRC_URI += "file://wl18xx-conf.bin"

do_install:append() {
    install -m 0644 ${WORKDIR}/wl18xx-conf.bin ${D}/lib/firmware/ti-connectivity/
}