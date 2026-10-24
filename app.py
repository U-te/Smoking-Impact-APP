import streamlit as st
from datetime import date

st.set_page_config(page_title="Smoking Impact & Quit Calculator", page_icon="🚭", layout="centered")

st.markdown("""
<style>
#MainMenu, footer {visibility: hidden;}
.block-container {padding-top: 2rem; max-width: 760px;}
.hero {background: linear-gradient(135deg,#0f766e,#14b8a6); padding: 28px 24px;
       border-radius: 16px; margin-bottom: 24px;}
.hero h1 {margin: 0; font-size: 1.9rem; color: #ffffff;}
.hero p {margin: 6px 0 0; color: #ecfeff;}
.card {background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px;
       padding: 18px 10px; text-align: center; margin-bottom: 10px;}
.card .v {font-size: 1.6rem; font-weight: 700; color: #0f766e;}
.card .l {font-size: .85rem; color: #475569;}
.card.red .v {color: #dc2626;}
.banner {border-radius: 12px; padding: 16px 18px; margin: 12px 0; font-size: 1.05rem;}
.banner.good {background: #dcfce7; color: #166534;}
.banner.bad {background: #fee2e2; color: #991b1b;}
.banner.info {background: #e0f2fe; color: #075985;}
div[data-testid="stFormSubmitButton"] > button {border-radius: 10px; font-weight: 600; padding: .6rem;}
</style>
<div class="hero">
  <h1>🚭 Smoking Impact & Quit Calculator</h1>
  <p>See how smoking may affect your life expectancy, and what quitting could give back.</p>
</div>
""", unsafe_allow_html=True)


def card(col, value, label, red=False):
    col.markdown(
        f'<div class="card {"red" if red else ""}"><div class="v">{value}</div>'
        f'<div class="l">{label}</div></div>',
        unsafe_allow_html=True,
    )


def banner(text, kind):
    st.markdown(f'<div class="banner {kind}">{text}</div>', unsafe_allow_html=True)


with st.sidebar:
    st.header("⚙️ Assumptions")
    life_expectancy = st.slider("Baseline life expectancy (years)", 60, 90, 75)
    minutes_per_cig = st.slider("Minutes of life lost per cigarette", 5, 20, 11)
    recovery_pct = st.slider("Share of lost time recovered by quitting (%)", 0, 100, 50)
    st.caption("Rough population-level estimates. Adjust as needed.")

smoke = st.radio("Do you currently smoke?", ("Yes", "No"), horizontal=True)

if smoke == "No":
    banner("🎉 Great! Staying smoke-free is one of the best things you can do for your health.", "good")
else:
    with st.form("calc_form"):
        st.subheader("Your details")
        c1, c2 = st.columns(2)
        age = c1.number_input("Your age", min_value=10, max_value=100, value=30, step=1)
        years = c2.number_input("Years smoked (0.5 = 6 months)", min_value=0.0, max_value=80.0, value=5.0, step=0.5)
        cigs = c1.number_input("Cigarettes per day", min_value=0, max_value=100, value=10, step=1)
        pack_cost = c2.number_input("Cost of a pack of 20 (Nu.)", min_value=0.0, value=150.0, step=10.0)
        quit_date = st.date_input("Planned quit date", min_value=date.today())
        submitted = st.form_submit_button("Calculate", use_container_width=True, type="primary")

    if submitted:
        if years > age:
            banner("⚠️ Years smoked cannot be greater than your age.", "bad")
        else:
            years_lost = years * cigs * 365 * minutes_per_cig / (60 * 24 * 365)
            recovered = years_lost * recovery_pct / 100
            remaining = life_expectancy - age - years_lost + recovered
            yearly_cost = cigs / 20 * pack_cost * 365
            days_to_quit = (quit_date - date.today()).days

            st.subheader("Your results")
            m1, m2, m3 = st.columns(3)
            card(m1, f"{years_lost:.2f} yrs", "Life lost so far", red=True)
            card(m2, f"{recovered:.2f} yrs", "Recoverable by quitting")
            card(m3, f"Nu. {yearly_cost:,.0f}", "Spent per year")

            if remaining > 0:
                banner(f"✅ Estimated remaining life expectancy if you quit: <b>{remaining:.1f} years</b>", "good")
            else:
                banner("❗ Estimated life expectancy is severely reduced. Please speak to a doctor.", "bad")

            if days_to_quit == 0:
                banner("🎯 Your quit date is today. You can do this!", "info")
            else:
                banner(f"📅 {days_to_quit} day(s) until your quit date.", "info")

    st.caption("⚠️ General estimates for awareness only, not medical advice. "
               "Talk to a healthcare professional for personal guidance on quitting.")
