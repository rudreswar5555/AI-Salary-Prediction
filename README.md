# 💰 AI Powered Salary Prediction Dashboard

An intelligent web-based Salary Prediction Dashboard developed using **Python, Flask, Machine Learning, HTML, CSS, Bootstrap and JavaScript**.

The application predicts an estimated salary based on candidate information such as age, gender, education level, years of experience and job role.

## 🚀 Project Overview

The AI Powered Salary Prediction Dashboard helps users estimate potential salaries using a trained Machine Learning model.

It provides a user-friendly interface where candidates can enter their professional information and receive an estimated salary prediction.

## ✨ Key Features

- AI-based salary prediction
- Interactive and responsive dashboard
- Candidate information input form
- Multiple education levels and job roles
- Machine Learning model integration
- Flask-based backend API
- Real-time salary prediction results
- Clean and modern user interface

## 🛠️ Technologies Used

**Frontend**
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Font Awesome

**Backend**
- Python
- Flask
- Flask API

**Machine Learning**
- Scikit-learn
- Pandas
- NumPy
- Joblib
- Label Encoding

## 📂 Project Structure

```text
AI-Salary-Prediction/
│
├── backend/
│   ├── app.py
│   ├── salary_model.pkl
│   ├── education_encoder.pkl
│   ├── gender_encoder.pkl
│   ├── job_encoder.pkl
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── training/
│   ├── Salary Data(1).csv
│   └── salary_prediction.py
│
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/rudreswar5555/AI-Salary-Prediction.git
```

### 2. Open the Project

```bash
cd AI-Salary-Prediction
```

### 3. Create a Virtual Environment

```bash
cd backend
python -m venv venv
```

### 4. Activate Virtual Environment (Windows)

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Flask Backend

```bash
python app.py
```

The backend will run at:

`http://127.0.0.1:5000/`

### 7. Run the Frontend

Open `frontend/index.html` using VS Code Live Server.

The frontend will open in your browser.

## 🖥️ Application Preview

Add your project screenshots here.

## 🧠 Machine Learning Model

The project uses a trained Machine Learning model to estimate candidate salaries based on input features.

The trained model and encoding files are stored in the backend directory using Pickle (`.pkl`) files.

## 🔮 Future Improvements

- Improve prediction accuracy
- Add user authentication
- Store prediction history
- Add interactive salary analytics
- Deploy the application online
- Improve mobile responsiveness

## 👨‍💻 Developer

**Rudreswar Prasad Paul**

B.Tech – Computer Science and Engineering

GitHub: https://github.com/rudreswar5555

LinkedIn: https://www.linkedin.com/in/rudreswar-prasad-paul-2a5214379/

---

⭐ If you find this project useful, consider giving it a star!

**Developed with ❤️ using Python and Machine Learning.**
