// SPDX-License-Identifier: GPL-2.0+
#include <common.h>
#include <command.h>
#include <asm/gpio.h>
#include <linux/delay.h>

#define LED0 53
#define LED1 54
#define LED2 55
#define LED3 56

static int do_ledtest(struct cmd_tbl *cmdtp, int flag, int argc, char * const argv[])
{
    int leds[] = { LED0, LED1, LED2, LED3 };
    int i, j;

    printf("U-Boot USER LED GPIO test\n");

    for (i = 0; i < 4; i++) {
        if (gpio_request(leds[i], "led")) {
            printf("FAIL: GPIO %d request failed\n", leds[i]);
            return CMD_RET_FAILURE;
        }
        gpio_direction_output(leds[i], 0);
    }

    for (j = 0; j < 5; j++) {
        for (i = 0; i < 4; i++) {
            gpio_set_value(leds[i], 1);
            mdelay(200);
            gpio_set_value(leds[i], 0);
        }
    }

    for (i = 0; i < 4; i++)
        gpio_free(leds[i]);

    printf("LED test PASS\n");
    return CMD_RET_SUCCESS;
}

//#ifndef CONFIG_SPL_BUILD
U_BOOT_CMD(
    ledtest, 1, 0, do_ledtest,
    "Test BeagleBone USER LEDs",
    "");
