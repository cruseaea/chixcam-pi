# Slim Shady Chicken Coop Security Camera System
** Last Updated: ** 4/26/25

## Overview
A motion-detection camera for monitoring wildlife near a chicken coop. When motion is detected, video clips are recorded and sent to specified email. Runs on a Raspberry Pi 4 along with a camera module and push-button.

--

## Features

## 1. Motion Detection & Recording
**Description:** Detects motion and records video clips. 

#### Functional Requirements  
- Continuously monitor camera feed using background subtraction.  
- Trigger recording when motion exceeds `min_movement_area`.  
- Temporarily saves videos and attach to email alerts.  

#### Non-Functional Requirements  
- Shall run headlessly on Raspberry Pi 4.  
- Auto-adjust sensitivity to reduce false positives.  

#### Acceptance Criteria  
- Motion triggers recording within 0.3 seconds.  
- Videos are 720p at 20 frames per second (FPS).  

---

### 2. Push-Button Activation  
**Description:** Manual control via button.  

#### Functional Requirements  
- Button (GPIO 17) starts the camera program.  
- Log all button presses to `camera_launcher.log`.

#### Non-Functional Requirements  
- Launcher script shall run at boot.

#### Acceptance Criteria  
- Button press launches chixcamPi.py within 1 second.  

---

### 3. Email Notifications  
**Description:** Sends alerts with video attachments.  

#### Functional Requirements  
- Shall use SMTP (Gmail) to send emails.  
- Compress videos >20MB before sending.  

#### Non-Functional Requirements  
- Credentials stored securely in `.env` file.  

#### Acceptance Criteria  
- Videos that >20MB are compressed.
- Test email successfully sent during intial setup.

---
