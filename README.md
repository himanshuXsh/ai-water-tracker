
# 💧 AI Water Tracker

An AI-powered hydration tracking system built using **FastAPI**, **Streamlit**, and **Hugging Face LLM**.

This project allows users to:

- Register with custom daily hydration goals
- Log water intake with date selection
- Track daily, weekly, and monthly progress
- View analytics charts
- Get AI-generated hydration advice
- Update personal hydration goals

---

## 🚀 Tech Stack

- **FastAPI** – Backend API
- **SQLite** – Database
- **Streamlit** – Frontend Dashboard
- **Hugging Face API** – AI-generated hydration advice
- **Python Requests** – API communication
- **Pydantic** – Data validation

---

## 🏗 System Architecture

```

Streamlit (Frontend)
↓
FastAPI (Backend API)
↓
SQLite Database
↓
Hugging Face LLM (AI Advice)

````

---

## 📌 Features

### 👤 User System
- User registration
- Custom daily hydration goal
- Goal update functionality

### 💧 Water Logging
- Log intake with date selection
- Auto calculation of daily total
- Progress percentage tracking

### 📊 Analytics
- Daily summary
- Weekly total & average
- Monthly total
- Weekly bar chart visualization

### 🤖 AI Feedback
- AI generates hydration advice
- Based on total intake vs goal

---

## 🛠 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-water-tracker.git
cd ai-water-tracker
````

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

**Windows:**

```bash
.venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Create `.env` File

Create a file named `.env` in root folder:

```
HF_API_KEY=your_huggingface_token_here
```

---

### 5️⃣ Run Backend

```bash
python -m uvicorn main:app --reload --port 8001
```

Swagger Docs:

```
http://127.0.0.1:8001/docs
```

---

### 6️⃣ Run Dashboard

Open new terminal:

```bash
streamlit run dashboard.py
```

Dashboard runs at:

```
http://localhost:8501
```

---

## 📂 Project Structure

```
ai-water-tracker/
│
├── main.py
├── database.py
├── agent.py
├── dashboard.py
├── requirements.txt
├── .env (ignored)
├── .gitignore
└── README.md
```

---

## 🔐 Security

* `.env` file is ignored via `.gitignore`
* API keys are not stored in repository
* GitHub secret scanning enabled

---

## 🎯 Learning Objectives

This project demonstrates:

* REST API design with FastAPI
* Clean backend architecture
* Separation of concerns
* AI API integration
* Secure secret handling
* Frontend-backend communication
* Data analytics and visualization

---

## 📈 Future Improvements

* Authentication with JWT
* Password-based login
* Streak tracking
* Calendar heatmap
* Deployment on cloud (Render / Railway)
* Switch to production-grade LLM endpoint

---

## 👨‍💻 Author

Himanshu Sharma
AI/ML Student | Backend & AI Systems Enthusiast

<img width="1919" height="1003" alt="Screenshot 2026-02-18 010820" src="https://github.com/user-attachments/assets/8bd76eec-92b4-47a6-af2d-aa7595de87ad" />
<img width="1919" height="1012" alt="Screenshot 2026-02-18 010838" src="https://github.com/user-attachments/assets/88f425c3-4657-4aae-b17d-9d7a8ffdbf40" />
<img width="1919" height="1004" alt="Screenshot 2026-02-18 010857" src="https://github.com/user-attachments/assets/89969352-11ef-4108-b5f7-543c392f0449" />
<img width="1893" height="1005" alt="Screenshot 2026-02-18 010908" src="https://github.com/user-attachments/assets/d1bcd490-2d0b-47a5-bbbb-ad0951177c60" />
<img width="1919" height="1140" alt="Screenshot 2026-02-18 011009" src="https://github.com/user-attachments/assets/7b19769e-f5e6-4a38-8503-4635ec4babd0" />

<img width="1024" height="1536" alt="ChatGPT Image Feb 18, 2026, 01_29_26 AM" src="https://github.com/user-attachments/assets/a2dd34db-c8ea-4efd-aa55-47afdbb03c60" />





