SUMMARY = "WiFi auto connect script"
LICENSE = "CLOSED"

SRC_URI = " \
    file://wifi.sh \
    file://wpa_supplicant.conf \
"

S = "${WORKDIR}"

do_install() {
    install -d ${D}/etc/init.d
    install -m 0755 ${WORKDIR}/wifi.sh ${D}/etc/init.d/wifi.sh
}

FILES:${PN} += "/etc/init.d/wifi.sh /etc/wpa_supplicant.conf"

inherit update-rc.d

INITSCRIPT_NAME = "wifi.sh"
INITSCRIPT_PARAMS = "defaults"