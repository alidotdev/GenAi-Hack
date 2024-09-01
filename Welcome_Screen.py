import streamlit as st

# Custom CSS for the professional design
st.markdown(
    """
    <style>
    .header-container {
        background: linear-gradient(135deg, #2b5876, #4e4376);
        padding: 50px;
        border-radius: 10px;
        text-align: center;
        color: white;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
    }
    .header-text {
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .subtext {
        font-size: 18px;
        margin-top: 0;
    }
    .button-container {
        text-align: center;
        margin-top: 30px;
    }
    .stButton>button {
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
        background-color: #4e4376;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2b5876;
        color: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header container with a gradient background and centered text
st.markdown(
    """
    <div class="header-container">
        <div class="header-text">Welcome to English Learning AI Bot</div>
        <p class="subtext">Enhance your English skills with AI-powered guidance.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Centered button to start the interaction
st.markdown(
    """
    <div class="button-container">
        <p>Click the button below to get started:</p>
    </div>
    """,
    unsafe_allow_html=True
)

if st.button("Get Started"):
    st.write("Let's begin your English learning journey!")

# Additional Streamlit elements can go here
