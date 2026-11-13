import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib


df = pd.read_csv("Salary Data(1).csv")


print("========== First 5 Records ==========")
print(df.head())


print("\n========== Dataset Shape ==========")
print(df.shape)


print("\n========== Data Types ==========")
print(df.dtypes)


print("\n========== Missing Values ==========")
print(df.isnull().sum())


print("\n========== Descriptive Statistics ==========")
print(df.describe())


#B – Exploratory Data Analysis

plt.figure(figsize=(8,5))
sns.histplot(df["Salary"], bins=20, kde=True)
plt.title("Salary Distribution")
plt.show()

plt.figure(figsize=(8,5))
sns.scatterplot(data=df,
                x="Years of Experience",
                y="Salary")
plt.title("Years of Experience vs Salary")
plt.show()

plt.figure(figsize=(8,5))
sns.countplot(data=df,
              x="Education Level")
plt.xticks(rotation=30)
plt.title("Education Level Count")
plt.show()

plt.figure(figsize=(12,6))
sns.boxplot(data=df,
            x="Job Title",
            y="Salary")
plt.xticks(rotation=90)
plt.title("Salary by Job Title")
plt.show()

temp = df.copy()

le = LabelEncoder()

temp["Gender"] = le.fit_transform(temp["Gender"])
temp["Education Level"] = le.fit_transform(temp["Education Level"])
temp["Job Title"] = le.fit_transform(temp["Job Title"])

plt.figure(figsize=(8,6))
sns.heatmap(temp.corr(),
            annot=True,
            cmap="coolwarm")

plt.title("Correlation Heatmap")
plt.show()

plt.figure(figsize=(6,5))
sns.boxplot(y=df["Salary"])
plt.title("Salary Boxplot")
plt.show()

#C – Data Preprocessing

df = df.dropna()


gender_encoder = LabelEncoder()
education_encoder = LabelEncoder()
job_encoder = LabelEncoder()


df["Gender"] = gender_encoder.fit_transform(df["Gender"])
df["Education Level"] = education_encoder.fit_transform(df["Education Level"])
df["Job Title"] = job_encoder.fit_transform(df["Job Title"])


X = df.drop("Salary", axis=1)
y = df["Salary"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

#D – Machine Learning Model

model = RandomForestRegressor(random_state=42)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("\n========== Model Evaluation ==========")

print("R2 Score :", r2_score(y_test, y_pred))

print("MAE :", mean_absolute_error(y_test, y_pred))

print("MSE :", mean_squared_error(y_test, y_pred))

result = pd.DataFrame({
    "Actual Salary": y_test.values,
    "Predicted Salary": y_pred
})

print("\n========== Prediction ==========")

print(result.head(20))

joblib.dump(model, "salary_model.pkl")

joblib.dump(gender_encoder, "gender_encoder.pkl")

joblib.dump(education_encoder, "education_encoder.pkl")

joblib.dump(job_encoder, "job_encoder.pkl")

print("\nModel Saved Successfully")

