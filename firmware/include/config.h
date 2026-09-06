#pragma once

// --- pins (DevKit v1; change to match your wiring) ---
static const int PIN_MOTOR_L_IN1 = 25;
static const int PIN_MOTOR_L_IN2 = 26;
static const int PIN_MOTOR_R_IN1 = 27;
static const int PIN_MOTOR_R_IN2 = 14;
static const int PIN_WIPE_PWM    = 33;  // disc/pad motor via driver EN or MOSFET

static const int PIN_EDGE_FL = 34;  // ADC-capable inputs for IR reflectance
static const int PIN_EDGE_FR = 35;
static const int PIN_EDGE_RL = 32;
static const int PIN_EDGE_RR = 39;

static const int PIN_ESTOP_BTN = 4;  // active LOW with INPUT_PULLUP

static const int EDGE_THRESHOLD = 1500;  // tune on wet glass: below = no surface / edge
static const uint32_t LOOP_HZ = 50;
static const float AUTO_SPEED = 0.35f;
