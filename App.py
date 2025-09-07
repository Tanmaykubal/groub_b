import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import numpy as np

with open("Classification.pkl", "rb") as f:
    loan_classifier = pickle.load(f)

with open("Regressor.pkl", "rb") as f:
    loan_regressor = pickle.load(f)

page_bg_img = f""" <style> [data-testid="stAppViewContainer"] {{ background: url("https://sdmntprnorthcentralus.oaiusercontent.com/files/00000000-ef28-622f-86b8-a4b70c064106/raw?se=2025-09-07T09%3A20%3A01Z&sp=r&sv=2024-08-04&sr=b&scid=2006ddad-8130-5cd5-82f0-6a5626da89f2&skoid=cb94e22a-e3df-4e6a-9e17-1696f40fa435&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-09-06T16%3A30%3A44Z&ske=2025-09-07T16%3A30%3A44Z&sks=b&skv=2024-08-04&sig=KzJJmTdqt3UtK6AWzAyIf/KAmBe0hfLXvrbQmKgv8V0%3D") no-repeat center center fixed; background-size: cover; }} [data-testid="stHeader"] {{ background-color: rgba(0, 0, 0, 0); /* transparent header */ }} .main .block-container {{ background-color: rgba(255, 255, 255, 0); /* transparent content */ }} </style> """
st.markdown(page_bg_img, unsafe_allow_html=True)

# Sidebar Styling
sidebar_style = f""" <style> [data-testid="stSidebar"] > div:first-child {{ background-color: #0E71C5; color: white; /* text color */ }} [data-testid="stSidebar"] .css-1v0mbdj, [data-testid="stSidebar"] .css-10trblm, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {{ color: white !important; /* force text/icons to white */ }} </style> """
st.markdown(sidebar_style, unsafe_allow_html=True)
st.sidebar.title("🌟 LoanBuddy Navigation")
menu = st.sidebar.radio("Choose an option:", ["🏠 Home", "✅ Loan Approval", "💰 Loan Prediction", "📊 CIBIL Estimator"])

st.markdown(
    """
    <h1 style='text-align: center; 
               font-family: "Trebuchet MS", sans-serif; 
               font-size: 70px; 
               color: #ffffff; 
               text-shadow: 2px 2px 10px #000000;'>
        🏦 Loan<span style="color:#FFD700;">Buddy</span>
    </h1>
    """,
    unsafe_allow_html=True
)

if menu == "🏠 Home":
    st.markdown(
    """
    <div style='text-align: center; 
            font-family: "Trebuchet MS", sans-serif; 
            font-size: 22px; 
            line-height: 1.8; 
            color: #ffffff; 
            padding: 25px; 
            margin-top: 30px;
            background: rgba(0, 0, 0, 0.55); 
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.4);'>

    <h2 style='color: #FFD700; text-shadow: 1px 1px 8px #000; margin-bottom:20px;'>
         Welcome to LoanBuddy!
    </h2>

    <p>
    LoanBuddy is your smart companion for quick and reliable loan predictions.<br>
    With just a few simple details, you can:
    </p>

    <div style='text-align: left; display: inline-block;'>
        <p>✔ <b>Check your Loan Eligibility:</b> Know whether your loan will be approved (Yes/No).</p>
        <p>✔ <b>Predict Loan Amount:</b> Find out how much loan can be sanctioned.</p>
        <p>✔ <b>CIBIL Score Estimator:</b> Estimate your CIBIL score based on your credit behavior and financial profile.</p>
    </div>

    <p style='margin-top: 25px; font-size: 20px;'>
     Designed to be <b>simple, fast, and user-friendly</b>, LoanBuddy helps you make 
    <span style='color:#FFD700;'>informed financial decisions</span> with confidence.
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )
elif menu == "✅ Loan Approval":
    st.markdown(
        """
        <h2 style='text-align: center; 
                   font-family: "Trebuchet MS", sans-serif; 
                   font-size: 40px; 
                   color: #FFD700; 
                   text-shadow: 1px 1px 6px black;'>
            ✅ Loan Approval Check
        </h2>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown(
            """
            <div style='background: rgba(0, 0, 0, 0.55); 
                        padding: 25px; 
                        border-radius: 15px; 
                        box-shadow: 0px 4px 15px rgba(0,0,0,0.5); 
                        color: white; 
                        font-size: 18px; 
                        font-family: "Trebuchet MS", sans-serif;'>
            """,
            unsafe_allow_html=True
        )

        # Inputs
        col1, col2 = st.columns(2)
        with col1:
            self_employed = st.selectbox("💼 Self Employed", ["Yes", "No"])
            income_annum = st.number_input("💰 Annual Income (₹)", 250000, 10000000, 5000000, step=50000)
        with col2:
            loan_amount = st.number_input("🏦 Requested Loan Amount (₹)", 300000, 10000000, 5000000, step=50000)
            loan_term = st.slider("📅 Loan Term (in years)", 1, 30, 15)

        cibil_score = st.slider("📊 CIBIL Score", 300, 900, 650)

        st.markdown("</div>", unsafe_allow_html=True)

        # Prediction
        if st.button("🔍 Check Approval", use_container_width=True):
            columns = ['self_employed', 'income_annum', 'loan_amount', 'loan_term', 'cibil_score']
            X1 = pd.DataFrame([[self_employed, income_annum, loan_amount, loan_term, cibil_score]],
                              columns=columns)

            pred = loan_classifier.predict(X1)[0]

            if pred == 1:
                st.success("🎉 Congratulations! Your loan is likely to be **Approved** ✅")
            else:
                st.error("❌ Sorry, your loan may not be approved. Please review your details.")
elif menu == "💰 Loan Prediction":
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

elif menu == "📊 CIBIL Estimator":
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

        fig = go.Figure(go.Indicator( mode="gauge+number", value=score, title={'text': "Estimated CIBIL Score"}, gauge={ 'axis': {'range': [300, 900]}, 'bar': {'color': "black"}, 'steps': [ {'range': [300, 600], 'color': "red"}, {'range': [600, 750], 'color': "yellow"}, {'range': [750, 900], 'color': "green"} ], 'threshold': { 'line': {'color': "blue", 'width': 4}, 'thickness': 0.8, 'value': score } } ))
        st.plotly_chart(fig)
                
        if score < 600:
            st.error("⚠️ Poor Credit Score – Work on repayment discipline.")
        elif score < 750:
            st.warning("🙂 Fair Credit Score – Can be improved with timely payments.")
        else:
            st.success("🎉 Excellent Credit Score – You’re likely to get loans easily.")


















































