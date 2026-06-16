import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FIOS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def check_login():
    """Checks if the user is logged in."""
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        # --- LOGIN FORM ---
        st.title("FIOS - Login")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Check against secrets
            correct_username = st.secrets.get("LOGIN_USERNAME", "admin")
            correct_password = st.secrets.get("LOGIN_PASSWORD", "password")
            
            if username == correct_username and password == correct_password:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("The username or password you entered is incorrect.")
        
        return False
    return True

if check_login():
    # --- MAIN APP ---
    st.title("Financial Intelligence Overview System (FIOS)")
    st.write("Welcome to your daily financial brief. Use the sidebar to navigate to different pages.")
    
    st.info("Navigate to the **Today** page for your AI-powered daily brief or the **Equities** page to dive into specific stocks.", icon="👈")

    # --- FOOTER ---
    st.markdown("---")
    st.write("FIOS - v1.0.0")