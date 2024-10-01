import streamlit as st
import requests

url = "http://127.0.0.1:8000/budget_planner"

# Initialize session state for investments if not already present
if 'investments_selected' not in st.session_state:
    st.session_state.investments_selected = None

if 'investment_amounts' not in st.session_state:
    st.session_state.investment_amounts = {}

st.title(":red[BUDGET BUDDY ] :) :blue[$$]")

with st.form("budget_plan_form", border=True):
    monthly_income = st.number_input("**Monthly Income**", value=0, placeholder="Enter your monthly income")
    eb_bill = st.number_input("**EB Bill**", value=0)
    rent = st.number_input("**Rent**", value=0)
    groceries = st.number_input("**Groceries**", value=0)
    travel = st.number_input("**Travel**", value=0)
    internet = st.number_input("**Internet/Wifi**", value=0)
    emis = st.number_input("**EMIs**", value=0)
    investments = st.radio("**Do you have any investments or savings?**", ["Yes", "No"], index=0)
    
    st.session_state.investments_selected = investments

    # Multiselect and amount inputs for investments if "Yes" is selected
    if st.session_state.investments_selected == "Yes":
        selected_investments = st.multiselect(
            "What investments and savings have you done so far?",
            ["Mutual Funds", "Stocks", "Liquid Cash", "Fixed/Recurring Deposits", "Insurances", "Post Office Schemes"]
        )

        # Capture amounts for each selected investment
        investment_amounts = {}
        for investment in selected_investments:
            investment_amounts[investment] = st.number_input(f"Enter the amount for {investment}", value=0)
        
        # Update session state with the amounts
        st.session_state.investment_amounts = investment_amounts
    else:
        st.session_state.investment_amounts = {}

    # Submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        # Prepare the payload to send to FastAPI
        payload = {
            "monthly_income": monthly_income,
            "eb_bill": eb_bill,
            "rent": rent,
            "groceries": groceries,
            "travel": travel,
            "internet": internet,
            "EMIs": emis,
            "existing_investments": st.session_state.investments_selected == "Yes",
            "investments": [
                {"investment_types": inv, "total_amount": amt} 
                for inv, amt in st.session_state.investment_amounts.items() if amt > 0
            ]if st.session_state.investments_selected == "Yes" else []
        }

        # Send POST request to FastAPI
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            st.success("Budget plan calculated successfully!")
            st.write(response.json())  # Display the response from FastAPI
        else:
            st.error("Error in calculating budget plan.")
            st.write(response.json())