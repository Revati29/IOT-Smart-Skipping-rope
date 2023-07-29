#include <Arduino.h>

#include <WiFi.h>
#include <WiFiMulti.h>

#include <HTTPClient.h>

#include <WiFiClientSecure.h>


const char* ssid = "Revati's phone";
const char* password = "123456789@re";

// Replace with the IP address of your Flask server
const char* serverIP = "192.168.113.100";
const int serverPort = 5000;
long randNumber;
void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
}

void loop() {
  // Read accelerometer data and update these variables accordingly
  randNumber = random(300);
  Serial.println(randNumber);
  int jump_count =randNumber ;
  int set_count = 3;
  int set_duration = 3000;

  // Create JSON payload
  String payload = "{\"jump_count\":" + String(jump_count) + ", \"set_count\":" + String(set_count) + ", \"set_duration\":" + String(set_duration) + "}";

  // Send data to Flask web server
  sendToServer(payload);

  delay(5000); // Adjust the delay as per your requirements
}

void sendToServer(String payload) {
  WiFiClient client;

  if (client.connect(serverIP, serverPort)) {
    Serial.println("Connected to server");
    client.print("POST /data HTTP/1.1\r\n");
    client.print("Host: ");
    client.print(serverIP);
    client.print("\r\n");
    client.print("Content-Type: application/json\r\n");
    client.print("Content-Length: ");
    client.print(payload.length());
    client.print("\r\n");
    client.print("\r\n");
    client.print(payload);
    delay(100);

    // Read and print the response from the server
    while (client.available()) {
      char c = client.read();
      Serial.print(c);
    }
  } else {
    Serial.println("Connection failed");
  }

  client.stop();
}
