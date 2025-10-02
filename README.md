# 🏦   LoanBuddy - End-to-End Loan Decision ML Application
<p align="center">
<img src="screenshot/Loanbuddy.png" alt="Placeholder for LoanBuddy App Screenshot" />
</p>

## 📂 Project Structure

The LoanBuddy project follows a standard structure for an end-to-end Streamlit application, organizing the core application code, serialized machine learning models, and application assets.

```bash
Loanbuddy/
├── .devcontainer/            
│   └── devcontainer.json
├── screenshot/
│   └── Loanbuddy.png
├── App.py 
├── Classification.pkl
├── Regressor.pkl
├── background.png
├── README.md
└── requirements.txt
```

| File Name          | Type                   | Purpose                                                              |
| ------------------ | ---------------------------- | -------------------------------------------------------------------- |
| devcontainer.json  | JSON Config           |Defines a reproducible development environment (used by tools like GitHub Codespaces/VS Code Dev Containers), ensuring consistent dependencies, settings, and base OS for all developers. |
| Loanbuddy.png      | Image Asset           |This image file is used by Readme.md |
| App.py             | Python Script         |This is the main Streamlit application file. It handles the user interface (UI), loads the trained models, takes user input, performs predictions, and displays the results using Streamlit and Plotly.|
| Classification.pkl | Pickle Object         |This file contains the serialized GradientBoosting Classifier model used for predicting the binary outcome of "Loan Approval Status" (Approved/Not Approved).|
| Regressor.pkl      | Pickle Object         |This file contains the serialized Ridge Regression model used for predicting the continuous outcome of the "Maximum Loan Amount" that can be sanctioned.|
| background.png     | Image Asset           | This image file is used by App.py (via base64 encoding) to set the custom background for the Streamlit web application, enhancing the UI/UX.|
| README.md          | Markdown Document     | Provides a comprehensive overview of the project, including features, models, tech stack, and team information.|
| requirements.txt   | Requirements Document |list all the external Python libraries and packages required for Loanbuddy application.|

## 💡 About LoanBuddy
LoanBuddy is an interactive, Streamlit-based web application developed to simplify and streamline loan-related decision-making for both applicants and financial institutions. By leveraging robust machine learning models, the application provides real-time predictions and essential credit insights.

## This project was developed by: 

Tanmay Kubal

Rushikesh Pawal

Akash Yadav

Pooja Chaurasiya

Vivekranjan Yadav

## ✨ Key Features
LoanBuddy provides three core services to users:

✅ Loan Approval Status:
Instantly check whether a loan application is likely to be Approved or Not Approved based on applicant and financial criteria.

💰 Loan Amount Prediction:
Predict the Maximum Loan Amount that can be realistically sanctioned to the applicant.

📊 CIBIL Score Estimation:
Estimate the applicant’s CIBIL Score (Credit Score) based on their historical financial behavior and credit profile.

## ⚙️ Machine Learning Pipeline
### Models Implemented
The application utilizes a combination of supervised learning models, all trained using the Scikit-learn framework:

| Prediction Task | Model Used                   | Purpose                                                              |
| -------------   | ---------------------------- | -------------------------------------------------------------------- |
| Loan Approval   | GradientBoosting Classifier  |Binary classification for approval status (Approved/Not Approved).    |
| Loan Amount     | Ridge Regression             |Regression model to estimate the maximum sanctioned amount.           |
| CIBIL Score     | Custom CIBIL Score Estimator |A custom-derived model based on financial history and credit behavior.|

### Dataset
The models were trained on the Kaggle Loan Approval Prediction Dataset, a publicly available dataset widely used for loan eligibility and prediction tasks.

### End-to-End Workflow
The project demonstrates a complete ML production workflow, from data to deployment:

### Data Preprocessing & Feature Engineering:
Cleaning, scaling, and transforming raw data features.

### Model Training & Evaluation:
Training classification and regression models using Scikit-learn.

### Model Serialization:
Saving the trained models and preprocessors using Pickle (Classification.pkl and Regressor.pkl) for efficient loading in the web application.

### Deployment:
Integrating the serialized models into an interactive, user-facing Streamlit application.

## UI/UX & Design Highlights
The user interface was built to be modern, intuitive, and highly responsive:

### Framework:
Built entirely using Streamlit.

### Custom Styling:
Enhanced aesthetics using custom CSS styling for a professional and modern feel.

### Interactive Elements:
Features like gradient-based sliders and styled dropdowns for easy user input.

### Dynamic Visuals:
Real-time results displayed using interactive Plotly charts (e.g., the CIBIL score gauge).

### Feedback:
Provides dynamic success, warning, and error messages based on the loan approval results.

## 🛠️ Tech Stack

| Category          | Technology    |
| ----------------- | ------------- |
| Language          | Python        |
| ML Framework      | Scikit-learn  |
| Data Manipulation | Pandas, NumPy |
| Web Framework     | Streamlit     |
| Visualization     | Plotly        |
| Serialization     | Pickle        |
| Styling           | Custom CSS    |

## Key Takeaway
This project successfully transforms a complex machine learning solution into a production-ready application. It highlights the critical synergy between a robust ML backend (accurate models) and a clean, user-friendly UI/UX design to create genuine business value.
