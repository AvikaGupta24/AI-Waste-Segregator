const int led6=6;    //white led
const int pLedPin = 7;    // green Positive LED pin
const int nLedPin = 8;    // Yellow LED 
const int ledPin = 9;     // red pin with buzzer 
const int cMoterPin=5;


void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(pLedPin, OUTPUT);
  pinMode(nLedPin, OUTPUT);
  Serial.begin(9600);
  pinMode(cMoterPin, OUTPUT);
}

void loop() {
 

      //2. conv belt on for 1 second
  digitalWrite(cMoterPin, HIGH);    // Turn on the positive LED
  Serial.print("Moter on pin 5");
  delay(5000);                   // Delay for 1 second
  digitalWrite(cMoterPin, LOW);     // Turn off the positive LED
  delay(100); 


 // 3.Turn on the positive LED pin7
  digitalWrite(pLedPin, HIGH);   // Turn on the positive LED
   Serial.print("positive Green LED pin7 ON");
  delay(1000);                   // Delay for 1 second
  digitalWrite(pLedPin, LOW);    // Turn off the positive LED
  delay(100);

// 4. Turn on the negative LED pin 8
  digitalWrite(nLedPin, HIGH);   // Turn on the negative LED
  Serial.print("Yellow LED pin8 ON");
  delay(1000);                   // Delay for 1 second
  digitalWrite(nLedPin, LOW);    // Turn off the negative LED

  delay(100);                   // Delay for 1 second before starting again

    //5. Toggle LEDs   pin 9 With Buzzer
  digitalWrite(ledPin, HIGH);    // Turn on the positive LED
   Serial.print("Red LED  pin9 ON");
  delay(1000);                   // Delay for 1 second
  digitalWrite(ledPin, LOW);     // Turn off the positive LED
  delay(100);                   // Delay for 1 second before starting again
  

    //5. Toggle LEDs   pin 6
  digitalWrite(led6, HIGH);    // Turn on the positive LED
   Serial.print("White led6 pin6 ON");
  delay(1000);                   // Delay for 1 second
  digitalWrite(led6, LOW);     // Turn off the positive LED
  delay(100); 
  
}