#include<DHT.h>
#include<TimeLib.h>

#define DHTPIN 22
#define DHTTYPE DHT11
// Heater
const int heater = 24;
bool heater_state = false;
// Humidifier
const int humidifier = 23;
bool humidifier_state = false;
// Pumps
const int pump_1 = 9; // pot 1
const int pump_2 = 8; // pot 2
// Fans
const int fan_1 = 7; 
bool fan_1_state = false;
// Lights
const int led_1 = 5; // 100W
const int led_2 = 4; // 150W
bool led_1_state = false;
bool led_2_state = false;

DHT dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(9600);
    while (!Serial) {
        
    }
    dht.begin();
    pinMode(led_1, OUTPUT);
    pinMode(led_2, OUTPUT);
    pinMode(fan_1, OUTPUT);
    pinMode(heater, OUTPUT);
    pinMode(humidifier, OUTPUT);
    
    setTime(0, 0, 0, 0, 0, 2024);
    
    }


void reset() {
    digitalWrite(led_1, LOW);
    digitalWrite(led_2, LOW);
    digitalWrite(fan_1, LOW);
    digitalWrite(heater, LOW);
    digitalWrite(humidifier, LOW);

    led_1_state = false;
    led_2_state = false;
    fan_1_state = false;
    heater_state = false;
    humidifier_state = false;
    
    delay(5000);
}


void dayCycle(int temperature, int humidity) {
  
    digitalWrite(led_1, HIGH);
    led_1_state = true;

    
    // Regulate Temperature
    if (temperature < 20 && !heater_state) {
        digitalWrite(fan_1, LOW);
        fan_1_state = false;
        digitalWrite(heater, HIGH);
        heater_state = true;
    }
    else if (temperature > 20 && !fan_1_state) {
        digitalWrite(heater, LOW);
        heater_state = false;
        digitalWrite(fan_1, HIGH);
        fan_1_state = true;
    }
    int wait = 600;
    // Regulate Humidity
    switch(humidifier_state){
      case false:
        if (humidity < 60 && !humidifier_state) {
          digitalWrite(humidifier, HIGH);
          delay(wait);
          digitalWrite(humidifier, LOW);
          delay(wait);
          humidifier_state = true;
        }
        break;
      case true:
        if (humidity > 70 && humidifier_state) {
          digitalWrite(humidifier, HIGH);
          delay(wait);
          digitalWrite(humidifier, LOW);
          delay(wait);
          digitalWrite(humidifier, HIGH);
          delay(wait);
          digitalWrite(humidifier, LOW);
          delay(wait);
          humidifier_state = false;
          }
          break;
    }

    Serial.print("{\"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + ",");
    Serial.print("\"humidifier_state\": " + String(humidifier_state) + ", " + "\"led_1_state\": " + String(led_1_state) + ", ");
    Serial.println("\"led_2_state\": " + String(led_2_state) + ", " + "\"fan_1_state\": " + String(fan_1_state) + "}");

}

void nightCycle(int temperature, int humidity) {

    digitalWrite(led_1, LOW);
    led_1_state = false;

    // Regulate Temperature
    digitalWrite(heater, LOW);
    digitalWrite(fan_1, HIGH);


    // Regulate Humidity
    if (humidity < 60 && !humidifier_state) {
        digitalWrite(humidifier, HIGH);
        delay(600);
        digitalWrite(humidifier, LOW);
        delay(600);
        humidifier_state = true;
    } else if (humidity > 70 && humidifier_state) {
        digitalWrite(humidifier, HIGH);
        delay(600);
        digitalWrite(humidifier, LOW);
        delay(600);
        digitalWrite(humidifier, HIGH);
        delay(600);
        digitalWrite(humidifier, LOW);
        delay(600);
        humidifier_state = false;
    }
  
}

void debug() {
    if (fan_1_state == true && heater_state == true) {
        digitalWrite(heater, LOW);
        digitalWrite(fan_1, LOW);
        fan_1_state = false;
        heater_state = false;
    }
}


void loop() {
    delay(2000);
    
    int temperature = dht.readTemperature();
    int humidity = dht.readHumidity();


    int currentHour = hour();
    int currentMinute = minute();
    int currentSecond = second();
    int currentDay = day();
    int currentMonth = month();
    int currentYear = year();

    
    if (!isnan(temperature) && !isnan(humidity)) {
        
        Serial.print("{\"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + ",");
        Serial.print("\"day\": " + String(currentDay) + ", " + "\"hour\": " + String(currentHour) + ", " + "\"minute\": " + String(currentMinute) + ", ");
        Serial.print("\"humidifier_state\": " + String(humidifier_state) + ", " + "\"led_1_state\": " + String(led_1_state) + ", ");
        Serial.println("\"led_2_state\": " + String(led_2_state) + ", " + "\"fan_1_state\": " + String(fan_1_state) + "}");
        
        if (currentHour < 18) {
            dayCycle(temperature, humidity);
         
        } else if (currentHour > 18){
            nightCycle(temperature, humidity);
            }
            
        debug();    
        }

       
     else {
      Serial.println("Failed to read DHT data");
    }
}
