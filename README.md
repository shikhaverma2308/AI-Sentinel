#  AI Sentinel

AI Sentinel is a real-time crowd monitoring and alert system built using Computer Vision and Deep Learning. It detects people through live camera feed, analyzes crowd density, classifies risk levels, and sends alerts automatically.

## ✨ Features

* 👤 Real-time person detection using YOLOv8
* 📊 Live Streamlit dashboard
* 🚨 Risk level classification (Normal / Warning / High Risk)
* 📩 Telegram alert notifications
* 📸 Automatic evidence image capture
* 🗄️ SQLite data logging

## 🛠️ Tech Stack

* Python
* YOLOv8
* OpenCV
* Streamlit
* SQLite
* Telegram Bot API

## ▶️ How to Run

```bash
pip install -r requirements.txt
python detect.py
streamlit run dashboard.py
```

## 📁 Project Structure

* `detect.py` → Detection system
* `dashboard.py` → Analytics dashboard
* `requirements.txt` → Dependencies

## 👩‍💻 Author

Shikha Verma
