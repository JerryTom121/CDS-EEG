// THE ARDUINO CODE FOR EEG
#define ANALOG_IN 0
#define LED_PIN 13
#define HZ 1
#define SAMPLE_SIZE 10
char msg = '  ';   // variable to hold data from serial
float averageAmp = 0;
int avgIndex = 0;
long period = 0;
int max_val = 0;
int min_val = 1023;
int val = 0;
long previousMillis = 0;
boolean first_sample_set = true;
int interval;
int* amps;

void setup() {
  Serial.begin(9600); //was 19200
  pinMode(LED_PIN, OUTPUT);
  interval = 1000 / HZ;
  amps = new int[SAMPLE_SIZE];
}

void setLimits(int val){
  if (val > max_val){
    max_val = val;
  }
  if (val < min_val){
    min_val = val;
  } 
}

// output for processing
void outputToProcessing(int val){
  
  Serial.write( 0xff);
  Serial.write( (val >> 8) & 0xff);
  Serial.write( val & 0xff);
  
  //Serial.println(val);
}

boolean amplitudeDrop(int amp){
  return amp < averageAmp / 2;
}

void loop() {
  val = analogRead(ANALOG_IN);
  Serial.println(val);
  
  //outputToProcessing(val);
  
  // Delay
  unsigned long currentMillis = millis();
  if(currentMillis - previousMillis > interval) {
    previousMillis = currentMillis;
  } 
}
