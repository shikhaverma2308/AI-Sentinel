# 🚨 AI Sentinel

AI Sentinel is a **real-time crowd monitoring and alert system** built using **Computer Vision and Deep Learning**. It detects people through live camera feed, analyzes crowd density, classifies risk levels, stores logs, and sends alerts automatically.

---

## 📸 Dashboard Preview

![AI Sentinel Dashboard](screenshots/dashboard.png)

---

## ✨ Features

* 👤 Real-time person detection using YOLOv8
* 📊 Live Streamlit dashboard
* 🚨 Risk level classification (Normal / Warning / High Risk)
* 📩 Telegram alert notifications
* 📸 Automatic evidence image capture
* 🗄️ SQLite data logging
* 📈 Crowd trend analytics

---

## 🛠️ Tech Stack

* Python
* YOLOv8
* OpenCV
* Streamlit
* Pandas
* SQLite
* Telegram Bot API

---

## ▶️ How to Run

```bash id="cxm7kk"
pip install -r requirements.txt
python detect.py
streamlit run dashboard.py
```

---

## 📁 Project Structure

* `detect.py` → Detection system
* `dashboard.py` → Analytics dashboard
* `requirements.txt` → Dependencies
* `screenshots/` → Project images
* `README.md` → Documentation

---

## 🚨 Risk Levels

* 🟢 NORMAL
* 🟠 WARNING
* 🔴 HIGH RISK

---

## 🎯 Use Cases

* Smart City Monitoring
* Public Crowd Management
* Event Safety Monitoring
* Railway / Metro Security
* Campus Surveillance

---

## 👩‍💻 Author

**Shikha Verma**

---


