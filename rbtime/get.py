# Fabio Eboli 01-2013
# functions useful for connecting to FE5680A
# usage:
# p=SetPort(portnumber)  note the in windows 0 is COM1, 1 is COM2 etc
# value=GetOffs(p)
# SetOffsRam(p,1000) 1000 is the new momentary offset
# SetOffsRelRam(p,-30) the new momentary offset s 30 units less than last one i.e. 970
# StoreOffsEE(p) stores the actual momentary offset into EEPROM
# SetOffsEE(p,500) 500 is the new offset, and is permanently saved into EEPROM
# ChangeFreqHz(p,1) move the output frequency 1Hz high
# ChangeFreqP(p,-2.5e-10) move the output frequency -2.5x10^-10
# SendCommandChar(p,0x22,'',True) check and print in readable format the result of 0x2D command

import serial
from struct import *
import time

lastcommandtime=0
resolution_parts_per_bit=6.80789e-13

# prepares the communication serial port to the FE5680A
# portno is the port number, in win 0 for COM1 etc
# returns the port that will be passed to the other functions
def SetPort(portno):
    global lastcommandtime
    port=serial.Serial(portno)
    print("Connected to "+port.name)
    port.baudrate=9600
    port.timeout=.1
    port.close()
    lastcommandtime=time.time()
    return port

# builds and sends a command to the FE5680A
# port : serial port returned by SetPort()
# ID : command code number
# Data : command data, string
# ReadBack : True if an answer from the FE5680A is expected
# Returns : [rtncode,rtndata,error]
# rtncode: -1 error in answer
#          0 no answer expected
#          1 correct answer received
# rtndata: payload data returned from FE5680A, binary string
# error: error description
def SendCommand(port,ID,Data,ReadBack):
    global lastcommandtime
    IDstring=pack('B',ID)
    datalen=len(Data)
    if datalen>128:
        return -1
    if len(Data)>0:
        totlen=datalen+5 # total message lenght ID+Lenght(2)+Checksum1+Data Lenght+Checksum2
    else:
        totlen=datalen+4
    totlenstr=pack('<H',totlen)
    cs1str=pack('B', (ID ^ (unpack('B',totlenstr[0])[0]) ^ (unpack('B',totlenstr[1])[0])))
    cs2=0
    for chars in Data:
        cs2 ^= unpack('B',chars)[0]
    cs2str=pack('B',cs2)

    timefromlastcommand=(time.time())-lastcommandtime
    while timefromlastcommand<2: #wait at least 2s between communications to FE5680A
        timefromlastcommand=(time.time())-lastcommandtime    
    port.open()
    port.write(IDstring+totlenstr+cs1str+Data+cs2str)
#    print(IDstring+totlenstr+cs1str+Data+cs2str)
    ret=[0,'','']
    if ReadBack==True:
        answer=port.readall()
#        answer=input("Answer? ")
        ansID=unpack('B',answer[0])[0]
        anslen=unpack('<H',answer[1:3])[0]
        anscs1=unpack('B',answer[3])[0]
        calccs2=0
        #check command code
        if ansID == ID:
            #check total lenght
            if len(answer) == anslen:
                #check command checksum
                calccs1=(unpack('B',answer[0])[0]) ^ (unpack('B',answer[1])[0]) ^ (unpack('B',answer[2])[0])
                if anscs1 == calccs1:
                    anscs2=unpack('B',answer[anslen-1])[0]
                    # calculate data checksum
                    for d in answer[4:anslen-1] :
                        calccs2^=unpack('B',d)[0]
                    #check data checksum
                    if anscs2 == calccs2 :
                        ret=[1,answer[4:anslen-1],"No Errors"]
                    else:
                        ret=[-1,answer[4:anslen-1],"Error: wrong data checksum"]
                else:
                    ret=[-1,answer[4:anslen-1],"Error: wrong command checksum"]
            else:
                ret=[-1,answer[4:anslen-1],"Error: wrong packet lenght"]
        else:
            ret=[-1,'',"Error: bad command code returned"]
    port.close()
    lastcommandtime=time.time()
    return  ret

# Same as SendCommand but returns the payload in readable string format
# and prints on stdout
def SendCommandChar(port,ID,Data,ReadBack):
    answer=SendCommand(port,ID,Dara,ReadBack)
#    answer=input("Answer? ")
    answerstring=''
    for i in answer[1]:
        answerstring+=(hex(unpack('B',i)[0]))+ "\r\n"
    print(str(len(answer[1]))+" Elements in answer")
    print(answerstring)
    return [answer[0],answerstring,answer[2]]


# Returns the Offset from the FE5680A         
def GetOffs(port):
    commandcode=0x2D
    data=''
    ret=SendCommand(port,commandcode,data,True)
    if ret[0]==1:
        return unpack('>i',ret[1])[0]
    else:
        print("Error code "+str(ret[0]))
        print(ret[2])
        return 0
    
# Sets the offset, without saving the value
def SetOffsRam(port,value):
    commandcode=0x2E
    data=pack('>i',value)
    return SendCommand(port,commandcode,data,False)[2]

# Sets the offset relative to the value stored in the FE5680A,
# without saving the value, useful for incremental changes
def SetOffsRelRam(port,value):
    refoffs=GetOffs(port)
    newoffs=refoffs+value
    return SetOffsRam(port,newoffs)

# Sets the offset, saving the value into the EEPROM of the FE5680A
def SetOffsEE(port,value):
    commandcode=0x2C
    data=pack('>i',value)
    return SendCommand(port,commandcode,data,False)

# Reads the offset from internal ram and Stores it to EEPROM
def StoreOffsEE(port):
    value=GetOffs(port)
    return SetOffsEE(port,value)

# Change the frequency output of valueHz Hz, not stored
def ChangeFreqHz(port,valueHz):
    Offs=int(float(valueHz)/(resolution_parts_per_bit*1e7))
    print("new offset: "+str(Offs))
    return SetOffsRelRam(port,Offs)

# Change the frequency output of valueP parts, not stored
def ChangeFreqP(port,valueP):
    Offs=int(float(valueP)/resolution_parts_per_bit)
    print("Offset: "+str(Offs))
    return SetOffsRelRam(port,Offs)
