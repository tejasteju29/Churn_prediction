import streamlit as st
import joblib
import pandas as pd

# Load model
model = joblib.load("churn_model.pkl")

st.set_page_config(page_title="Churn Prediction App", layout="wide")

st.title("📊 Customer Churn Prediction Dashboard")
st.write("Predict whether a customer will churn based on their behavior.")

# Sidebar Inputs
st.sidebar.header("Enter Customer Details")

age = st.sidebar.slider("Age", 18, 65, 30)
tenure = st.sidebar.slider("Tenure (Months)", 1, 60, 12)
usage = st.sidebar.slider("Usage Frequency", 1, 30, 10)
support = st.sidebar.slider("Support Calls", 0, 10, 2)
delay = st.sidebar.slider("Payment Delay", 0, 30, 5)
spend = st.sidebar.slider("Total Spend", 100, 1000, 500)
interaction = st.sidebar.slider("Last Interaction", 1, 30, 10)

gender = st.sidebar.selectbox("Gender", ["Female", "Male"])
subscription = st.sidebar.selectbox("Subscription Type", ["Basic", "Standard", "Premium"])
contract = st.sidebar.selectbox("Contract Length", ["Monthly", "Quarterly", "Yearly"])

# Convert categorical variables
data = {
    "Age": age,
    "Tenure": tenure,
    "Usage Frequency": usage,
    "Support Calls": support,
    "Payment Delay": delay,
    "Total Spend": spend,
    "Last Interaction": interaction,
    "Gender_Male": 1 if gender == "Male" else 0,
    "Subscription Type_Premium": 1 if subscription == "Premium" else 0,
    "Subscription Type_Standard": 1 if subscription == "Standard" else 0,
    "Contract Length_Monthly": 1 if contract == "Monthly" else 0,
    "Contract Length_Quarterly": 1 if contract == "Quarterly" else 0
}

input_df = pd.DataFrame([data])

# Prediction
if st.button("🔮 Predict Churn"):

    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]

    st.subheader("Prediction Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Churn Probability", f"{prob*100:.2f}%")

    with col2:
        if prediction == 1:
            st.error("⚠️ High Risk: Customer Likely to Churn")
        else:
            st.success("✅ Low Risk: Customer Will Stay")

    st.progress(int(prob * 100))

    # ---------------------------
    # Reason for Churn Analysis
    # ---------------------------

    st.subheader("📌 Possible Reasons for Churn")

    reasons = []

    if delay > 15:
        reasons.append("⏰ High Payment Delay")

    if support > 5:
        reasons.append("📞 Too Many Support Calls")

    if usage < 5:
        reasons.append("📉 Low Product Usage")

    if tenure < 6:
        reasons.append("🆕 New Customer (Low Loyalty)")

    if spend < 300:
        reasons.append("💰 Low Spending Customer")

    if interaction > 20:
        reasons.append("⌛ Long Time Since Last Interaction")

    if subscription == "Basic":
        reasons.append("📦 Basic Subscription Plan")

    if contract == "Monthly":
        reasons.append("📄 Short Contract Length")

    # Display reasons
    if prediction == 1:
        if len(reasons) > 0:
            st.warning("Customer may churn due to the following reasons:")
            for r in reasons:
                st.write("•", r)
        else:
            st.info("Model predicts churn but no strong rule-based reason detected.")
    else:
        st.success("Customer behavior indicates low churn risk.")