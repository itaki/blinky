import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
#https://forums.raspberrypi.com/viewtopic.php?f=63&t=221972&hilit=acs712&start=150#p1366441

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)


displayCurrent=0.0
WriteCount=0
ad = ADS.ADS1115(i2c)


#resistor divider and ACS712 Voltage offset and slope

ratioACS712_20A =  9880.0/(9880+4750) 
ratioACS712_5A =  9880.0/(9880+4750)
ratioVCC =  4750.0/(4750+9880)
ACS712_20A_slope = 0.100
ACS712_5A_slope = 0.185
ACS712_20A_Voffset = 2.5
ACS712_5A_Voffset = 2.5


#manual adjustment to zero 0A
ACS712_5A_Ioffset =0.072
ACS712_20A_Ioffset =0.154


##########  kbhit function

import sys, termios, atexit
from select import select

# save the terminal settings
fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)

# new terminal setting unbuffered
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)

# switch to normal terminal
def set_normal_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

# switch to unbuffered terminal
def set_curses_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

def putch(ch):
    sys.stdout.write(ch)

def getch():
    return sys.stdin.read(1)

def getche():
    ch = getch()
    putch(ch)
    return ch

def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr != []

##### END OF  kbhit function


def readA2D( channel):

   value=0.0;
   count=1
   for i in range(count):
     value = value + ad.readSingle(channel)
   value = value / float(count)
#   print("A2D({}):{}".format(channel,value))
   return value


def getACS712_20A():
  return readA2D(3) / ratioACS712_20A

def getACS712_5A():
  return readA2D(4)/  ratioACS712_5A

def getVCC():
  return readA2D(2)/  ratioVCC

def getResistorVoltage():
  return  readA2D(1)


def writeInfo(displayCurrent,data):
  data.append(float(displayCurrent))
  file = open("currentData.txt","a")
  file.write("{:5.2f}\t{:7.3f}\t{:7.3f}\t{:7.3f}\t{:7.3f}\n".format(*data))
  file.close()


atexit.register(set_normal_term)
set_curses_term()


try:

 while True:

  info=[]
  #ok get VCC
  VCC = getVCC()
  info.append(VCC)

  #read Resistor current
  Vres = getResistorVoltage()
  Ires = Vres / 0.1

  info.append(Ires)

  #read ACS712_20A
  V20A = getACS712_20A()
  #normalize to 5V
  V20A = V20A *  5.0 / VCC
  #print("V30A {}".format(V20A))
  I20A = (V20A - ACS712_20A_Voffset) / ACS712_20A_slope  - ACS712_20A_Ioffset
  info.append(I20A)

  #read ACS712_5A
  V5A = getACS712_5A()
  #normalize to 5V
  V5A = V5A * 5.0 / VCC
  #print("V5A {}".format(V5A))

  I5A =  (V5A - ACS712_5A_Voffset) / ACS712_5A_slope - ACS712_5A_Ioffset
  info.append(I5A)

  

  if kbhit():
   getch()
   set_normal_term()
   displayCurrent=input("Display current: ")
   writeInfo(displayCurrent,info)
   set_curses_term()
   WriteCount=4
  else:
   if WriteCount > 0:
     writeInfo(displayCurrent,info)
     WriteCount=WriteCount - 1

  #display info
  print("VCC:{:5.2f}V Res:{:7.3f}A ACS712-20:{:+7.3f}A ACS712-5:{:7.3f}A".format(*info))
  time.sleep(0.01)

except KeyboardInterrupt:
  pass