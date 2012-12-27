float temp[4] = {0.0 , 0.0 , 0.0 , 0.0};
float temp_calibrate[4] = {0.0 , 0.0 , 0.0 , 0.0};

void setup()
{
  Serial.begin(9600);
}

void print_temps()
{
  for(int i=0;i<3;i++){
    Serial.print(temp[i]);
    Serial.print(",");
  }
  Serial.print(temp[4]);
  Serial.println();
}

void loop()
{
  for(int i=0;i<4;i++){
    temp[i] = analogRead(i) * 0.004882812 * 100 - 273.15 + temp_calibrate[i];
  }  
  print_temps();
  delay(100); 
}

