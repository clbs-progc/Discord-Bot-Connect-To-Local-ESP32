#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>

const char *ssid = " "; //REPLACE WITH LOCAL WIFI NAME
const char *password = " "; //REPLACE WITH LOCAL WIFI PASSWORD

bool light = false;
WebServer server(80);

// Set your Static IP address
IPAddress local_IP(192, 168, 0, 184);
// Set your Gateway IP address
IPAddress gateway(192, 168, 0, 1);

IPAddress subnet(255, 255, 0, 0);
IPAddress primaryDNS(8, 8, 8, 8); // optional
IPAddress secondaryDNS(8, 8, 4, 4); // optional

void handleRoot()
{
  server.send(200, "text/plain", "CONNECTED TO SERVER.");

}

void handleOn() {
  light = true;
  Serial.println("LIGHT ON");
  delay(80);

  // Send a quick response back so Python knows it worked
  server.send(200, "text/plain", "ON_OK");
}

void handleOff() {
  //digitalWrite(2, LOW); 
  light = false;
  //tft.fillScreen(0x0000);
  Serial.println("LIGHT OFF");

  // Send a quick response back so Python knows it worked
  server.send(200, "text/plain", "OFF_OK");
}

void setup() {

  Serial.begin(115200);  
  pinMode(2, OUTPUT);
  delay(1000);
  digitalWrite(2, LOW);
  // We start by connecting to a WiFi network
    // Configures static IP address
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    Serial.println("STA Failed to configure");
  }
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/on", HTTP_GET, handleOn);
  server.on("/off", HTTP_GET, handleOff);

  server.begin();
}

void loop() {
  server.handleClient();
  if(light == true)
  {
    digitalWrite(2, HIGH);
    delay(100);
    digitalWrite(2, LOW); 
    delay(100);
  }
  else
  {
    digitalWrite(2, LOW);
  }

}