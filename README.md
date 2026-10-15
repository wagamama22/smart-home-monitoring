# Automated Smart Home Monitoring System with Remote Access 
#### Intelligent IoT-Based Home Automation & Remote Monitoring Platform
#### Built as a hands-on embedded systems and software integration project.

A Raspberry Pi-based smart-home monitoring prototype that brings together environmental and light sensing, distance measurement, camera capture, on-device alerts, and a lightweight Flask dashboard.
This project is a practical example of connecting Python software to physical hardware: sensor readings are collected in background threads, shown on an LCD, made available over HTTP, and used to trigger camera and email workflows.
The project showcases my ability to:
•	Analyze real-world business and technical requirements
•	Design technology solutions for connected environments
•	Research and evaluate emerging technologies
•	Develop structured project documentation
•	Communicate technical concepts to both technical and non-technical stakeholders
•	Apply software engineering and problem-solving methodologies
•	Deliver end-to-end technology projects from concept to implementation

Project Objective
The main objective of this project was to investigate and design a smart home ecosystem capable of:
•	Monitoring home activity in real time
•	Providing remote access capabilities
•	Improving residential security
•	Increasing energy efficiency
•	Enhancing user comfort through automation
•	Enabling centralized control of connected devices
The project explores how modern IoT technologies can be integrated into everyday environments to create intelligent and scalable home automation solutions.

## Key Features

Sensor monitoring:  
Reads temperature and humidity from a DHT11, distance from an ultrasonic sensor, and light level through a photoresistor and I2C ADC.
Camera integration: 
Captures still images and records short video clips using Raspberry Pi Camera software.
Local feedback: 
Displays status and readings on an LCD1602 and drives LEDs and a buzzer.
Web access: 
Runs a Flask dashboard and exposes the latest sensor readings through HTTP endpoints.
Email notifications: 
Uses Yagmail to send sensor summaries and camera attachments to designated email address.
Concurrent workflows: 
Runs the sensor routines in daemon threads while the Flask server handles web requests.
Business Value
Smart Monitoring
•	Real-time home status monitoring
•	Connected sensor integration
•	Activity tracking and reporting
Remote Accessibility
•	Remote device visibility
•	Off-site monitoring capabilities
•	Secure access architecture considerations

Home Automation
•	Automated workflows
•	Device coordination
•	Event-driven actions
Security & Safety
•	Smart surveillance concepts
•	Automated alerts and notifications
•	Risk reduction through continuous monitoring
Energy Management
•	Energy consumption awareness
•	Smart resource utilization
•	Automation-driven efficiency improvements
## Tech Stack

Language : Python 
Framework/Web server : Flask 
Hardware I/O : GPIO Zero, I2C / SMBus, pigpio 
Camera : Picamera2 
Sensors and peripherals : DHT11, ultrasonic distance sensor, photoresistor with ADC, LCD1602, LEDs, buzzer 
Notifications : Yagmail 

## Engineering work demonstrated

- Integrating third-party libraries and hardware-specific drivers.
- Converting sensor output into readable values and exposing the latest state through HTTP.
- Coordinating sensor loops and a web server with Python threads and an event.
- Connecting physical feedback, camera capture, file storage, and email notifications into one workflow.
- Working with Linux device setup, GPIO pin mapping, I2C peripherals, and Raspberry Pi camera tooling.

## Getting started

### Prerequisites

- A Raspberry Pi running a compatible Raspberry Pi OS installation.
- The hardware listed above, wired to match the pin map.
- I2C enabled for the ADC module.
- A configured Raspberry Pi camera and Picamera2 installation.
- The pigpio daemon for the `PiGPIOFactory` distance sensor.
- Python dependencies compatible with the OS and Raspberry Pi hardware: `gpiozero`, `smbus`, `Flask`, `yagmail`, and Picamera2.
- The Freenove DHT native library (`/usr/lib/libdht.so`), which `Freenove_DHT.py` loads directly.

This repository does not currently include a dependency manifest. Install OS- and board-compatible packages using the Raspberry Pi OS package manager or an appropriately configured Python environment.

### Configure before running

`smart_home.py` currently contains machine-specific settings. Before starting the program:

1. Update the email sender and recipient settings and replace the hard-coded password-file location with a credential source appropriate for your setup. Do not commit passwords, app passwords, or other secrets.
2. Update `image_folder` and `video_folder` to writable directories on your Raspberry Pi.
3. Check the camera output location against the `/image` route, which currently serves `static/v_0.jpg`. The capture folder and route must refer to the same file if you want the dashboard image link to work.
4. Review the dashboard links: the HTML currently points to `0.0.0.0`. When browsing from another device, use the Raspberry Pi's LAN address instead.
5. Confirm the pin assignments and ADC address match your actual wiring and modules.

The application binds Flask to `0.0.0.0` on port `5000` and has no authentication. Use it only on a trusted local network; do not expose it directly to the public internet.

### Run

From the project directory on the Raspberry Pi:

```bash
python3 smart_home.py
```

The program initializes the display and ADC, starts the Flask server, and prompts in the terminal. Enter `1` to start the sensor routines and `0` to pause them. Press `Ctrl+C` to stop the program and run its cleanup handler.

Open the dashboard from a device on the same network:

```text
http://<raspberry-pi-ip>:5000/
```

The server listens on port `5000`; ensure the host firewall permits local access if needed.

## HTTP endpoints

| Route | Response |
| --- | --- |
| `/` | HTML dashboard |
| `/dht11` | Latest humidity and temperature values with a timestamp |
| `/photoresistor` | Latest ADC value and calculated voltage with a timestamp |
| `/ultrasonic` | Latest distance reading with a timestamp |

The sensor endpoints return plain-text responses. Sensor values are updated by the background routines after they are started from the terminal.

## Current scope

This is a hardware-dependent learning project rather than a production-ready home security system. The runtime paths, credentials, wiring, native DHT library, and camera setup need to be configured for each device. The dashboard is unauthenticated, and sensor readings and camera files are intended for local-network demonstration.

## Author

Morgan Chinedu Ofodum

Junior Software Developer 

### Areas of interest include:

•	Software Development

•	Front-End Engineering

•	Web Applications

•	JavaScript Development

•	Enterprise Software Solutions

•	Technology Consulting

I am actively seeking opportunities where I can contribute, learn from experienced teams, and continue developing into a high performing software professional.

### Career Objective

I am particularly interested in graduate and junior-level opportunities within innovative technology and consulting organisations.






