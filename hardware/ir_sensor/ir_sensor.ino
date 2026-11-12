const int irPin = 2;  // IR sensor pin
const int LedWhitePin=6;    // Non Object decteted out of class probablity
const int LedGreenPin=7; // green led  Recyclable
const int LedYellowPin=8;   // Yellow led when Non-Recyclable
const int ledRedBuzzerPin = 9;  // LED pin RED Buzzer
 
const int cMoterPin=5;
bool dataReceived = false;
bool previous_state = false;
bool current_state = false;

// this setup of hardware pin mode
void setup() {
  pinMode(irPin, INPUT);
  pinMode(cMoterPin, OUTPUT);
  pinMode(LedWhitePin, OUTPUT); 
  pinMode(LedGreenPin, OUTPUT); 
  pinMode(LedYellowPin, OUTPUT);  
  pinMode(ledRedBuzzerPin, OUTPUT);

  Serial.begin(9600);
  //initial conveyor belt started
  digitalWrite(cMoterPin, HIGH); 
}

void loop() {
  // Check if IR sensor detects an object
  if (digitalRead(irPin) == HIGH) {
    // Send serial data "1" to indicate object detection on the laptop
    Serial.println("1");     
    digitalWrite(cMoterPin, LOW);  // Turn off conveyor belt
    // Wait until serial data "0" is received
    while (!dataReceived) {
      if (Serial.available() > 0) {
        char receivedData = Serial.read();
        if (receivedData == '1') {
          dataReceived = true;
          digitalWrite(LedGreenPin, HIGH);  // Turn on  GREEN LED  Object is Recyclable
		  digitalWrite(LedYellowPin, LOW);
		  digitalWrite(LedWhitePin, LOW);
		  digitalWrite(ledRedBuzzerPin, LOW);		   
          digitalWrite(cMoterPin, HIGH);  // Turn on conv. belt
          delay(9000);
		  // for new object dection status clear
		  digitalWrite(LedGreenPin, LOW);  
		  digitalWrite(LedYellowPin, LOW);
		  digitalWrite(LedWhitePin, LOW);
		  digitalWrite(ledRedBuzzerPin, LOW);
        }
		// here receive cmd object is  Non Bio-Degradable
		else if(receivedData == '2') 
		{
		  dataReceived = true;
          digitalWrite(LedGreenPin, LOW);  // Turn on  GREEN LED  Object is Non-Recyclable
		  digitalWrite(LedYellowPin, HIGH);
		  digitalWrite(LedWhitePin, LOW);
		  digitalWrite(ledRedBuzzerPin, LOW);		   
          digitalWrite(cMoterPin, HIGH);  // Turn on conv. belt
          delay(9000);
		  // for new object dection status clear
		  digitalWrite(LedGreenPin, LOW);  
		  digitalWrite(LedYellowPin, LOW);
		  digitalWrite(LedWhitePin, LOW);
		  digitalWrite(ledRedBuzzerPin, LOW);		
			
		}
		else if(receivedData == '3') 
		{
		  dataReceived = true;
          digitalWrite(LedGreenPin, LOW);  // Turn on  GREEN LED  Object is Recyclable
		  digitalWrite(LedYellowPin, LOW);
		  digitalWrite(LedWhitePin, HIGH);
		  digitalWrite(ledRedBuzzerPin, HIGH);		   
          digitalWrite(cMoterPin, HIGH);  // Turn on conv. belt
          delay(9000);
		  // for new object dection status clear
		  digitalWrite(LedGreenPin, LOW);  
		  digitalWrite(LedYellowPin, LOW);
		  digitalWrite(LedWhitePin, LOW);
		  digitalWrite(ledRedBuzzerPin, LOW);		
			
		}
      }
    }
    
    dataReceived = false;  // Reset the flag for next detection
  }
 
}
