#define RIGHT_FORWARD_PIN 5
#define RIGHT_BACKWARD_PIN 4
#define LEFT_FORWARD_PIN 6
#define LEFT_BACKWARD_PIN 7

unsigned long lastCommandTime = 0;
const unsigned long COMMAND_TIMEOUT = 200;

void setup() {
  pinMode(RIGHT_FORWARD_PIN, OUTPUT);
  pinMode(RIGHT_BACKWARD_PIN, OUTPUT);
  pinMode(LEFT_FORWARD_PIN, OUTPUT);
  pinMode(LEFT_BACKWARD_PIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Ready for WASD control!");
}

void loop() {
  // Check if a command is available from the serial buffer
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    handleCommand(cmd);
    lastCommandTime = millis(); // Reset the timeout timer on each command
  }

  // If no command has been received for a while, stop the motors
  if (millis() - lastCommandTime > COMMAND_TIMEOUT) {
    stopMotors();
  }
}

void handleCommand(char cmd) {
  switch(tolower(cmd)) {
    case 'w': moveForward(255); break;
    case 's': moveBackward(255); break;
    case 'a': turnLeft(255); break;
    case 'd': turnRight(255); break;
    case 'q': moveForwardLeft(255); break;  // diagonal forward-left
    case 'e': moveForwardRight(255); break; // diagonal forward-right
    case 'z': moveBackwardLeft(255); break; // diagonal backward-left
    case 'c': moveBackwardRight(255); break; // diagonal backward-right
    default: stopMotors(); break;
  }
}

void moveForward(int speed) {
  analogWrite(RIGHT_FORWARD_PIN, speed);
  digitalWrite(RIGHT_BACKWARD_PIN, LOW);
  analogWrite(LEFT_FORWARD_PIN, speed);
  digitalWrite(LEFT_BACKWARD_PIN, LOW);
}

void moveBackward(int speed) {
  digitalWrite(RIGHT_FORWARD_PIN, LOW);
  analogWrite(RIGHT_BACKWARD_PIN, speed);
  digitalWrite(LEFT_FORWARD_PIN, LOW);
  analogWrite(LEFT_BACKWARD_PIN, speed);
}

void turnLeft(int speed) {
  analogWrite(RIGHT_FORWARD_PIN, speed);
  digitalWrite(RIGHT_BACKWARD_PIN, LOW);
  digitalWrite(LEFT_FORWARD_PIN, LOW);
  analogWrite(LEFT_BACKWARD_PIN, speed);
}

void turnRight(int speed) {
  digitalWrite(RIGHT_FORWARD_PIN, LOW);
  analogWrite(RIGHT_BACKWARD_PIN, speed);
  analogWrite(LEFT_FORWARD_PIN, speed);
  digitalWrite(LEFT_BACKWARD_PIN, LOW);
}

void moveForwardLeft(int speed) {
  analogWrite(RIGHT_FORWARD_PIN, speed);
  digitalWrite(RIGHT_BACKWARD_PIN, LOW);
  analogWrite(LEFT_FORWARD_PIN, speed/2);
  digitalWrite(LEFT_BACKWARD_PIN, LOW);
}

void moveForwardRight(int speed) {
  analogWrite(RIGHT_FORWARD_PIN, speed/2);
  digitalWrite(RIGHT_BACKWARD_PIN, LOW);
  analogWrite(LEFT_FORWARD_PIN, speed);
  digitalWrite(LEFT_BACKWARD_PIN, LOW);
}

void moveBackwardLeft(int speed) {
  digitalWrite(RIGHT_FORWARD_PIN, LOW);
  analogWrite(RIGHT_BACKWARD_PIN, speed/2);
  digitalWrite(LEFT_FORWARD_PIN, LOW);
  analogWrite(LEFT_BACKWARD_PIN, speed);
}

void moveBackwardRight(int speed) {
  digitalWrite(RIGHT_FORWARD_PIN, LOW);
  analogWrite(RIGHT_BACKWARD_PIN, speed);
  digitalWrite(LEFT_FORWARD_PIN, LOW);
  analogWrite(LEFT_BACKWARD_PIN, speed/2);
}

void stopMotors() {
  analogWrite(RIGHT_FORWARD_PIN, 0);
  analogWrite(RIGHT_BACKWARD_PIN, 0);
  analogWrite(LEFT_FORWARD_PIN, 0);
  analogWrite(LEFT_BACKWARD_PIN, 0);
}
