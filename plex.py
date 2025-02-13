import streamlit as st
import requests
import threading
from streamlit_autorefresh import st_autorefresh

# API endpoints (Replace with actual URLs)
CREATE_NODES_API = "https://your-api-endpoint.com/create"
DELETE_NODES_API = "https://your-api-endpoint.com/delete"

# Auto-refresh to prevent session timeout
st_autorefresh(interval=60000, key="keep_alive")  # Refresh every 60 seconds

@st.cache_resource
def create_nodes(snapplex, num_nodes, pod, fm_nodes, org_name):
    payload = {"snapplex": snapplex, "num_nodes": num_nodes, "pod": pod, "fm_nodes": fm_nodes, "org_name": org_name}
    response = requests.post(CREATE_NODES_API, json=payload)
    return response.json()

@st.cache_resource
def delete_nodes(snapplex, pod, org_name):
    payload = {"snapplex": snapplex, "pod": pod, "org_name": org_name}
    response = requests.post(DELETE_NODES_API, json=payload)
    return response.json()

def long_running_task():
    import time
    time.sleep(30)  # Simulating a long task

# Streamlit UI
st.title("SnapLogic Node Management")

option = st.radio("Choose an action:", ["Create Nodes", "Delete Nodes"])

# POD Selection
pod = st.selectbox("Select POD:", ["snap", "pigeon", "canary", "budgy", "stage"])
org_name = st.text_input("Enter Organization Name:")

if option == "Create Nodes":
    snapplex = st.text_input("Enter Snapplex Name:")
    num_nodes = st.number_input("Enter Number of Nodes:", min_value=1, step=1)
    fm_nodes = st.number_input("Enter Number of FM Nodes:", min_value=0, step=1)
    
    if st.button("Create Nodes"):
        if snapplex and num_nodes and org_name:
            threading.Thread(target=long_running_task).start()  # Run long task in background
            response = create_nodes(snapplex, num_nodes, pod, fm_nodes, org_name)
            st.success(f"Nodes Created: {response}")
        else:
            st.error("Please enter all required fields.")

elif option == "Delete Nodes":
    snapplex = st.text_input("Enter Snapplex Name:")
    
    if st.button("Delete Nodes"):
        if snapplex and org_name:
            threading.Thread(target=long_running_task).start()  # Run long task in background
            response = delete_nodes(snapplex, pod, org_name)
            st.success(f"Nodes Deleted: {response}")
        else:
            st.error("Please enter Snapplex Name and Organization Name.")

# Footer to indicate app ownership
st.markdown("---")
st.markdown("### App created by QA Team")
