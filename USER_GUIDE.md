# Slim Shady Chicken Coop Security Camera - User Guide

## Overview
This system detects motion near your chicken coop, records video clips, and sends email alerts. It runs on a **Raspberry Pi 4** with a camera module and a push button.

---

## Hardware Setup
1. **Raspberry Pi 4** with Raspberry Pi Camera Module v2/3 connected.
2. **Push Button** wired to GPIO Pin 17 (with ground).
3. **Power Supply**: Ensure stable power (5V/3A recommended).

---

## Software Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/cruseaea/chixcam-pi.git
   cd chixcam-pi

---

## Install Dependencies
1. pip3 install opencv-python python-dotenv smtplib

---

## Configure Email Credentials
1. Edit .env with your Gmail credentials: SENDER_EMAIL="your@gmail.com" RECEIVER_EMAIL="recipient@email.com" EMAIL_PASSWORD="your_app_password"

---
