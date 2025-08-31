import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import numpy as np

with open("Classification.pkl", "rb") as f:
    loan_classifier = pickle.load(f)

with open("Regressor.pkl", "rb") as f:
    loan_regressor = pickle.load(f)

# ------------------ Gauge Function ------------------
def make_gauge(score=300):
    # Map score (300–900) → angle (180° to 0°)
    angle = (score - 300) * 180 / (900 - 300)
    rad = np.deg2rad(180 - angle)  # 300 = left, 900 = right
    
    needle_length = 0.4
    x_head = 0.5 + needle_length * np.cos(rad)
    y_head = 0.5 + needle_length * np.sin(rad)

    fig = go.Figure()

    # Gauge background (semicircle)
    fig.add_trace(go.Pie(
        values=[1,1,1,1,1,5],  # last part = blank
        labels=["Poor 300-579","Fair 580-669","Good 670-739",
                "Very Good 740-799","Excellent 800-900",""],
        marker=dict(colors=["#ef4444","#f97316","#facc15","#a3e635","#2ecc71","white"]),
        hole=0.5,
        direction="clockwise",
        sort=False,
        rotation=180,   # semicircle
        textinfo="label",
        hoverinfo="skip"
    ))

    # Needle
    fig.add_trace(go.Scatter(
        x=[0.5, x_head],
        y=[0.5, y_head],
        mode="lines",
        line=dict(color="black", width=6),
        hoverinfo="skip",
        showlegend=False
    ))

    # Center circle
    fig.add_trace(go.Scatter(
        x=[0.5],
        y=[0.5],
        mode="markers",
        marker=dict(size=30, color="black"),
        hoverinfo="skip",
        showlegend=False
    ))

    # Layout
    fig.update_layout(
        showlegend=False,
        margin=dict(t=50,b=20,l=20,r=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=400
    )
    return fig

st.sidebar.title("Loan Prediction App")
menu = st.sidebar.radio("Navigation", ["Home", "Loan Approval", "Loan Prediction", "CIBIL Estimator"])

if menu == "Home":
    st.title("🏦 LoanBuddy")
    st.write("""
    🏦 Welcome to LoanBuddy!
    
    LoanBuddy is your smart companion for quick and reliable loan predictions.
    With just a few simple details, you can:


    - **Check your Loan Eligibility**: Check whether your loan will be approved (Yes/No)
    - **Predict Loan Amount**: Predict how much loan can be sanctioned.
             
    Designed to be simple, fast, and user-friendly, LoanBuddy helps you make informed financial decisions with confidence
""")

elif menu == "Loan Approval":
    st.title("✅ Loan Approval Check")

    self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    income_annum = st.number_input("Annual Income (₹)", 250000, 10000000, 5000000)
    loan_amount = st.number_input("Requested Loan Amount (₹)", 300000, 10000000, 5000000)
    loan_term = st.slider("Loan Term (in years)", 0, 30, 15)
    cibil_score = st.slider("CIBIL Score", 300, 900, 650)

    


    if st.button("Check Approval"):
        columns = ['self_employed', 'income_annum', 'loan_amount', 'loan_term', 'cibil_score']
        X1 = pd.DataFrame([[self_employed, income_annum, loan_amount, loan_term, cibil_score]],
                 columns=columns)
        pred = loan_classifier.predict(X1)[0]


        if pred == 1:
            st.success("🎉 Congratulations! Your loan is likely to be Approved.")
        else:
            st.error("❌ Sorry, your loan may not be approved.")

elif menu == "Loan Prediction":
    st.title("💰 Loan Amount Prediction")

    self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    income_annum = st.number_input("Annual Income (₹)", 250000, 10000000, 5000000)
    loan_term = st.slider("Loan Term (in years)", 0, 30, 15)
    cibil_score = st.slider("CIBIL Score", 300, 900, 650)


    if st.button("Predict Sanctioned Loan"):
        columns_2 = ['self_employed', 'income_annum', 'loan_term', 'cibil_score']
        X2 = pd.DataFrame([[self_employed, income_annum, loan_term, cibil_score]],
                 columns=columns_2)
        pred = loan_regressor.predict(X2)[0]


        st.success(f"🏦 You are likely to be sanctioned a loan of: ₹{int(pred):,}")

elif menu == "CIBIL Estimator":
    st.title("📊 CIBIL Score Estimator")
    st.write("If you don’t know your CIBIL score, answer a few questions to estimate it.")

    # Example factors that influence CIBIL
    payment_history = st.slider("How regular are you with loan/credit card payments?", 1, 5, 3,
                                help="1 = Very Irregular, 5 = Always On Time")
    credit_utilization = st.slider("Credit Utilization Ratio (%)", 0, 100, 40,
                                   help="How much of your credit limit you use")
    credit_mix = st.selectbox("Do you have a mix of loans (Credit Card + Personal + Home Loan)?", ["No", "Yes"])
    loan_accounts = st.slider("Number of Active Loan/Credit Accounts", 0, 15, 3)
    credit_age = st.slider("Age of Credit History (years)", 0, 25, 5)

    if st.button("Estimate CIBIL Score"):
        # Simple formula for estimation (you can refine this with ML later)
        score = 300
        score += payment_history * 80
        score += (100 - credit_utilization) * 2
        score += 50 if credit_mix == "Yes" else -20
        score += loan_accounts * 5
        score += credit_age * 4

        # Keep within CIBIL range
        score = min(max(score, 300), 900)
        st.plotly_chart(make_gauge(score))
                
        if score < 600:
            st.error("⚠️ Poor Credit Score – Work on repayment discipline.")
        elif score < 750:
            st.warning("🙂 Fair Credit Score – Can be improved with timely payments.")
        else:
            st.success("🎉 Excellent Credit Score – You’re likely to get loans easily.")







