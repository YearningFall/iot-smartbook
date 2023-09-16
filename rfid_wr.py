import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import sys
print
continue_reading = True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Crtl+C captured, ending read")
    continue_reading = False
    GPIO.cleanup()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Hook the SIGINT 
signal.signal(signal.SIGINT, end_read)

GPIO.setmode(GPIO.BOARD)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print ("Welcome to the MFRC data write")
print ("Press Crtl+C to stop")

while continue_reading :

    (status, uid) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        print ("Card detected")

        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:
            print ("Card read UID : ", uid[0], ":", uid[1], ":", uid[2], ":", uid[3])

            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

            MIFAREReader.MFRC522_SelectTag(uid)

            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

            if status == MIFAREReader.MI_OK:
                
                print("Enter the character : ")
                indata = input()
                input1 = indata.ljust(16)
                print(input1)
                input2 = "SmartBook       "
                datachar = bytes(input1,'ascii')
                datalast = bytes(input2,'ascii')

                print ("Sector 8 & 9 looked like this : ")

                input1 = MIFAREReader.MFRC522_Readdata(8)
                input2 = MIFAREReader.MFRC522_Readdata(9)
                input1 = "".join(map(chr, input1))
                input2 = "".join(map(chr, input2))

                print (input1+input2+"\n")

                print ("Write Sector 8 & 9 : ")

                MIFAREReader.MFRC522_Write(8, datachar)
                MIFAREReader.MFRC522_Write(9, datalast)

                print ("Now look like this : ")

                input1 = MIFAREReader.MFRC522_Readdata(8)
                input2 = MIFAREReader.MFRC522_Readdata(9)
                input1 = "".join(map(chr, input1))
                input2 = "".join(map(chr, input2))

                print (input1+input2+"\n")

                MIFAREReader.MFRC522_StopCrypto1()
                
                continue_reading = False
            
            else: 

                print ("Authenticating error")