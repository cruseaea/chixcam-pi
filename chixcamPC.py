import cv2
import time
import smtplib
import os
import tempfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent / "chixcred.env"
if not env_path.exists():
    raise FileNotFoundError(f"Env file not found at {env_path}")
load_dotenv(env_path)

# Get email credentials
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
password = os.getenv("EMAIL_PASSWORD")

# Verify variables
required_vars = ["SENDER_EMAIL", "RECEIVER_EMAIL", "EMAIL_PASSWORD"]
missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    raise ValueError(f"Missing environment variables: {missing}")

# Webcam initialization
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open video device")

# Video settings
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 20

# Background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2(
    history=50,
    varThreshold=5,
    detectShadows=False
)

# Motion detection settings
min_movement_area = 500
max_movement_area = 5000
motion_duration_threshold = 0.3  # Seconds of motion required to start recording
email_cooldown = 20  # Minimum seconds between emails

# Recording settings
record_duration = 30  # Maximum recording duration (seconds)
no_motion_threshold = 5  # Stop recording after this many seconds without motion
motion_display_duration = 1.0  # How long to show "MOTION" indicator

# State variables
video_writer = None
recording_start_time = None
is_recording = False
motion_start_time = None
last_motion_time = None
last_email_time = 0

def safe_show_window(name, img):
    """Safely show a window and handle any OpenCV errors"""
    try:
        cv2.imshow(name, img)
    except Exception as e:
        print(f"Window error {name}: {str(e)}")

def start_recording():
    """Initialize video writer for recording"""
    global video_writer, recording_start_time, is_recording, last_motion_time, recorded_filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    temp_dir = tempfile.gettempdir()
    video_filename = os.path.join(temp_dir, f"motion_{timestamp}.mp4")
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))
    if not video_writer.isOpened():
        raise RuntimeError("Failed to initialize video writer")
    
    recording_start_time = time.time()
    last_motion_time = time.time()
    is_recording = True
    recorded_filename = video_filename  # Make sure this gets passed to `send_email`
    print(f"Started recording: {video_filename}")
    return video_filename

def stop_recording():
    """Finalize video recording"""
    global video_writer, is_recording
    if video_writer is not None:
        video_writer.release()
        video_writer = None
    is_recording = False
    print("Stopped recording")

def send_email(video_path):
    """Send an email with the attached video"""
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return
        
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Security Alert: Motion Detected"

        body = f"""Motion detected in your security camera.
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Video attachment contains the recording."""
        msg.attach(MIMEText(body, "plain"))

        with open(video_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(video_path)}")
        msg.attach(part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
        print(f"Email sent with {video_path}")
        
    except Exception as e:
        print(f"Email error: {str(e)}")
    finally:
        try:
            os.remove(video_path)
        except:
            pass

try:
    recorded_filename = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame capture failed - retrying...")
            time.sleep(0.1)
            cap = cv2.VideoCapture(0)
            continue

        current_time = time.time()

        # Motion detection (always performed)
        fgmask = fgbg.apply(frame)
        _, thresh = cv2.threshold(fgmask, 245, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_detected = any(
            min_movement_area <= cv2.contourArea(c) <= max_movement_area 
            for c in contours
        )

        if is_recording:
            # Write frame to video
            video_writer.write(frame)
            
            # Update motion time if detected
            if motion_detected:
                last_motion_time = current_time
                
            # Visual feedback for motion
            if motion_detected or (last_motion_time and (current_time - last_motion_time) < motion_display_duration):
                cv2.putText(frame, "MOTION DETECTED", (20, 50), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Stop conditions (no motion for threshold OR max duration reached)
            no_motion_time = current_time - last_motion_time if last_motion_time else 0
            recording_time = current_time - recording_start_time
            
            if no_motion_time >= no_motion_threshold or recording_time >= record_duration:
                stop_recording()
                if current_time - last_email_time >= email_cooldown:
                    send_email(recorded_filename)
                    last_email_time = current_time
                continue

        else:  # Not recording
            if motion_detected:
                if motion_start_time is None:
                    motion_start_time = current_time
                elif current_time - motion_start_time >= motion_duration_threshold:
                    if not is_recording:
                        recorded_filename = start_recording()
                last_motion_time = current_time  # Update for recording
            else:
                motion_start_time = None

            # Adjust sensitivity dynamically
            if motion_detected:
                min_movement_area = min(min_movement_area + 5, max_movement_area)
            else:
                min_movement_area = max(min_movement_area - 1, 100)

        # Display status information
        status = "RECORDING" if is_recording else "MONITORING"
        cv2.putText(frame, status, (frame_width - 200, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # Show sensitivity level
        sensitivity = int(100 * (max_movement_area - min_movement_area) / max_movement_area)
        cv2.putText(frame, f"Sensitivity: {sensitivity}%", (20, frame_height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Display windows
        safe_show_window("Security Camera", frame)
        if not is_recording:  # Only show motion mask when not recording
            safe_show_window("Motion Mask", fgmask)
        else:
            try:
                cv2.destroyWindow("Motion Mask")
            except:
                pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    if is_recording:
        stop_recording()
    cap.release()
    cv2.destroyAllWindows()