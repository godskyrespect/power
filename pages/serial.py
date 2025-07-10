# ui.py
import streamlit as st
import requests

SERVER_HTTP = "http://16.176.5.74:8000"  # ex: http://myserver.com
if "serial_data" not in st.session_state:
  st.session_state.serial_data = []
st.title("🚀 Arduino Cloud 시리얼 통신")

if "agent_id" not in st.session_state:
  st.session_state.agent_id = ""

port = st.text_input("포트", "/dev/ttyACM0")
fqbn = st.text_input("보드 FQBN", "arduino:avr:uno")
st.session_state.agent_id = st.text_input("Agent ID",placeholder="ASTDIO-")

st.write("현재 통신 AGENT ID : ", st.session_state.agent_id)
st.divider()
