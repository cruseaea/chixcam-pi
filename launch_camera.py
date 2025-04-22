#!/usr/bin/env python3
import RPi.GPIO as GPIO
import os
import time
import logging

# Configuration
BUTTON_PIN = 17
LOG_FILE = "/home/cruse/camera_launcher.log"

def setup():
    """Initialize GPIO and logging"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=LOG_FILE
    )

def main():
    setup()
    logging.info("Camera launcher ready. Press GPIO17 button to start.")
    
    try:
        while True:
            GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
            logging.info("Button pressed - Launching chixcamPI.py")
            
            # Start main camera program
            os.system("python3 /home/cruse/chixcam-pi/chixcamPI.py")
            
            # Debounce delay
            time.sleep(2)
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        logging.info("Launcher stopped by user")

if __name__ == "__main__":
    main()
