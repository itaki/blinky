import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
ledPin12 = 12
buttonPin16 = 16
GPIO.setup(ledPin12, GPIO.OUT)
GPIO.setup(buttonPin16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
  buttonState = GPIO.input(buttonPin16)
  if buttonState == False:
    GPIO.output(ledPin12, GPIO.HIGH)
  else:
    GPIO.output(ledPin12, GPIO.LOW)