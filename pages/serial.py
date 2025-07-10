# ui.py
import streamlit as st
import requests, time

SERVER_HTTP = "http://16.176.5.74:8000"  # ex: http://myserver.com
if "serial_data" not in st.session_state:
  st.session_state.serial_data = []
st.title("🚀 Arduino Cloud 시리얼 통신")

if "agent_id" not in st.session_state:
  st.session_state.agent_id = ""

port = st.text_input("포트", "/dev/ttyACM0")
fqbn = st.text_input("보드 FQBN", "arduino:avr:uno")
st.session_state.agent_id = st.text_input("Agent ID",placeholder="ASTDIO-")
serial_on = st.toggle("시리얼 통신 영역 전개")

st.write("현재 통신 AGENT ID : ", st.session_state.agent_id)
st.divider()

serial_area = st.empty()

if serial_on:
  st.write("시리얼 통신 시작")
  if not st.session_state.agent_id:
    st.warning("Client와 연결되어 있지 않음.")
  else:
      send = requests.get(f"{SERVER_HTTP}/serial/on", json={"agent_id": st.session_state.agent_id})
      while True:
          try:
              res = requests.get(f"{SERVER_HTTP}/serial", params={"agent_id": st.session_state.agent_id})
              if res.status_code == 200:
                  data = res.json()["serial_data"]
                  if data:
                      serial_area.text('\n'.join(data))
              time.sleep(1)
          except Exception as e:
              st.error(f"에러: {e}")
              time.sleep(5)
              
              break
      get = requests.post(f"{SERVER_HTTP}/serial/off", json={"agent_id": st.session_state.agent_id})
