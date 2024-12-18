import streamlit as st
import requests

# Streamlit UI
st.title("Send Input to AI")

# Input Box for User Message
user_input = st.text_input("Enter pipeline runtime to send to the AI Response:")

# Webhook URL
webhook_url = "https://budgy.elastic.snaplogicdev.com/api/1/rest/slsched/feed/AutoSyncV2_QA/projects/Srikanth%20Varanasi/trigger%20Task?bearer_token=abc"  # Replace with your actual webhook URL

# Button to trigger webhook
if st.button("Submit"):
    if user_input:  # Ensure input is not empty
        payload = {
            "message": user_input,
            "user": "Streamlit User"  # You can add any additional data
        }
        try:
            # Sending the POST request to the webhook URL
            response = requests.post(webhook_url, json=payload)
            
            # Check if the response is successful
            if response.status_code == 200:
                st.success("Webhook sent successfully!")
                # Display the JSON response from the webhook
                try:
                    webhook_response = response.json()  # Try to parse the JSON response
                    st.json(webhook_response)  # Display the response data
                except ValueError:
                    st.write("Response received but not in JSON format.")
            else:
                st.error(f"Failed to send webhook. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a message before sending.")
