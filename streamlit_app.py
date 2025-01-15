import streamlit as st
import requests
import pandas as pd
from io import StringIO

# Streamlit UI
st.title("Send Input to AI")

# Input Box for Runtime
runtime_input = st.text_input("Enter pipeline runtime to send to the AI Response:")

# Input Box for Organization Name (OrgName)
org_name = st.text_input("Enter the Organization Name (OrgName):")

# Input Box for POD with full path
pod_path = st.text_input("Enter POD with full path:")

# Webhook URL
webhook_url = "https://elastic.snaplogic.com/api/1/rest/slsched/feed/QA/qa_diagnostic_space/GenAI_diagnostic/triggerErrorAnalysisTask?bearer_token=abc"  # Replace with your actual webhook URL

# Button to trigger webhook
if st.button("Submit"):
    if runtime_input and org_name and pod_path:  # Ensure all inputs are not empty
        payload = {
            "runtime": runtime_input,  # Replaced 'message' with 'runtime'
            "org_name": org_name,      # Add OrgName to the payload
            "pod_path": pod_path,      # Add POD with full path to the payload
            "user": "Streamlit User"   # You can add any additional data
        }
        try:
            # Sending the POST request to the webhook URL
            response = requests.post(webhook_url, json=payload)
            
            # Check if the response is successful
            if response.status_code == 200:
                st.success("Webhook sent successfully!")
                
                # Check if the response is in CSV format
                content_type = response.headers.get('Content-Type')
                if 'csv' in content_type:
                    # Read CSV content from response
                    csv_data = StringIO(response.text)
                    df = pd.read_csv(csv_data)
                    
                    # Display the CSV data as a table
                    st.write("Response as CSV:")
                    st.dataframe(df)  # Display as a dataframe
                else:
                    st.write("Response received is not in CSV format.")
            else:
                st.error(f"Failed to send webhook. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter all fields (runtime, Organization Name, and POD path) before submitting.")
