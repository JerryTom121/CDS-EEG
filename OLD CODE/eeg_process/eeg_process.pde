// SET FOR 5 SECONDS EEG, 180 Hz.  A LONGER DISPLAY MAY RUN SLOW,
// DEPENDING ON THE SPEED OF YOUR CPU.

import processing.serial.*;

Serial port;      // Create object from Serial class
int val;              // Data received from the serial port
int amp;              // Amplitude received from serial port
int cnt;
int hht;
int wm1;
int[] values;
int fraction;
int hz = 1;

void setup() 
{
  fraction = 2;
  size(900, 900);                                  //currently set to 5 sec
  // Open the port that the board is connected to and use the same speed (19200 bps)
  port = new Serial(this, Serial.list()[0], 9600);
  values = new int[width];  
  hht = 450*fraction + 1024/2;     // Sets display DC offset; must adjust if gain is changed# 
  wm1= width-1; 
  cnt = 1;     
  frameRate(180);                                //read/draw 180 samples/sec
  for (int s=0;s<width;s++) {                 //set initial values to midrange
    values[s] = 550;
  }
}

void draw()
{

  background(0);  
   
      while (port.available() >= 3) {                  //read the latest value
        if (port.read() == 0xff) {
          val = (port.read() << 8) | (port.read());
        }  
        /*
        String data = port.readString();
        if (data.contains("AMP=")) {
          amp = int(data.substring(4));
        } else {
          val = int(data);
        }
        */
      }
        
        
        values[cnt] = val;                              //put it in the array#
        cnt++;                                                 //increment the count
  
        stroke(60);
        for (int d = 0; d < width-1; d = d + 180) {   //**draw lines for seconds
          line(d,0,d,400);
        }
        
        stroke(255,255,0);
        line(cnt,100,cnt,300);                      //draw the leading edge line
        stroke(255,0,0);
  
        for (int x=2; x<wm1; x++) {
          line (x-1,  (hht-values[x-1])/fraction, x, (hht-values[x])/fraction);    //increment the data line
          //println(str(values[x]));
        }
              
        if (cnt > wm1) {                                //back to beginning
          cnt = 1;
        }
        
   /*unsigned long currentMillis = millis();
 
 
   println(values[wml-1]);
  if(currentMillis - previousMillis > interval) {
    // save the last time you blinked the LED 
    previousMillis = currentMillis;
    
    int amp = max_val - min_val;
    Serial.println("AMP="+String(amp));
    
    max_val = 0;
    min_val = 1023;
  }

  
  setLimits(val);  
   */
 }
