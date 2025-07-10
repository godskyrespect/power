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


# if serial_on:
#   st.write("시리얼 통신 시작")
#   if not st.session_state.agent_id:
#     st.warning("Client와 연결되어 있지 않음.")
#   else:
#       send = requests.post(f"{SERVER_HTTP}/serial/on", json={"agent_id": st.session_state.agent_id})
#       while True:
#           try:
#               res = requests.get(f"{SERVER_HTTP}/serial", params={"agent_id": st.session_state.agent_id})
#               if res.status_code == 200:
#                   data = res.json()["serial_data"]
#                   if data:
#                       serial_area.text(st.session_state.serial_data.append(data))
#               time.sleep(1)
#           except Exception as e:
#               st.error(f"에러: {e}")
#               time.sleep(5)
#               break
# else:
#   if st.session_state.agent_id:
#     get = requests.post(f"{SERVER_HTTP}/serial/off", json={"agent_id": st.session_state.agent_id})  

# serial_area.text(st.session_state.serial_data)

st.markdown("""
아래 버튼을 누르고 포트를 선택하면, 시리얼 데이터가 웹 브라우저 내에서 바로 표시됩니다.  
(크롬/엣지/브레이브 등 최신 브라우저만 지원)
""")

serial_html = """
<button id="connect">시리얼 연결</button>
<pre id="output" style="background:black; color:lime; height:300px; overflow:auto"></pre>
<script>
let port;
let reader;
document.getElementById('connect').onclick = async () => {
  if (!('serial' in navigator)) {
    alert('이 브라우저는 Web Serial API를 지원하지 않습니다.');
    return;
  }
  try {
    port = await navigator.serial.requestPort();
    await port.open({ baudRate: 9600 });
    document.getElementById('output').textContent += '[연결됨]\\n';
    reader = port.readable.getReader();
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      if (value) {
        const text = new TextDecoder().decode(value);
        document.getElementById('output').textContent += text;
        document.getElementById('output').scrollTop = document.getElementById('output').scrollHeight;
      }
    }
  } catch(e) {
    document.getElementById('output').textContent += '\\n에러: ' + e + '\\n';
  }
};
</script>
"""

with st.container():
    st.markdown("### 📡 시리얼 모니터 컨테이너")
    st.components.v1.html(serial_html, height=350)
