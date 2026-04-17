from ultralytics import YOLO
import cv2
import requests
import time
import os
import threading
import sqlite3
import threading
from datetime import datetime
from dotenv import load_dotenv

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

# =========================
# TELEGRAM ALERT FUNCTION
# =========================
def send_alert():
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    if not token or not chat_id:
        print("Telegram token/chat id missing")
        return

    message = "🚨 ALERT: Crowd Detected!"

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        requests.post(url, data={
            "chat_id": chat_id,
            "text": message
        })
        print("Alert Sent!")
    except:
        print("Telegram alert failed")


# =========================
# SAVE IMAGE EVIDENCE
# =========================
def save_evidence(frame):
    if not os.path.exists("evidence"):
        os.makedirs("evidence")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"evidence/alert_{timestamp}.jpg"

    cv2.imwrite(filename, frame)
    print("Saved:", filename)
# =========================
# DATABASE SETUP
# =========================
def setup_database():
    with sqlite3.connect("crowd.db") as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS crowd_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            person_count INTEGER,
            risk_level TEXT
        )
        """)

        conn.commit()

# =========================
# SQL LOGGING
# =========================
def log_data(count):
    with sqlite3.connect("crowd.db") as conn:
        cursor = conn.cursor()

        time_now = datetime.now().strftime("%H:%M:%S")

        if count >= 5:
            risk = "HIGH RISK"
        elif count >= 3:
            risk = "WARNING"
        else:
            risk = "NORMAL"

        cursor.execute("""
        INSERT INTO crowd_log (time, person_count, risk_level)
        VALUES (?, ?, ?)
        """, (time_now, count, risk))

        conn.commit()


# =========================
# LOAD MODEL
# =========================
setup_database()
model = YOLO("yolov8n.pt")

# =========================
# CAMERA START
# =========================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# =========================
# VARIABLES
# =========================
threshold = 2
last_log_time = 0
last_alert_time = 0
last_count = 0
frame_count = 0
frame_id = 0
zero_start = None

# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_id += 1
    if frame_id % 3 != 0:
        continue

    # YOLO detection
    results = model(frame)
    annotated_frame = results[0].plot()

    # =====================
    # PERSON COUNT
    # =====================
    person_count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            if label == "person":
                person_count += 1

    print("Persons:", person_count)

    current_time = time.time()

    # =====================
    # STABLE COUNT LOGIC
    # =====================
    if person_count > 0:
        stable_count = person_count
        last_count = person_count
        zero_start = None

    else:
        if zero_start is None:
            zero_start = time.time()

        if time.time() - zero_start > 5:
            stable_count = 0
            last_count = 0
        else:
            stable_count = last_count

    # =====================
    # LOG EVERY 2 SEC
    # =====================
    if current_time - last_log_time > 2:
        log_data(stable_count)
        last_log_time = current_time

    # =====================
    # STATUS COLOR
    # =====================
    if person_count >= 5:
        status = "HIGH RISK"
        color = (0, 0, 255)

    elif person_count >= 3:
        status = "WARNING"
        color = (0, 165, 255)

    else:
        status = "NORMAL"
        color = (0, 255, 0)

    cv2.putText(
        annotated_frame,
        status,
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        3
    )

    # =====================
    # FALSE ALERT CONTROL
    # =====================
    if person_count >= threshold:
        frame_count += 1
    else:
        frame_count = 0

    # =====================
    # ALERT TRIGGER
    # =====================
    if frame_count >= 5:
      if current_time - last_alert_time > 10:

        threading.Thread(target=send_alert).start()

        save_evidence(frame)

        last_alert_time = current_time
        frame_count = 0

    # =====================
    # SHOW CAMERA
    # =====================
    cv2.imshow("AI Sentinel", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# =========================
# RELEASE
# =========================
cap.release()
cv2.destroyAllWindows()