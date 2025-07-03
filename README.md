# ZebraSync

> [https://zebrasync.onrender.com](https://zebrasync.onrender.com)


⚠️ **Note:** The server may go to sleep if inactive. The first request after a period of inactivity can take up to **50 seconds** to wake up. Please be patient when accessing the live demo.

ZebraSync is a one-way folder synchronization engine with a built-in dashboard, real-time logging, and async task handling. Designed for reliability, minimalism, and clarity — not hype.

## Features

- One-way sync: `source → replica`
- MD5-based file comparison
- Nested directories supported
- File upload via ZIP (auto-extracted)
- Background task execution with Celery
- Real-time log streaming (API + DB + file)
- Futuristic terminal-style UI
- REST API integration

## Tech Stack

- Python 3.11+
- Django 5+
- Celery 5+
- Redis (Upstash-compatible)
- PostgreSQL (or SQLite for dev/testing)

## Setup

```bash
git clone https://github.com/Mario8802/zebrasync.git
cd zebrasync
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
![image](https://github.com/user-attachments/assets/0802039a-8b19-404f-a6db-a1c4f23758ee)
