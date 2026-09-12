"""GPIO map for Raspberry Pi Model B (2011.12) — verify on your P1 header revision."""

# BCM numbering
MOTOR_L_IN1 = 17
MOTOR_L_IN2 = 18
MOTOR_R_IN1 = 22
MOTOR_R_IN2 = 23

IR_FRONT_L = 27  # digital DO from TCRT5000 module
IR_FRONT_R = 24

ESTOP_BTN = 25  # active low to GND

# I2C VL53L0X on default bus 0/1 depending on Rev — check with i2cdetect
I2C_BUS = 1
