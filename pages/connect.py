# ui.py
import streamlit as st
import requests

SERVER_HTTP = "http://16.176.5.74:8000"  # ex: http://myserver.com

if "key" not in st.session_state:
  st.session_state.key = ""

if "info" not in st.session_state:
  st.session_state.info = ""
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

agent_id = st.text_input("Agent ID", "ASTDIO-")

if st.button("📤 아두이노 클라이언트 연결하기"):
    res = requests.post(f"{SERVER_HTTP}/connect", json={
        "agent_id": agent_id,
    })

    if res.status_code == 200:
        result = res.json()
        if res:
            st.success(f"✅ 연결 성공: {result['status']}")
            st.session_state.key = agent_id
        with st.spinner("아두이노 정보를 가져오는 중입니다..."):
          response = requests.post(f"{SERVER_HTTP}/arduino_info", json={"agent_id": st.session_state.key})
          infos = response.json()['output']
          for item in infos["detected_ports"]:
          if "matching_boards" in item:
              for board in item["matching_boards"]:
                  name = board["name"]
                  fqbn = board["fqbn"]
                  address = item["port"]["address"]
                  protocol_label = item["port"]["protocol_label"]
                  st.session_state.info = {"Name": name, "fqbn": fqbn, "Port": address, "Type": protocol_label}

        st.json(st.session_state.info)
    else:
        st.error(f"❌ 연결 실패 : {res.json()['error']}")
