Components needed
    1 × LED
    1 × 220Ω resistor
    Breadboard + jumper wires

GPIO selection (safe pin)

    Use:
        P9_12 → GPIO1_28 → GPIO60

Wiring
    9_12 (GPIO) ----[220Ω resistor]---->| LED ---- GND

LED polarity:

    Long leg → GPIO (via resistor)
    Short leg → GND

GPIO Mapping (important)
    GPIO number = (bank × 32) + pin
    GPIO1_28 = (1×32)+28 = 60

Quick Test in U-Boot (without custom command)

    Interrupt boot:

        => gpio status

    Set GPIO:

        => gpio set 60

    LED should turn ON ✅

    Turn OFF:

        => gpio clear 60

Use safe GPIOs like:

    Pin	        GPIO
    P9_12	    60
    P9_14	    50
    P9_16	    51