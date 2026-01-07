int motor1pin1 = 26;
int motor1pin2 = 28;

int motor2pin1 = 30;
int motor2pin2 = 32;

// Enable pins (PWM)
int ENA = 3;
int ENB = 4;

char command;

void setup() {
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);

  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  analogWrite(ENA, 150);   // speed
  analogWrite(ENB, 150);

  Serial.begin(9600);
  Serial.println("Use W A S D keys");
}

void stopMotors() {
  Serial.println("Stop");
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, LOW);
}

void forward() {
  Serial.println("forward");
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW)d;

  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);
}

void backward() {
  Serial.println("backward");
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);

  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);
}

void left() {
  Serial.println("left");
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, LOW);   // left motor stop

  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);   // right motor forward
}

void right() {
  Serial.println("right");
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);   // left motor forward

  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, LOW);   // right motor stop
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.read();
    delay(1000);
    switch (command) {
      case 'w':
      case 'W':
        forward();
        break;

      case 's':
      case 'S':
        backward();
        break;

      case 'a':
      case 'A':
        left();
        break;

      case 'd':
      case 'D':
        right();
        break;

      default:
        stopMotors();
        break;

      
    }
  }
}
