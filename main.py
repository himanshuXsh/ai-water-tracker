from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

from database import (
    create_user,
    get_user,
    update_user_goal,
    log_intake,
    get_history,
    get_today_total,
    get_weekly_total,
    get_monthly_total,
    get_weekly_chart_data
)

from agent import analyze_intake

app = FastAPI()


# -------------------------------
# Pydantic Models
# -------------------------------

class UserCreate(BaseModel):
    username: str
    daily_goal: int


class GoalUpdate(BaseModel):
    username: str
    new_goal: int


class IntakeRequest(BaseModel):
    username: str
    amount: int
    date: str  # format: YYYY-MM-DD


# -------------------------------
# User Routes
# -------------------------------

@app.post("/register")
def register_user(data: UserCreate):
    try:
        create_user(data.username, data.daily_goal)
        return {"message": "User registered successfully"}
    except:
        raise HTTPException(status_code=400, detail="User already exists")


@app.post("/update-goal")
def change_goal(data: GoalUpdate):
    update_user_goal(data.username, data.new_goal)
    return {"message": "Goal updated successfully"}


# -------------------------------
# Intake Route
# -------------------------------

@app.post("/log")
def log_water(data: IntakeRequest):

    # Validate date format
    try:
        datetime.strptime(data.date, "%Y-%m-%d")
    except:
        raise HTTPException(status_code=400, detail="Invalid date format (YYYY-MM-DD)")

    success = log_intake(data.username, data.amount, data.date)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    user = get_user(data.username)
    daily_goal = user[1]

    total_today = get_today_total(data.username)
    progress_percent = (total_today / daily_goal) * 100

    feedback = analyze_intake(total_today, daily_goal)

    return {
        "message": "Water logged successfully",
        "today_total_ml": total_today,
        "daily_goal_ml": daily_goal,
        "progress_percent": round(progress_percent, 2),
        "ai_feedback": feedback
    }


# -------------------------------
# History Route
# -------------------------------

@app.get("/history/{username}")
def read_history(username: str):
    records = get_history(username)
    return {"username": username, "history": records}


# -------------------------------
# Analytics Routes
# -------------------------------

@app.get("/daily/{username}")
def daily_summary(username: str):
    total = get_today_total(username)
    return {"username": username, "today_total_ml": total}


@app.get("/weekly/{username}")
def weekly_summary(username: str):
    total = get_weekly_total(username)
    average = total / 7
    return {
        "username": username,
        "weekly_total_ml": total,
        "average_per_day_ml": round(average, 2)
    }


@app.get("/monthly/{username}")
def monthly_summary(username: str):
    total = get_monthly_total(username)
    return {"username": username, "monthly_total_ml": total}


@app.get("/weekly-chart/{username}")
def weekly_chart(username: str):
    data = get_weekly_chart_data(username)
    return {"username": username, "data": data}
