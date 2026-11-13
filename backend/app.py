import os
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent

def load_artifact(filename):
    path = BASE_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Required model file not found: {path}")
    return joblib.load(path)

# Load the trained model and encoders once when the service starts.
model = load_artifact("salary_model.pkl")
gender_encoder = load_artifact("gender_encoder.pkl")
education_encoder = load_artifact("education_encoder.pkl")
job_encoder = load_artifact("job_encoder.pkl")

app = Flask(__name__)

# Set NETLIFY_URL in Render after the frontend has been deployed.
# Multiple origins can be comma-separated.
allowed_origins = [
    origin.strip()
    for origin in os.getenv("NETLIFY_URL", "*").split(",")
    if origin.strip()
]
CORS(app, resources={r"/*": {"origins": allowed_origins}})


@app.get("/")
def home():
    return jsonify({
        "status": "success",
        "message": "AI Salary Prediction API is running"
    })


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.get("/options")
def options():
    """Return the valid dropdown choices for the frontend."""
    return jsonify({
        "genders": [str(value) for value in gender_encoder.classes_],
        "educations": [str(value) for value in education_encoder.classes_],
        "jobs": [str(value) for value in job_encoder.classes_]
    })


def required_number(data, key, number_type):
    value = data.get(key)
    if value is None or value == "":
        raise ValueError(f"{key} is required.")
    try:
        number = number_type(value)
    except (TypeError, ValueError):
        raise ValueError(f"{key} must be a valid number.")
    return number


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Request body must be valid JSON."
        }), 400

    try:
        age = required_number(data, "age", int)
        experience = required_number(data, "experience", float)

        gender = str(data.get("gender", "")).strip()
        education = str(data.get("education", "")).strip()
        job = str(data.get("job", "")).strip()

        if not 18 <= age <= 100:
            raise ValueError("Age must be between 18 and 100.")
        if experience < 0 or experience > 80:
            raise ValueError("Years of experience must be between 0 and 80.")

        if gender not in gender_encoder.classes_:
            raise ValueError("Please select a valid gender.")
        if education not in education_encoder.classes_:
            raise ValueError("Please select a valid education level.")
        if job not in job_encoder.classes_:
            raise ValueError("Please select a valid job title.")

        gender_value = int(gender_encoder.transform([gender])[0])
        education_value = int(education_encoder.transform([education])[0])
        job_value = int(job_encoder.transform([job])[0])

        # Column names and order must match the model's training data.
        input_data = pd.DataFrame([{
            "Age": age,
            "Gender": gender_value,
            "Education Level": education_value,
            "Job Title": job_value,
            "Years of Experience": experience
        }])

        salary = float(model.predict(input_data)[0])

        score = min(100, int((experience * 10) + 40))
        hiring = min(100, score + 5)
        progress = min(100, int((experience / 10) * 100))

        if salary < 50000:
            rating = "⭐⭐⭐"
        elif salary < 100000:
            rating = "⭐⭐⭐⭐"
        else:
            rating = "⭐⭐⭐⭐⭐"

        if experience < 2:
            ai = "Gain practical experience through internships and improve technical skills."
            category = "Fresher"
            recommendation = "Suitable for Entry Level Position"
        elif experience < 5:
            ai = "You are ready for Junior Software Engineer or Web Developer roles."
            category = "Junior"
            recommendation = "Recommended for Interview"
        elif experience < 10:
            ai = "You have strong potential for Team Lead or Senior Developer positions."
            category = "Mid-Level"
            recommendation = "Strong Candidate"
        else:
            ai = "Excellent profile for Senior Engineer, Manager or Architect positions."
            category = "Senior"
            recommendation = "Highly Recommended"

        return jsonify({
            "status": "success",
            "prediction": round(salary, 2),
            "category": category,
            "recommendation": recommendation,
            "score": score,
            "hiring": hiring,
            "progress": progress,
            "rating": rating,
            "ai_suggestion": ai
        })

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400
    except Exception:
        app.logger.exception("Salary prediction failed")
        return jsonify({
            "status": "error",
            "message": "Prediction failed due to a server error. Please try again."
        }), 500


if __name__ == "__main__":
    # Local development only. Render runs the app with Gunicorn.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
