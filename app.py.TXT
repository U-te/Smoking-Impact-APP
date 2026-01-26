import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Smoking Impact & Quit Calculator",
    page_icon="🚭"
)

st.title("🚭 Smoking Impact & Quit Calculator")

smoke = st.radio("Do you smoke?", ("Yes", "No"))

if smoke == "Yes":
    years = st.number_input("Years smoked", min_value=0, step=1)
    cigs = st.number_input("Cigarettes per day", min_value=0, step=1)
    age = st.number_input("Your age", min_value=0, step=1)
    quit_date = st.date_input("Planned quit date", min_value=date.today())

    if st.button("Calculate"):
        minutes_lost = years * cigs * 365 * 11
        years_lost = minutes_lost / (60 * 24 * 365)

        life_expectancy = 75
        remaining = life_expectancy - age - years_lost
        recovered = years_lost * 0.5

        st.subheader("Results")
        st.write(f"Years of life lost: **{years_lost:.2f}**")
        st.write(f"Life recovered by quitting: **{recovered:.2f}**")

        if remaining > 0:
            st.success(f"Estimated remaining life expectancy: **{remaining + recovered:.2f} years**")
        else:
            st.error("Smoking has severely reduced life expectancy.")

else:
    st.success("Great! Staying smoke-free saves lives ❤️")

