float temp[4] = {0.0 , 0.0 , 0.0 , 0.0};
float temp_calibrate[4] = {0.0 , 0.0 , 0.0 , 0.0};

void setup()
{
  Serial.begin(9600);
  Serial.print("Starting Temperature Monitoring"); 
}

void print_temps()
{
  for(int i=0;i++;i<4){
    Serial.print(temp[i]);
    Serial.print(",");
  }
  Serial.println();
}

void loop()
{
  for(int i=0;i++;i<4){
    temp[i] = analogRead(i) * 0.004882812 * 100 - 273.15 + temp_calibrate[i];
  }  
  print_temps();
  delay(100); 
}

