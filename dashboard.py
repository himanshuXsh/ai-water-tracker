import streamlit as st
import requests
import pandas as pd
from datetime import date

BASE_URL = "http://127.0.0.1:8001"

st.set_page_config(page_title="AI Water Tracker", layout="wide")

# -------------------------------
# Session State
# -------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None


# -------------------------------
# Login / Register Page
# -------------------------------

def login_page():
    st.title("💧 AI Water Tracker")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username")

        if st.button("Login"):
            response = requests.get(f"{BASE_URL}/history/{username}")
            if response.status_code == 200:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error("User not found")

    with tab2:
        new_user = st.text_input("New Username")
        goal = st.number_input("Daily Goal (ml)", min_value=500, value=3000)

        if st.button("Register"):
            payload = {
                "username": new_user,
                "daily_goal": goal
            }
            response = requests.post(f"{BASE_URL}/register", json=payload)
            if response.status_code == 200:
                st.success("User registered! Now login.")
            else:
                st.error("User already exists")


# -------------------------------
# Dashboard Page
# -------------------------------

def dashboard_page():

    st.sidebar.title(f"👤 {st.session_state.username}")

    menu = st.sidebar.radio(
        "Navigation",
        ["Home", "Analytics", "Settings", "Logout"]
    )

    if menu == "Home":
        home_page()

    elif menu == "Analytics":
        analytics_page()

    elif menu == "Settings":
        settings_page()

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()


# -------------------------------
# Home Page
# -------------------------------

def home_page():
    st.title("🏠 Today's Dashboard")

    today = date.today().strftime("%Y-%m-%d")

    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("Water Intake (ml)", min_value=0, step=100)

    with col2:
        selected_date = st.date_input("Select Date", value=date.today())

    if st.button("Log Water"):
        payload = {
            "username": st.session_state.username,
            "amount": amount,
            "date": selected_date.strftime("%Y-%m-%d")
        }

        response = requests.post(f"{BASE_URL}/log", json=payload)

        if response.status_code == 200:
            data = response.json()

            st.success("Water logged successfully!")

            st.metric("Today Total (ml)", data["today_total_ml"])
            st.metric("Daily Goal (ml)", data["daily_goal_ml"])
            st.metric("Progress (%)", data["progress_percent"])

            st.progress(data["progress_percent"] / 100)

            st.subheader("🤖 AI Feedback")
            st.write(data["ai_feedback"])

        else:
            st.error("Error logging water")


# -------------------------------
# Analytics Page
# -------------------------------

def analytics_page():
    st.title("📊 Analytics")

    username = st.session_state.username

    # Weekly chart
    response = requests.get(f"{BASE_URL}/weekly-chart/{username}")
    if response.status_code == 200:
        data = response.json()["data"]

        if data:
            df = pd.DataFrame(data)
            df["date"] = pd.to_datetime(df["date"])

            st.subheader("Weekly Intake Trend")
            st.bar_chart(df.set_index("date")["total_ml"])

    # Monthly summary
    monthly = requests.get(f"{BASE_URL}/monthly/{username}")
    if monthly.status_code == 200:
        st.metric("Monthly Total (ml)", monthly.json()["monthly_total_ml"])


# -------------------------------
# Settings Page
# -------------------------------

def settings_page():
    st.title("⚙ Settings")

    new_goal = st.number_input("Update Daily Goal (ml)", min_value=500)

    if st.button("Update Goal"):
        payload = {
            "username": st.session_state.username,
            "new_goal": new_goal
        }

        response = requests.post(f"{BASE_URL}/update-goal", json=payload)

        if response.status_code == 200:
            st.success("Goal updated successfully!")
        else:
            st.error("Failed to update goal")


# -------------------------------
# App Controller
# -------------------------------

if not st.session_state.logged_in:
    login_page()
else:
    dashboard_page()
