# ui.py
import streamlit as st
import requests

SERVER_HTTP = "http://16.176.5.74:8000"  # ex: http://myserver.com

st.title("🚀 Arduino Cloud 업로더")

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
agent_id = st.text_input("Agent ID", "ASTDIO-")

if st.button("📤 업로드"):
    res = requests.post(f"{SERVER_HTTP}/upload", json={
        "agent_id": agent_id,
        "code": code,
        "fqbn": fqbn,
        "port": port
    })

    if res.status_code == 200:
        st.success(f"✅ 업로드 명령 전송 완료({res.text})")
    else:
        st.error("❌ 업로드 실패")
        st.text(res.text)
