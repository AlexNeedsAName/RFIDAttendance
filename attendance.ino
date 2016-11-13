#include <SoftwareSerial.h>
#include <SPI.h>

SoftwareSerial rSerial(8,9);

const int tagLen = 16;
const int idLen = 12;

String lastID = "123456789012";
int i = 0;

void setup()
{
    // Starts the hardware and software serial ports
    Serial.begin(9600);
    rSerial.begin(9600);
    Serial.println("Ready");
}

void loop()
{
   String id = scanTag();
   Serial.print("\nID: "); 
   Serial.println(id);
}

String scanTag()
{
    char tag[idLen];
    for (int c=0; c < idLen; c++) tag[c] = 0;

    while(true)
    {
        int i = 0;  
        if (rSerial.available() == tagLen)
        {
            while (rSerial.available() && i < idLen)
            {
                tag[i] = rSerial.read();
                if (tag[i] != 2 /* STX */ && tag[i]!= 13 /* CR */ && tag[i] != 10 /* LF */ && tag[i] != 3 /* ETX */) i++;
            }
        }
        if(tag[idLen-1] == 3) tag[idLen-1]=0; //Replace ETX with Null character to end the string
        if (!strlen(tag)== 0) return tag;
    }
}

