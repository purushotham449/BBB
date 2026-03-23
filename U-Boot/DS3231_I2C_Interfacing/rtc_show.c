#include <common.h>
#include <command.h>
#include <i2c.h>

static int bcd_to_dec(u8 val)
{
    return ((val >> 4) * 10) + (val & 0x0F);
}

static int do_rtcshow(struct cmd_tbl *cmdtp, int flag,
                     int argc, char * const argv[])
{
    u8 buf[7];

    if (i2c_read(0x68, 0x00, 1, buf, 7)) {
        printf("RTC read failed\n");
        return -1;
    }

    int sec  = bcd_to_dec(buf[0]);
    int min  = bcd_to_dec(buf[1]);
    int hour = bcd_to_dec(buf[2]);
    int date = bcd_to_dec(buf[4]);
    int mon  = bcd_to_dec(buf[5]);
    int year = 2000 + bcd_to_dec(buf[6]);

    printf("Time: %02d:%02d:%02d\n", hour, min, sec);
    printf("Date: %02d-%02d-%04d\n", date, mon, year);

    return 0;
}

U_BOOT_CMD(
    rtcshow, 1, 0, do_rtcshow,
    "Show DS3231 time",
    ""
);