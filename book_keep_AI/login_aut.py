
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

with st.expander("Don't have an account? Create one"):
    new_username = st.text_input("Choose a username")
    new_name = st.text_input("Your full name")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_password != confirm_password:
            st.error("Passwords do not match.")
        elif new_username in config['credentials']['usernames']:
            st.error("Username already exists.")
        elif not new_username or not new_password:
            st.error("Username and password cannot be empty.")
        else:
            config['credentials']['usernames'][new_username] = {
                'name': new_name,
                'email': new_email,
                'password': new_password
            }

            # Save new credentials back to config.yaml
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)

            st.success("Account created! You can now log in.")


