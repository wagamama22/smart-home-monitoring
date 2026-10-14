import smbus
from flask import send_file
from gpiozero import Buzzer 
from time import sleep, strftime
from datetime import datetime
from LCD1602 import CharLCD1602
import os
os.system("sudo pigpiod")
from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
import time
from Freenove_DHT import DHT
from gpiozero import LED, PWMLED
from ADCDevice import *
import yagmail
from flask import Flask
import threading
from picamera2 import Picamera2


# Flask app initialization
app = Flask(__name__)

# Email configuration
my_email = 'raspb7813@gmail.com'  # Replace with your Gmail address
password = ''  # Replace with your Gmail App Password

with open("/home/morgan/Desktop/password", "r") as f:
    password = f.read().rstrip()

receiver_email = 'raspb7813@gmail.com'  # Recipient email

# Initialize yagmail
yag = yagmail.SMTP(my_email, password)

# LED pins declared
led1 = LED(19)

# Buzzer variable declared
buzzer = Buzzer(26)

#camera variable declared
pcamera = Picamera2()

#setup camera for snapping and video recording picture
camera_config = pcamera.create_preview_configuration()
pcamera.configure(camera_config)
video_config = pcamera.create_preview_configuration()
pcamera.configure(video_config)
pcamera.start()
time.sleep(2)



# Hygrothermograph variables declared
DHTPin = 12  # define the pin of DHT11

# Ultrasonic Ranging Module variables declared
trigPin = 23
echoPin = 24
my_factory = PiGPIOFactory() 
sensor = DistanceSensor(echo=echoPin, trigger=trigPin, max_distance=3, pin_factory=my_factory)

# Photoresistor and ADC variable declared
ledPin = 17  # define ledPin
led = PWMLED(ledPin)
adc = ADCDevice()  # Define an ADCDevice class object

# LCD variables declared
lcd1602 = CharLCD1602()

#initialize camera


# Global variables to store last sensor readings
last_distance = 0
last_adc_value = 0
last_voltage = 0
last_humidity = 0
last_temperature = 0
image_folder = "/home/morgan/Desktop/pratice folder/static/"
video_folder = "/home/morgan/camo/op/"
last_photo = 0



#image folder validation
if not os.path.exists(image_folder):
    os.mkdir(image_folder)

#video folder validation
if not os.path.exists(video_folder):
    os.mkdir(video_folder)    
    

# Events to control the threads
run_event = threading.Event()


def get_cpu_temp():  # get CPU temperature from file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format(float(cpu)/1000) + ' C '

def get_time_now():  # get system time
    return datetime.now().strftime('    %H:%M:%S')

def loop_lcd():
    lcd1602.init_lcd()
    lcd1602.clear()
    lcd1602.write(0, 0, 'Welcome To Smart')
    lcd1602.write(0, 1, 'Home System MCO')
    sleep(2)
    lcd1602.write(0, 0, 'CPU Temp: ' + get_cpu_temp())
    lcd1602.write(0, 1, 'Time: ' + get_time_now())
    sleep(2)
    print("LCD stopped")



def loop_ultra():
    global last_distance
    lcd1602.clear()
    count = 0
    while True:
        run_event.wait()  # Wait until the event is set
        print("Loop 1 running")
        time.sleep(1)
        Distance = sensor.distance * 100
        last_distance = Distance  # Update last distance
        takeimage()
        print('Distance: ', Distance, 'cm')
        buzzer.on()
        print("Motion detected, buzzer turned on >>>")
        time.sleep(0.1)
        lcd1602.write(0, 0, 'Motion Detected ')
        lcd1602.write(0, 1, 'Dist: ' '{:.2f} cm'.format(Distance))
        time.sleep(1)
        buzzer.off()
        print("buzzer turned off <<<")
        time.sleep(0.1)
        count += 1
        if count == 1:
            # Send email with the last distance reading
            subject = "Ultrasonic Sensor - Last Reading"
            body = f"Last Distance Reading: {last_distance:.2f} cm\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            yag.send(to=receiver_email, subject=subject, contents=body)
            print(f"Email sent with last distance: {last_distance:.2f} cm")
            break

def takeimage():
    global last_photo
    global last_distance
    count = 0
    while True:
        filename = f"v_{count}.jpg"
        filepath = os.path.join(image_folder, filename)
        pcamera.capture_file(filepath)
        last_photo = filepath
        print("new photo taken")
        count += 1
        time.sleep(0.1)
        if last_distance:
            # Send email with the last photo
            subject = "camera - last photo"
            body = f"Last photo: {last_photo}\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            yag.send(to=receiver_email, subject=subject, contents=body, attachments=last_photo)
            print("Email sent with last photo")
            break

def setup_adc():
    global adc
    if(adc.detectI2C(0x48)):  # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)):  # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
              "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
              "Program Exit. \n")
        exit(-1)

        
def loop_ADC():
    global last_adc_value, last_voltage
    lcd1602.clear()
    count = 0
    while True:
        run_event.wait()
        print("Loop 2 running")
        time.sleep(1)
        value = adc.analogRead(0)  # read the ADC value of channel 0
        led.value = 0  # Mapping to PWM duty cycle
        voltage = value / 255.0 * 3.3
        last_adc_value = value  # Update last ADC value
        last_voltage = voltage  # Update last voltage
        print('ADC Value : %d, Voltage : %.2f' % (value, voltage))
        lcd1602.write(0, 0, 'Light Detected ')
        lcd1602.write(0, 1, 'ADC: ' '{:.2f} '.format(value))
        if value < 170:
            led.off()
        elif value > 170:
            led.on()
            takevideo()
        else:
            led.off()
        time.sleep(1)
        count += 1
        if count == 5:
            # Send email with the last ADC and voltage readings
            subject = "Photoresistor - Last Reading"
            body = f"Last ADC Value: {last_adc_value}\nLast Voltage: {last_voltage:.2f} V\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            yag.send(to=receiver_email, subject=subject, contents=body)
            print(f"Email sent with last ADC: {last_adc_value}, Voltage: {last_voltage:.2f} V")
            break



def takevideo():
    global last_video
    global last_adc_value
    count = 0
    while True:
        filename = f"vv_{count}.mp4"
        filepath = os.path.join(video_folder, filename)
        pcamera.start_and_record_video(filepath, duration=10)
        last_video = filepath
        print("new video taken")
        count += 1
        time.sleep(0.1)
        if last_adc_value:
            # Send email with the last video
            subject = "camera - last video"
            body = f"Last photo: {last_video}\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            yag.send(to=receiver_email, subject=subject, contents=body, attachments=last_video)
            print(f"Email sent with last video {last_video}")
            break



def dHTLoop():
    global last_humidity, last_temperature
    dht = DHT(DHTPin)
    time.sleep(1) 
    counts = 0  # Measurement counts
    while True:
        run_event.wait()
        print("Loop 3 running")
        time.sleep(1)
        counts += 1
        lcd1602.clear()
        print("Measurement counts: ", counts)
        lcd1602.write(0, 0, 'DHT: ' '{:.2f} C'.format(counts))
        for i in range(0, 15):            
            chk = dht.readDHT11()  # read DHT11 and get a return value
            if chk == 0:  # data read is normal
                print("DHT11, OK!")
                break
            time.sleep(0.1)
        humidity = dht.getHumidity()
        temperature = dht.getTemperature()
        last_humidity = humidity  # Update last humidity
        last_temperature = temperature  # Update last temperature
        lcd1602.write(0, 1, 'TEMP: ' '{:.2f} C'.format(temperature))
        led1.on()
        print("LED is turned on showing temperature and humidity detected")
        sleep(1)
        led1.off()
        sleep(1)
        print("Humidity : %.2f, \t Temperature : %.2f \n" % (humidity, temperature))
        time.sleep(2)
        if counts == 5:
            # Send email with the last humidity and temperature readings
            subject = "DHT11 Sensor - Last Reading"
            body = f"Last Humidity: {last_humidity:.2f} %\nLast Temperature: {last_temperature:.2f} C\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            yag.send(to=receiver_email, subject=subject, contents=body)
            print(f"Email sent with last Humidity: {last_humidity:.2f} %, Temperature: {last_temperature:.2f} C")
            break
def main():
    # Thread creation
    thread1 = threading.Thread(target=loop_ultra, daemon=True)
    thread2 = threading.Thread(target=loop_ADC, daemon=True)
    thread3 = threading.Thread(target=dHTLoop, daemon=True)
    thread1.start()
    thread2.start()
    thread3.start()
    while True:
        user_input = input("Press 1 to start, 0 to stop: ")
        if user_input == '1':
            run_event.set()  # Start all loops
        elif user_input == '0':
            run_event.clear()  # Stop all loops
    
    
        
# Flask routes for sensor readings
@app.route('/')
def index():
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      background-color: white;
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
    }

    h2 {
      color: #333;
      margin: 40px 0 20px;
      text-align: center;
    }

    .button-container {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 20px;
      padding: 20px;
      max-width: 800px;
      width: 100%;
    }

    .dashboard-button {
      background-color: #007BFF;
      color: white;
      padding: 15px 30px;
      font-size: 16px;
      border: none;
      border-radius: 5px;
      text-decoration: none;
      display: inline-block;
      text-align: center;
      transition: background-color 0.3s ease;
      flex: 1 1 200px;
      max-width: 300px;
    }

    .dashboard-button:hover {
      background-color: #0056b3;
    }

    @media (max-width: 600px) {
      .dashboard-button {
        font-size: 14px;
        padding: 12px 20px;
      }
    }
  </style>
</head>
<body>

  <h2>Automated Smart Home Monitoring With Remote Access</h2>
  <h2>Dashboard</h2>
  <br>
 


  <div class="button-container">
    <a href="http://0.0.0.0:5000/dht11" class="dashboard-button">DHT11</a>
    <a href="http://0.0.0.0:5000/photoresistor" class="dashboard-button">Photoresistors</a>
    <a href="http://0.0.0.0:5000/ultrasonic" class="dashboard-button">Ultrasonic</a>
    <a href="http://0.0.0.0:5000/image" class="dashboard-button">Photo</a>
   

  </div>

</body>
</html>
"""
@app.route('/image')
def takeimage_file():
    return send_file('static/v_0.jpg', mimetype='image/jpeg')

@app.route('/ultrasonic')
def ultrasonic_reading():
    return f"Sensor: Ultrasonic\nLast Distance: {last_distance:.2f} cm\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@app.route('/photoresistor')
def photoresistor_reading():
    return f"Sensor: Photoresistor\nLast ADC Value: {last_adc_value}\nLast Voltage: {last_voltage:.2f} V\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@app.route('/dht11')
def dht11_reading():
    return f"Sensor: DHT11\nLast Humidity: {last_humidity:.2f} %\nLast Temperature: {last_temperature:.2f} C\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def destroy():
    lcd1602.clear()
    led.close()
    led1.close()
    adc.close()
    buzzer.close()
    yag.close()  # Close the yagmail connection
    pcamera.stop()


def run_flask():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    print('Program is starting ... ')
    loop_lcd()
    setup_adc()
    try:
        # Start Flask app in a separate thread to allow sensor loops to run concurrently
        flask_thread = threading.Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()
        main()
    except KeyboardInterrupt:
        destroy()
        sensor.close()
        os.system("sudo killall pigpiod")
        print("Ending program")




