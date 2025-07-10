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
아래에서 **시리얼 연결/해제**를 클릭해 USB 시리얼 장치와 연결하세요.<br>
실시간 수신 데이터가 아래 박스에 표시됩니다.<br>
(Chrome/Edge/Brave 등 최신 브라우저만 지원)
""", unsafe_allow_html=True)

serial_html = """
<div style="max-width:430px; margin:0 auto;">
  <div id="status" style="padding:8px 12px; border-radius:8px; border:1px solid #ccc; background:#f5f5f5; margin-bottom:10px; color:#333;">
    <b>상태</b>: 연결되지 않음
  </div>
  <div style="display:flex; gap:10px; margin-bottom:10px;">
    <button id="connect" style="padding:8px 20px; border-radius:6px; border:none; background:#2674ff; color:#fff; font-weight:bold;">연결</button>
    <button id="disconnect" style="padding:8px 20px; border-radius:6px; border:none; background:#ccc; color:#444; font-weight:bold;">해제</button>
  </div>
  <div style="border:1.5px solid #2674ff; border-radius:10px; background:rgba(230,240,255,0.8); min-height:220px; max-height:300px; overflow-y:auto; font-family:monospace; font-size:1.05em; color:#19355a; padding:10px;" id="output"></div>
</div>
<script>
let port;
let reader;
let keepReading = false;

function setStatus(msg, color="#333") {
  let st = document.getElementById('status');
  st.innerHTML = "<b>상태</b>: " + msg;
  st.style.color = color;
}

// 연결 버튼
document.getElementById('connect').onclick = async () => {
  if (!('serial' in navigator)) {
    setStatus('Web Serial API 미지원 브라우저입니다.', "#d60000");
    return;
  }
  try {
    port = await navigator.serial.requestPort();
    await port.open({ baudRate: 9600 });
    setStatus("연결됨", "#2674ff");
    document.getElementById('output').innerHTML += '<div style="color:#2674ff;">[연결됨]</div>';
    keepReading = true;
    reader = port.readable.getReader();
    while (keepReading) {
      const { value, done } = await reader.read();
      if (done || !keepReading) break;
      if (value) {
        const text = new TextDecoder().decode(value);
        let div = document.createElement('div');
        div.textContent = text;
        document.getElementById('output').appendChild(div);
        document.getElementById('output').scrollTop = document.getElementById('output').scrollHeight;
      }
    }
    reader.releaseLock();
    setStatus("연결해제됨", "#888");
  } catch(e) {
    setStatus("에러: " + e, "#d60000");
  }
};

// 해제 버튼
document.getElementById('disconnect').onclick = async () => {
  keepReading = false;
  if (reader) {
    try { await reader.cancel(); } catch {}
    reader = null;
  }
  if (port) {
    try { await port.close(); } catch {}
    port = null;
  }
  setStatus("연결해제됨", "#888");
  document.getElementById('output').innerHTML += '<div style="color:#888;">[연결 해제됨]</div>';
};
</script>
"""

with st.container():
    st.components.v1.html(serial_html, height=400)
