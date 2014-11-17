// THE ARDUINO CODE FOR EEG
#define ANALOG_IN 0
#define LED_PIN 13
#define MEMORY_SIZE 30
#define OUTPUT_INTERVAL 0
int* memory;
int val, sumOfMemory, currentElemI;
unsigned long currentMillis, previousMillis;

void setup() {
  Serial.begin(9600); //was 19200
  pinMode(LED_PIN, OUTPUT);
  memory = new int[MEMORY_SIZE];
  int i;
  for (i = 0; i < MEMORY_SIZE; i++){
    memory[i] = 0;
  }
  currentElemI = 0;
  sumOfMemory = 0;
  previousMillis = millis();
}

int average(int new_val){
  if (currentElemI >= MEMORY_SIZE){
    currentElemI = 0;
  }

  sumOfMemory -= memory[currentElemI];
  memory[currentElemI] = new_val;
  sumOfMemory += memory[currentElemI];
  
  currentElemI++;
}

void loop() {
  val = analogRead(ANALOG_IN);
  average(val);
   
  // Delay
  currentMillis = millis();
  if(currentMillis - previousMillis > OUTPUT_INTERVAL) {
    Serial.println(sumOfMemory/MEMORY_SIZE);
    previousMillis = currentMillis;
  }
}
