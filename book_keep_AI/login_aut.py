
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
import app as main_app
# Load the YAML config
with open(r'C:\Users\felix\bookkeeper_ai\Book_keeper_AI\book_keep_AI\config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create the authenticator (✅ removed deprecated 'pre-authorized')
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']

)

if st.session_state.get("authentication_status") is None:
    st.title("📚 Welcome to RoboLedger! 📚")
    st.subheader("Please log in to continue")

authenticator.login()


if st.session_state.get('authentication_status'):
    authenticator.logout()
    st.title("🧠📊 RoboLedger 📊🧠")
    main_app.run()  # Call the main app function
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    pass  # Do nothing if not authenticated
