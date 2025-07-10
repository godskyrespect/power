# ui.py
import streamlit as st
import requests

SERVER_HTTP = "http://16.176.5.74:8000"  # ex: http://myserver.com
if "serial_data" not in st.session_state:
  st.session_state.serial_data = []
st.title("🚀 Arduino Cloud 업로더")

if "agent_id" not in st.session_state:
  st.session_state.agent_id = ""

code = st.text_area("코드 입력", """
void setup() {
  Serial.begin(9600);
}
void loop() {
  Serial.println("Hello!");
  delay(1000);
}
""", height=200)

port = st.text_input("포트", "/dev/ttyACM0")
fqbn = st.text_input("보드 FQBN", "arduino:avr:uno")
st.session_state.agent_id = st.text_input("Agent ID",placeholder="ASTDIO-")

st.write("현재 통신 AGENT ID : ", st.session_state.agent_id)
