import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")

# Get API key from environment variable or set direct key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.AbBRN6K1nnONCS3h1klFk3yZoWBWLHDaYGF180En-FVYYatjA")
genai.configure(api_key=GEMINI_API_KEY)

class UserProfile(BaseModel):
    weight_kg: float
    height_cm: float
    age: int
    gender: str
    goal: str

@app.get("/")
def home():
    return {"message": "Welcome to FitBuddy AI Fitness Plan Generator!"}

@app.post("/generate-fitness-plan")
def generate_fitness_plan(profile: UserProfile):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Act as an expert fitness trainer and nutritionist.
        Create a personalized 1-day sample fitness and diet plan for:
        - Age: {profile.age}, Gender: {profile.gender}
        - Weight: {profile.weight_kg} kg, Height: {profile.height_cm} cm
        - Goal: {profile.goal}

        Provide response in structured JSON with keys:
        - bmi_status
        - daily_workout_routine
        - diet_recommendation
        - motivational_tip
        """
        response = model.generate_content(prompt)
        return {"status": "success", "fitness_plan": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}