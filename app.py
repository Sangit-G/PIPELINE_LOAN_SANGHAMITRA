import streamlit as st
import pandas as pd
import joblib

# Load your trained model and preprocessing pipeline
model = joblib.load("artifacts/model.pkl")
preprocessor = joblib.load("artifacts/preprocessor.pkl")

st.title("Loan Defaulters Prediction App")


# Sidebar inputs
Credit_Worthiness=st.sidebar.selectbox("Credit Worthiness",["l1","l2"])
loan_amount = st.sidebar.number_input("Loan Amount")
term=st.sidebar.number_input("Term")
Neg_ammortization = st.sidebar.selectbox("Neg Ammortization",["not_neg", "neg_amm"])
interest_only = st.sidebar.selectbox("Interest only",['not_int','int_only'])
lump_sum_payment= st.sidebar.selectbox("Lump Sum Payment",["not_lpsm", "lpsm"])
income = st.sidebar.number_input("Income")
credit_type= st.sidebar.selectbox("Credit Type",["EXP", "EQUI", "CRIF", "CIB"])
Credit_Score = st.sidebar.slider("Credit Score")

# Create input dataframe
input_data = pd.DataFrame({
    "Credit_Worthiness":[Credit_Worthiness],
    "loan_amount": [loan_amount],
    "term":[term],
    "Neg_ammortization":[Neg_ammortization],
    "interest_only":[interest_only],
    "lump_sum_payment":[lump_sum_payment],
    "income": [income],
    "credit_type":[credit_type],
    "Credit_Score": [Credit_Score]
})

# Preprocess and predict
transformed_data = preprocessor.transform(input_data)
prediction = model.predict(transformed_data)[0]
probability = model.predict_proba(transformed_data)[0][1]

# Display results
st.subheader("Prediction:")
if prediction == 1:
    st.error(f"Likely to Default ⚠️ (Confidence: {probability:.2f})")
else:
    st.success(f"Not Likely to Default ✅ (Confidence: {1 - probability:.2f})")