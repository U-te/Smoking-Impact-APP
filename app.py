import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Smoking Impact & Quit Calculator",
    page_icon="🚭",
    layout="centered",
)

# Hide default Streamlit menu/footer for a cleaner look
st.markdown(
    "<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>",
    unsafe_allow_html=True,
)

st.title("🚭 Smoking Impact & Quit Calculator")
st.caption("See how smoking may affect your life expectancy, and what quitting could give back.")

# ---------- Sidebar: adjustable assumptions ----------
with st.sidebar:
    st.header("⚙️ Assumptions")
    life_expectancy = st.slider("Baseline life expectancy (years)", 60, 90, 75)
    minutes_per_cig = st.slider("Minutes of life lost per cigarette", 5, 20, 11)
    recovery_pct = st.slider("Share of lost time recovered by quitting (%)", 0, 100, 50)
    st.caption("These are rough population-level estimates and can be changed.")

# ---------- Main ----------
smoke = st.radio("Do you currently smoke?", ("Yes", "No"), horizontal=True)

if smoke == "No":
    st.success("Great! Staying smoke-free is one of the best things you can do for your health ❤️")
else:
    with st.form("calc_form"):
        st.subheader("Your details")
        c1, c2 = st.columns(2)
        age = c1.number_input("Your age", min_value=10, max_value=100, value=30, step=1)
        years = c2.number_input("Years smoked", min_value=0, max_value=80, value=5, step=1)
        cigs = c1.number_input("Cigarettes per day", min_value=0, max_value=100, value=10, step=1)
        pack_cost = c2.number_input("Cost of a pack of 20 (Nu.)", min_value=0.0, value=150.0, step=10.0)
        quit_date = st.date_input("Planned quit date", min_value=date.today())
        submitted = st.form_submit_button("Calculate", use_container_width=True, type="primary")

    if submitted:
        if years > age:
            st.error("Years smoked cannot be greater than your age.")
        else:
            years_lost = years * cigs * 365 * minutes_per_cig / (60 * 24 * 365)
            recovered = years_lost * recovery_pct / 100
            remaining = life_expectancy - age - years_lost + recovered
            yearly_cost = cigs / 20 * pack_cost * 365
            days_to_quit = (quit_date - date.today()).days

            st.subheader("Your results")
            m1, m2, m3 = st.columns(3)
            m1.metric("Life lost so far", f"{years_lost:.2f} yrs")
            m2.metric("Recoverable by quitting", f"{recovered:.2f} yrs")
            m3.metric("Saved per year", f"Nu. {yearly_cost:,.0f}")

            st.divider()
            if remaining > 0:
                st.success(f"Estimated remaining life expectancy if you quit: **{remaining:.1f} years**")
            else:
                st.error("Smoking has severely reduced estimated life expectancy. Please speak to a doctor.")

            if days_to_quit == 0:
                st.info("🎯 Your quit date is today. You can do this!")
            else:
                st.info(f"📅 {days_to_quit} day(s) until your quit date.")

    st.caption("⚠️ These are general estimates for awareness only, not medical advice. "
               "Talk to a healthcare professional for personal guidance on quitting.")
