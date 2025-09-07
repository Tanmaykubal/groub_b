import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import numpy as np

with open("Classification.pkl", "rb") as f:
    loan_classifier = pickle.load(f)

with open("Regressor.pkl", "rb") as f:
    loan_regressor = pickle.load(f)

# Dropdown for background-size
size_option = st.sidebar.selectbox(
    "Choose Background Size",
    ["auto", "cover", "contain", "100% auto", "auto 100%", "100% 100%", "50% 50%", "200px 300px"]
)

image_url = st.sidebar.text_input(
    "Enter background image URL:", 
    "https://lh3.googleusercontent.com/gg-dl/AJfQ9KQ4oPkJOUh0MhF_wjH3DNhNzW4kbCnssfjO61GEkEtMoz0HUPLsx2JDWjVlE_z4ZaNB_GP1gAx1HXk7v0KvLJOzkL7x-TadZyOaBj-6ZxGIBwIOFPzRot3bL-uqf2l7_1k8ulxCi8rYX-zZbhSlE2T8-TeNRAb9Jn9kXVC8WVs8E-X-aw"  # default demo image
)

if image_url:
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: url("{image_url}") no-repeat center center fixed;
        background-size: {size_option};
    }}

    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);  /* transparent header */
    }}

    .main .block-container {{
        background-color: rgba(255, 255, 255, 0);  /* transparent content */
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
# Sidebar background color picker
sidebar_color = st.sidebar.color_picker("Pick a sidebar color", "#1E3A8A")  # default navy blue

# Inject CSS
sidebar_style = f"""
<style>
[data-testid="stSidebar"] > div:first-child {{
    background-color: {sidebar_color};
    color: white;  /* text color */
}}

[data-testid="stSidebar"] .css-1v0mbdj, 
[data-testid="stSidebar"] .css-10trblm, 
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] span {{
    color: white !important;  /* force text/icons to white */
}}
</style>
"""
st.markdown(sidebar_style, unsafe_allow_html=True)

st.sidebar.title("Loan Prediction App")
menu = st.sidebar.radio("Navigation", ["Home", "Loan Approval", "Loan Prediction", "CIBIL Estimator"])

import streamlit as st

st.markdown(
    """
    <h1 style='text-align: center; 
               font-family: "Trebuchet MS", sans-serif; 
               font-size: 70px; 
               color: #ffffff; 
               text-shadow: 2px 2px 10px #000000;'>
        🏦 Loan<span style="color:#00f2fe;">Buddy</span>
    </h1>
    """,
    unsafe_allow_html=True
)

if menu == "Home":
    st.title("🏦 LoanBuddy")
    st.write("""
    🏦 Welcome to LoanBuddy!
    
    LoanBuddy is your smart companion for quick and reliable loan predictions.
    With just a few simple details, you can:


    - **Check your Loan Eligibility**: Check whether your loan will be approved (Yes/No)
    - **Predict Loan Amount**: Predict how much loan can be sanctioned.
    - **CIBIL Score Estimator**: Estimate your CIBIL score based on your credit behavior and financial profile.
             
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

        fig = go.Figure(go.Indicator( mode="gauge+number", value=score, title={'text': "Estimated CIBIL Score"}, gauge={ 'axis': {'range': [300, 900]}, 'bar': {'color': "black"}, 'steps': [ {'range': [300, 600], 'color': "red"}, {'range': [600, 750], 'color': "yellow"}, {'range': [750, 900], 'color': "green"} ], 'threshold': { 'line': {'color': "blue", 'width': 4}, 'thickness': 0.8, 'value': score } } ))
        st.plotly_chart(fig)
                
        if score < 600:
            st.error("⚠️ Poor Credit Score – Work on repayment discipline.")
        elif score < 750:
            st.warning("🙂 Fair Credit Score – Can be improved with timely payments.")
        else:
            st.success("🎉 Excellent Credit Score – You’re likely to get loans easily.")


























