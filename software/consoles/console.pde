

#define INPUT_BUF_LEN 80
char input_buffer[INPUT_BUF_LEN];

void readCommands()
{
    while(Serial.available() > 0)
    {
        incoming_val = Serial.read();

        if (incoming_val != 13 && incoming_val != 10 ) 
        {
            input_buffer[bufferPointer++] = incoming_val;
        }

        if(bufferPointer >= INPUT_BUF_LEN)
        {
            //Serial.println("buffer overrun");
		    bufferPointer = 0;
            input_buffer[0] = 1;
            Serial.flush();
            memset(input_buffer,0,sizeof(input_buffer));
            return;
		}
    }
    parseCommand(input_buffer);
    memset(input_buffer, 0,s izeof(input_buffer));
}


void parseCommand(char *buffer)
{
    //Serial.println("got cmd ");
    //Serial.println(buffer);
    char *token;

    //parse tokens 
}

