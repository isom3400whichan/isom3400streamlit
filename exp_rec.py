import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Personal Expense Tracker")

# to keep track of data from previous sessions --> Session State
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

with st.form('expense_form'):
    st.subheader("Add New Expense")
    date = st.date_input("Date")
    category = st.selectbox("Category", ['Food', 'Transport', 'Entertainment', 'Bills', 'Other']) #create list of options to choose
    amount = st.number_input("Amount", min_value = 0.00, step=0.01) #step controls how much the +/- button changes
    desc = st.text_input("Description")

    add_expense_button = st.form_submit_button9('Add Expense')

    if add_expense_button: # if all the input items are input correctly
        new_expense = pd.DataFrame({
            'Date': [date],
            "Category": [category],
            'Amount': [amount],
            'Descriptoin': [desc]
        })

        st.session_states.expenses = pd.concat({st.session_state.expenses, new_expense}, ignore_index = True)
        st.success("Expense added!")

if not st.session_state.expenses.empty:
    st.subheader("Your Expenses")
    st.dataframe(st.session_state.expenses)

    st.subheader("Summary")
    total_spent = st.session_state.expenses['Amount'].sum() # Add all the values from "Amount" column in the table
    st.write(f"Total Spent: ${total_spent:.2f}")

    # Calculate total amount spent by each category
    category_total = st.session_state.expenses.groupby('Category')['Amount'].sum()

    fig, ax = plt.subplots(figsize=(10,6))
    ax.pie(category_total.values, labels=category_total.index, autopct='%1.1f%%')

    ax.set_title('Expenses by Category')
    st.pyplot(fig)
else:
    st.info("No expenses recorded yet. Please enter expense.")
