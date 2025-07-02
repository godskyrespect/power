import streamlit as st
import streamlit.components.v1 as components

st.title("💬 아두이노 시리얼 통신 (Web Serial API)")

components.html("""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
</head>
<body>
  <h3>🛠 브라우저 기반 시리얼 통신</h3>
  <button id="connect">🔌 연결</button>
  <span id="status">상태: 미연결</span><br><br>

  <input id="command" placeholder="보낼 명령어" />
  <button id="send">📤 전송</button>

  <h4>📥 수신 결과:</h4>
  <pre id="output"></pre>

<script>
let port, writer, reader;

document.getElementById('connect').addEventListener('click', async () => {
  try {
    port = await navigator.serial.requestPort();
    await port.open({ baudRate: 9600 });
    document.getElementById('status').textContent = "상태: 연결됨";

    const encoder = new TextEncoderStream();
    encoder.readable.pipeTo(port.writable);
    writer = encoder.writable.getWriter();

    const decoder = new TextDecoderStream();
    port.readable.pipeTo(decoder.writable);
    reader = decoder.readable.getReader();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      document.getElementById('output').textContent += value;
    }
  } catch (err) {
    console.error("연결 실패:", err);
    document.getElementById('status').textContent = "상태: 연결 실패";
  }
});

document.getElementById('send').addEventListener('click', async () => {
  if (!writer) return;
  const text = document.getElementById('command').value;
  await writer.write(text + "\\n");
});
</script>
</body>
</html>
""", height=500)
