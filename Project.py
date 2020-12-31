import RPi.GPIO as GPIO 
import time
import spidev 
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

left_right_motor_pin = 7
up_down_motor_pin = 26
    
GPIO.setwarnings(False)        
GPIO.setmode(GPIO.BCM)

GPIO.setup(left_right_motor_pin,GPIO.OUT)
GPIO.setup(up_down_motor_pin,GPIO.OUT)

left_right_servo = GPIO.PWM(left_right_motor_pin,50)
up_down_servo = GPIO.PWM(up_down_motor_pin,50)

left_right_servo.start(7.5)
up_down_servo.start(7.5)

##################################
# joystick and SPI

sw_channel = 0 
vry_channel = 1 
vrx_channel = 2

spi = spidev.SpiDev()      
spi.open(0,0)                     
spi.max_speed_hz = 100000

def readadc(adcnum):     
	if adcnum > 7 or adcnum < 0: 
			return -1
	r= spi.xfer2([1,8 + adcnum << 4, 0])
	data = ((r[1] & 3) << 8) + r[2] 
	return data
###############################################

x_angle = 7.5
y_angle = 7.5  

with canvas(device) as draw:
			draw.rectangle(device.bounding_box, outline="white", fill="black")
			draw.text((20, 20), "Game Start!!", fill="white")

try:
	while 1:
		vrx_pos = readadc(vrx_channel)
		vry_pos = readadc(vry_channel)
		sw_val = readadc(sw_channel)
		print("X:{} Y: {} SW: {}" .format(vrx_pos, vry_pos, sw_val))
		if vrx_pos < 10 and x_angle > 5.5:
			x_angle = x_angle - 0.008
			left_right_servo.ChangeDutyCycle(x_angle)
		elif vrx_pos > 1000 and x_angle < 10.5:
			x_angle = x_angle + 0.008
			left_right_servo.ChangeDutyCycle(x_angle)
		elif vry_pos < 10 and y_angle > 5.5:
			y_angle = y_angle - 0.008
			up_down_servo.ChangeDutyCycle(y_angle)
		elif vry_pos > 1000  and y_angle < 10.5:
			y_angle = y_angle + 0.008
			up_down_servo.ChangeDutyCycle(y_angle)	
		else:
			time.sleep(0.12)
	

except KeyboardInterrupt:
	left_right_servo.stop()
	up_down_servo.stop()
	GPIO.cleanup()
