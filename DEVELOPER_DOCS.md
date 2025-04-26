# Slim Shady Chicken Coop Security Camera - Developer Documentation

## 🛠️ Core Components
| File               | Purpose                                | Key Technologies Used       |
|--------------------|----------------------------------------|-----------------------------|
| `chixcamPI.py`     | Main RPi program (headless)            | OpenCV, Picamera2, SMTP     |
| `chixcamPC.py`     | PC test version (GUI)                  | OpenCV, Webcam              |
| `launch_camera.py` | GPIO button controller                 | RPi.GPIO                    |

---

## 🚀 Setup for Development
1. **Clone the repo**:
   ```bash
   git clone https://github.com/cruseaea/chixcam-pi.git
   cd chixcam-pi
   pip install opencv-python python-dotenv smtplib picamera2
