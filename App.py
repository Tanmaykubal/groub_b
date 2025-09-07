import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import base64

with open("Classification.pkl", "rb") as f:
    loan_classifier = pickle.load(f)
with open("Regressor.pkl", "rb") as f:
    loan_regressor = pickle.load(f)


# --- Functions for handling local images ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


bin_str = get_base64_of_bin_file('background.png')
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: url("data:image/png;base64,{bin_str}") no-repeat center center fixed;
    background-size: cover;
}}
[data-testid="stHeader"] {{
    background-color: rgba(0, 0, 0, 0); /* transparent header */
}}
.main .block-container {{
    background-color: rgba(255, 255, 255, 0); /* transparent content */
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# Sidebar Styling
sidebar_style = f"""
<style>
[data-testid="stSidebar"] > div:first-child {{
    background-color: #0E71C5;
    color: white; /* text color */
}}
[data-testid="stSidebar"] .css-1v0mbdj, [data-testid="stSidebar"] .css-10trblm, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {{
    color: white !important; /* force text/icons to white */
}}
</style>
"""
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

# --- Common Styling for all inputs and buttons ---
common_style = """
<style>
/* Number inputs and text inputs */
input[type="number"] {
    background-color: rgba(255,255,255,0.95) !important;
    color: #000000 !important;
    border-radius: 10px !important;
    border: 1px solid #ccc !important;
    padding: 8px 10px !important;
    font-weight: 700 !important;
}

div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.95) !important;
    color: black !important
}
/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #FFD700, #FFA500) !important;
    color: #000 !important;
    font-size: 18px;
    font-weight: 800;
    border-radius: 12px;
    padding: 10px 18px;
    border: none;
    box-shadow: 0 6px 14px rgba(0,0,0,0.18);
}

/* Labels white (to sit well on background) */
label, .stMarkdown p {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Ensure dropdown arrow is black */
div[data-baseweb="select"] svg { fill: #000 !important; }

/* Result boxes */
.result-success {
    background: linear-gradient(90deg, #dff7df, #bff0bf);
    color: #064d11;
    padding: 14px 18px;
    border-radius: 12px;
    font-weight: 800;
    text-align: center;
    box-shadow: 0 8px 18px rgba(0,0,0,0.12);
}
.result-error {
    background: linear-gradient(90deg, #ffd6d6, #ffb3b3);
    color: #5a0000;
    padding: 14px 18px;
    border-radius: 12px;
    font-weight: 800;
    text-align: center;
    box-shadow: 0 8px 18px rgba(0,0,0,0.12);
}
.result-warning {
    background: linear-gradient(90deg, #fff7df, #ffe0b3);
    color: #5a4b00;
    padding: 14px 18px;
    border-radius: 12px;
    font-weight: 800;
    text-align: center;
    box-shadow: 0 8px 18px rgba(0,0,0,0.12);
}
</style>
"""

# --- CIBIL Slider-specific styling ---
slider_style = """
<style>
/* Slider track (CIBIL gradient) */
div[data-testid="stSlider"] > div > div > div {
    background: linear-gradient(90deg, #ff4b4b 0%, #ffd14d 50%, #66d36e 100%) !important;
    height: 10px !important;
    color: white;
    border-radius: 6px !important;
}
/* Slider value text */
div[data-testid="stSlider"] .st-bd {
    color: white !important;
}
</style>
"""

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

# ---------- Loan Approval block ----------
elif menu == "✅ Loan Approval":
    st.markdown(common_style + slider_style, unsafe_allow_html=True)
    st.markdown(
        """
        <h1 style='text-align: center; 
                    font-family: "Trebuchet MS", sans-serif; 
                    font-size: 50px; 
                    color: #FFD700; 
                    text-shadow: 2px 2px 8px #000000; margin-bottom: 8px;'>
            ✅ Loan Approval Check
        </h1>
        """,
        unsafe_allow_html=True
    )

    # ---------- Inputs ----------
    col1, col2 = st.columns(2)
    with col1:
        self_employed = st.selectbox("🏢 Self Employed", ["Yes", "No"])
        income_annum = st.number_input("💰 Annual Income (₹)", 250000, 10000000, 5000000, step=50000, format="%d")
    with col2:
        loan_amount = st.number_input("🏦 Requested Loan Amount (₹)", 300000, 10000000, 5000000, step=50000, format="%d")
        loan_term = st.number_input("📅 Loan Term (in years)", 1, 30, 15)

    cibil_score = st.slider("📊 CIBIL Score", 300, 900, 650)

    # ---------- Prediction ----------
    if st.button("🔍 Check Approval"):
        columns = ['self_employed', 'income_annum', 'loan_amount', 'loan_term', 'cibil_score']
        X1 = pd.DataFrame([[self_employed, income_annum, loan_amount, loan_term, cibil_score]],
                          columns=columns)
        
        pred = loan_classifier.predict(X1)[0]
        
        if pred == 1:
            st.markdown(
                f"""
                <div class="result-success">
                    🎉 Congratulations! Your loan is likely to be
                    <span style='color:#0b6e0b; margin-left:8px;'>Approved ✅</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="result-error">
                    ❌ Sorry, your loan may not be approved.
                    <div style='font-weight:700; margin-top:6px;'>Tip: try improving income or CIBIL score.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ---------- Loan Prediction block ----------
elif menu == "💰 Loan Prediction":
    st.markdown(common_style + slider_style, unsafe_allow_html=True)
    st.markdown(
        """
        <h1 style='text-align: center; 
                    font-family: "Trebuchet MS", sans-serif; 
                    font-size: 50px; 
                    color: #FFD700; 
                    text-shadow: 2px 2px 8px #000000; margin-bottom: 8px;'>
            💰 Loan Amount Prediction
        </h1>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        self_employed = st.selectbox("🏢 Self Employed", ["Yes", "No"])    
    with col2:
        income_annum = st.number_input("💰 Annual Income (₹)", 250000, 10000000, 5000000)
    loan_term = st.slider("📅 Loan Term (in years)", 0, 30, 15)
    cibil_score = st.slider("📊 CIBIL Score", 300, 900, 650)    

    if st.button("Predict Sanctioned Loan"):
        columns_2 = ['self_employed', 'income_annum', 'loan_term', 'cibil_score']
        X2 = pd.DataFrame([[self_employed, income_annum, loan_term, cibil_score]],
                          columns=columns_2)
        pred = loan_regressor.predict(X2)[0]

        st.markdown(f'<div class="result-success">🏦 You are likely to be sanctioned a loan of: ₹{int(pred):,}</div>', unsafe_allow_html=True)

# ---------- CIBIL Estimator block ----------
elif menu == "📊 CIBIL Estimator":
    st.markdown(common_style + slider_style, unsafe_allow_html=True)
    st.markdown(
        """
        <h1 style='text-align: center; 
                    font-family: "Trebuchet MS", sans-serif; 
                    font-size: 50px; 
                    color: #FFD700; 
                    text-shadow: 2px 2px 8px #000000; margin-bottom: 8px;'>
            📊 CIBIL Score Estimator
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.write("If you don’t know your CIBIL score, answer a few questions to estimate it.")

    credit_mix = st.selectbox("Do you have a mix of loans (Credit Card + Personal + Home Loan)?", ["No", "Yes"])
    col1, col2 = st.columns(2)
    with col1:
        payment_history = st.slider("How regular are you with loan/credit card payments?", 1, 5, 3,
                                    help="1 = Very Irregular, 5 = Always On Time")
        credit_utilization = st.slider("Credit Utilization Ratio (%)", 0, 100, 40,
                                       help="How much of your credit limit you use")
    with col2:
        loan_accounts = st.slider("Number of Active Loan/Credit Accounts", 0, 15, 3)
        credit_age = st.slider("Age of Credit History (years)", 0, 25, 5)

    # Calculate score dynamically
    score = 300
    score += payment_history * 80
    score += (100 - credit_utilization) * 2
    score += 50 if credit_mix == "Yes" else -20
    score += loan_accounts * 5
    score += credit_age * 4

    score = min(max(score, 300), 900)
    st.button('Estimated CIBIL Score', use_container_width= True)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        gauge={
            'axis': {'range': [300, 900], 'tickwidth': 1, 'tickcolor': "darkgrey", 'tickfont': {'color': '#ffffff'}},
            'bar': {'color': "black"},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [
                {'range': [300, 600], 'color': "red"},
                {'range': [600, 750], 'color': "yellow"},
                {'range': [750, 900], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "blue", 'width': 4},
                'thickness': 0.8,
                'value': score
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#ffffff"},
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig)
    
    if score < 600:
        st.markdown('<div class="result-error">⚠️ Poor Credit Score – Work on repayment discipline.</div>', unsafe_allow_html=True)
    elif score < 750:
        st.markdown('<div class="result-warning">🙂 Fair Credit Score – Can be improved with timely payments.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-success">🎉 Excellent Credit Score – You’re likely to get loans easily.</div>', unsafe_allow_html=True)




