import streamlit as st
import pandas as pd
import joblib

# Load your trained model and preprocessing pipeline
model = joblib.load("artifacts/model.pkl")
preprocessor = joblib.load("artifacts/preprocessor.pkl")

st.title("📊 Loan Risk Analyzer | Tiered Credit Prediction")

#  Step 1: Tier selection with mapping
tier_map = {
    "Basic Credit Info (l1)": "l1",
    "Full Credit Profile (l2)": "l2"
}

neg_map = {
    "No Negative Amortization": "not_neg",
    "Negative Amortization": "neg_amm"
}

interest_map = {
    "No Interest Only Period": "not_int",
    "Has Interest Only Period": "int_only"
}

lump_map = {
    "No Lump Sum Payment": "not_lpsm",
    "Has Lump Sum Payment": "lpsm"
}

credit_type_map = {
    "Experian (EXP)-global player in credit scoring ": "EXP",
    "Equifax (EQUI)-known for consumer credit insights ": "EQUI",
    "CRIF High Mark (CRIF)-analytics-driven credit bureau ": "CRIF",
    "CIBIL (CIB)-dominant bureau in India": "CIB"
}



selected_tier = st.sidebar.selectbox("🧾 Credit Data Tier", list(tier_map.keys()))
Credit_Worthiness = tier_map[selected_tier]

selected_neg = st.sidebar.selectbox(" 🌀 Negative Amortization", list(neg_map.keys()))
Neg_ammortization = neg_map[selected_neg]

selected_interest = st.sidebar.selectbox(" 🕰️ Interest Only Period", list(interest_map.keys()))
interest_only = interest_map[selected_interest]

selected_lump = st.sidebar.selectbox(" 💼  Lump Sum Payment Status", list(lump_map.keys()))
lump_sum_payment = lump_map[selected_lump]

selected_credit_type = st.sidebar.selectbox(" 🔍 Credit Bureau", list(credit_type_map.keys()))
credit_type = credit_type_map[selected_credit_type]
#  Step 2: Clarify tier definitions
st.sidebar.info(" **Credit Data Tiers Explained**\n\n- **l1**: Includes only basic credit details like card usage and loan amount.\n- **l2**: Enriched credit profile with income, repayment history, and score insights.")
st.sidebar.markdown("### 💬 Feature Descriptions")

st.sidebar.markdown("""
- 🔄 **Negative Amortization**  
  Unpaid interest gets added to your loan balance over time.

- 💸 **Interest Only Period**  
  Borrower pays just the interest at the start, not the principal.

- 💰 **Lump Sum Payment**  
  A one-time big payment made before starting regular installments.
                    
- 🏦 **Credit Bureau Details**
  Refers to different credit bureaus that provide credit reports and scores in India.
  
""")


# Sidebar inputs
#Credit_Worthiness=st.sidebar.selectbox("Credit Worthiness",["l1","l2"])
loan_amount = st.sidebar.number_input(" 💵 Loan Amount")
term=st.sidebar.number_input("📅 Term")
#Neg_amortization=st.sidebar.selectbox("Neg_Ammortization")
income = st.sidebar.number_input(" 📥 Income")
#credit_type= st.sidebar.selectbox("Credit Type",["EXP", "EQUI", "CRIF", "CIB"])
Credit_Score = st.sidebar.slider("📊 Credit Score")

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