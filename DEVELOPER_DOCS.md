# Slim Shady Chicken Coop Security Camera - Developer Documentation

## Core Components

| File               | Purpose                          | Key Technologies       |
|--------------------|----------------------------------|------------------------|
| `chixcamPI.py`     | Main RPi program (headless)      | OpenCV, Picamera2, SMTP|
| `chixcamPC.py`     | PC test version (GUI)            | OpenCV, Webcam         |
| `launch_camera.py` | GPIO button controller           | RPi.GPIO               |

## Architecture Overview  
**Design Principle**:  
*"Keep hardware-specific code isolated (launch_camera.py) and business logic centralized (chixcamPI.py)."*  

**Key Constraints**:  
- Must work headless on Raspberry Pi OS  
- Gmail attachment limit: 25MB  
- Max camera resolution: 1280×720  

## Hardware Requirements

| Component          | Specification                   | Connection            |
|--------------------|---------------------------------|-----------------------|
| Raspberry Pi       | Model 4B (2GB+ RAM)             | N/A                   |
| Camera Module      | Official Pi Camera v2           | CSI Port              |
| Push Button        | Momentary SPST                  | GPIO17 + Ground       |

## Key Configuration

| Variable           | File             | Default Value        |
|--------------------|-----------------|----------------------|
| `MIN_MOTION_AREA`  | `chixcamPI.py`  | 500 pixels           |
| `EMAIL_COOLDOWN`   | `chixcamPI.py`  | 20 seconds           |
| `RECORD_DURATION`  | `chixcamPI.py`  | 30 seconds           |

## 🔧 Critical Functions  
| Function           | File             | Parameters           | Notes                  |  
|--------------------|-----------------|----------------------|------------------------|  
| `detect_motion()`  | `chixcamPI.py`  | `frame`, `min_area`  | Uses MOG2 background subtraction |  
| `send_email()`     | `chixcamPI.py`  | `video_path`         | Auto-compresses >20MB files |  

## Onboarding Checklist  
1. **Hardware Setup**:  
   - [ ] Connect camera to CSI port  
   - [ ] Wire button to GPIO17  

## Development Quickstart

| Step               | Command                          |
|--------------------|----------------------------------|
| Install            | `pip install -r requirements.txt` |
| Test (PC)         | `python chixcamPC.py`            |
| Deploy (RPi)      | `python chixcamPI.py`            |

## Troubleshooting

| Symptom            | Likely Fix                       |
|--------------------|----------------------------------|
| Camera not found   | Run `sudo raspi-config`          |
| SMTP auth errors   | Verify Gmail App Password        |
| False positives    | Increase `MIN_MOTION_AREA`       |


