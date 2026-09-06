/**
 * PV-Clean Rain — ESP32 starter firmware
 * Serial JSON API @ 115200. Edge sensors force motor cutoff.
 */
#include <Arduino.h>
#include <ArduinoJson.h>
#include "config.h"

enum class Mode : uint8_t { Idle, Manual, AutoRow, Fault };

static Mode mode = Mode::Idle;
static float cmdDrive = 0, cmdTurn = 0, cmdWipe = 0;
static bool faultEdge = false;
static uint32_t lastWatchdog = 0;

static void motorsWrite(float drive, float turn, float wipe) {
  // Simple tank mix → left/right in [-1,1]
  float left = constrain(drive - turn, -1.f, 1.f);
  float right = constrain(drive + turn, -1.f, 1.f);
  auto channel = [](float v, int in1, int in2) {
    int pwm = (int)(fabsf(v) * 255);
    if (v > 0.05f) {
      analogWrite(in1, pwm);
      analogWrite(in2, 0);
    } else if (v < -0.05f) {
      analogWrite(in1, 0);
      analogWrite(in2, pwm);
    } else {
      analogWrite(in1, 0);
      analogWrite(in2, 0);
    }
  };
  channel(left, PIN_MOTOR_L_IN1, PIN_MOTOR_L_IN2);
  channel(right, PIN_MOTOR_R_IN1, PIN_MOTOR_R_IN2);
  analogWrite(PIN_WIPE_PWM, (int)(constrain(wipe, 0.f, 1.f) * 255));
}

static void motorsStop() {
  motorsWrite(0, 0, 0);
  cmdDrive = cmdTurn = cmdWipe = 0;
}

static bool edgeUnsafe() {
  int fl = analogRead(PIN_EDGE_FL);
  int fr = analogRead(PIN_EDGE_FR);
  int rl = analogRead(PIN_EDGE_RL);
  int rr = analogRead(PIN_EDGE_RR);
  // Low reading ≈ looking off glass (tune for your IR sensors)
  return fl < EDGE_THRESHOLD || fr < EDGE_THRESHOLD ||
         rl < EDGE_THRESHOLD || rr < EDGE_THRESHOLD;
}

static void enterFault(const char *why) {
  mode = Mode::Fault;
  faultEdge = true;
  motorsStop();
  Serial.printf("{\"ok\":false,\"err\":\"%s\",\"mode\":\"fault\"}\n", why);
}

static void replyOk(JsonDocument &extra) {
  extra["ok"] = true;
  const char *m = "idle";
  if (mode == Mode::Manual) m = "manual";
  else if (mode == Mode::AutoRow) m = "auto_row";
  else if (mode == Mode::Fault) m = "fault";
  extra["mode"] = m;
  serializeJson(extra, Serial);
  Serial.println();
}

static void handleLine(const String &line) {
  JsonDocument doc;
  if (deserializeJson(doc, line)) {
    Serial.println("{\"ok\":false,\"err\":\"bad_json\"}");
    return;
  }
  const char *cmd = doc["cmd"] | "";
  JsonDocument out;

  if (strcmp(cmd, "ping") == 0) {
    out["pong"] = true;
    replyOk(out);
    return;
  }
  if (strcmp(cmd, "status") == 0) {
    out["edge_unsafe"] = edgeUnsafe();
    out["fault"] = faultEdge;
    replyOk(out);
    return;
  }
  if (strcmp(cmd, "stop") == 0) {
    motorsStop();
    if (mode != Mode::Fault) mode = Mode::Idle;
    replyOk(out);
    return;
  }
  if (strcmp(cmd, "estop") == 0) {
    enterFault("estop");
    return;
  }
  if (strcmp(cmd, "clear_fault") == 0) {
    if (!edgeUnsafe() && digitalRead(PIN_ESTOP_BTN) == HIGH) {
      faultEdge = false;
      mode = Mode::Idle;
      replyOk(out);
    } else {
      Serial.println("{\"ok\":false,\"err\":\"still_unsafe\"}");
    }
    return;
  }
  if (strcmp(cmd, "set_mode") == 0) {
    if (mode == Mode::Fault) {
      Serial.println("{\"ok\":false,\"err\":\"fault\"}");
      return;
    }
    const char *m = doc["mode"] | "idle";
    if (strcmp(m, "idle") == 0) mode = Mode::Idle;
    else if (strcmp(m, "manual") == 0) mode = Mode::Manual;
    else if (strcmp(m, "auto_row") == 0) {
      mode = Mode::AutoRow;
      cmdDrive = doc["speed"] | AUTO_SPEED;
      cmdTurn = 0;
      cmdWipe = 1.f;
    } else {
      Serial.println("{\"ok\":false,\"err\":\"bad_mode\"}");
      return;
    }
    replyOk(out);
    return;
  }
  if (strcmp(cmd, "start_row") == 0) {
    if (mode == Mode::Fault) {
      Serial.println("{\"ok\":false,\"err\":\"fault\"}");
      return;
    }
    mode = Mode::AutoRow;
    cmdDrive = doc["speed"] | AUTO_SPEED;
    cmdTurn = 0;
    cmdWipe = 1.f;
    replyOk(out);
    return;
  }
  if (strcmp(cmd, "manual") == 0) {
    if (mode == Mode::Fault) {
      Serial.println("{\"ok\":false,\"err\":\"fault\"}");
      return;
    }
    mode = Mode::Manual;
    cmdDrive = doc["drive"] | 0.f;
    cmdTurn = doc["turn"] | 0.f;
    cmdWipe = doc["wipe"] | 0.f;
    replyOk(out);
    return;
  }
  Serial.println("{\"ok\":false,\"err\":\"unknown_cmd\"}");
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_MOTOR_L_IN1, OUTPUT);
  pinMode(PIN_MOTOR_L_IN2, OUTPUT);
  pinMode(PIN_MOTOR_R_IN1, OUTPUT);
  pinMode(PIN_MOTOR_R_IN2, OUTPUT);
  pinMode(PIN_WIPE_PWM, OUTPUT);
  pinMode(PIN_ESTOP_BTN, INPUT_PULLUP);
  motorsStop();
  lastWatchdog = millis();
  Serial.println("{\"ok\":true,\"boot\":\"pv-clean-esp32\"}");
}

void loop() {
  static String buf;
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      buf.trim();
      if (buf.length()) handleLine(buf);
      buf = "";
    } else if (c != '\r') {
      buf += c;
      if (buf.length() > 512) buf = "";
    }
  }

  if (digitalRead(PIN_ESTOP_BTN) == LOW) enterFault("button");
  if (edgeUnsafe() && mode != Mode::Fault) enterFault("edge");

  if (mode == Mode::Fault) {
    motorsStop();
  } else if (mode == Mode::AutoRow) {
    // v0 zigzag placeholder: drive straight; turn logic comes with tuned sensors
    motorsWrite(cmdDrive, 0, cmdWipe);
  } else if (mode == Mode::Manual) {
    motorsWrite(cmdDrive, cmdTurn, cmdWipe);
  } else {
    motorsStop();
  }

  // Cooperative watchdog mark (enable Task WDT in production)
  if (millis() - lastWatchdog > 1000) lastWatchdog = millis();
  delay(1000 / LOOP_HZ);
}
