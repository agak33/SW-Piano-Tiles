#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>  // Required for 16 MHz Adafruit Trinket
#endif

#define LED_PIN   6
#define LED_COUNT 40

Adafruit_NeoPixel pixels(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

int l, r, g, b;

void setup() {
  Serial.begin(9600);
  pixels.begin();
  pixels.clear();
  pixels.setBrightness(10);
  pixels.show();
}

void loop() { 
  if(Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if(data[0] >= '0' && data[0] <= '9') {
      l = (data[0]-'0')*100+(data[1]-'0')*10+(data[2]-'0');
      r = (data[4]-'0')*100+(data[5]-'0')*10+(data[6]-'0');
      g = (data[8]-'0')*100+(data[9]-'0')*10+(data[10]-'0');
      b = (data[12]-'0')*100+(data[13]-'0')*10+(data[14]-'0');
      pixels.setPixelColor(l, pixels.Color(r, g, b));
      pixels.show();
    }
    else {
      pixels.fill((0, 0, 0), 0, pixels.numPixels());
      pixels.show();
    }
  }
}
