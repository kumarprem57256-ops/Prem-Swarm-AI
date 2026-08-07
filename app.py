from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
from brain import LocalOllamaBrain

messages_queue = []

def on_ai_thought(thought_msg):
    messages_queue.append({
        "sender": "NEXUS OLLAMA CORE",
        "message": thought_msg,
        "timestamp": time.strftime("%H:%M:%S")
    })

brain = LocalOllamaBrain(callback_func=on_ai_thought)
brain.start_thought_loop()

class SwarmHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NEXUS AI - Prem Swarm Core</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Inter', sans-serif; background: #070913; color: #e2e8f0; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 10px; }
        .cyber-container { width: 100%; max-width: 850px; background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 16px; box-shadow: 0 0 30px rgba(0,0,0,0.8); padding: 20px; display: flex; flex-direction: column; height: 90vh; }
        .header { text-align: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 15px; margin-bottom: 15px; }
        .header h1 { font-family: 'Orbitron', sans-serif; font-size: 20px; color: #38bdf8; letter-spacing: 1.5px; }
        .status-badge { display: inline-flex; align-items: center; gap: 8px; font-size: 12px; color: #4ade80; background: rgba(74, 222, 128, 0.1); padding: 4px 12px; border-radius: 20px; margin-top: 8px; }
        .dot { width: 8px; height: 8px; background: #4ade80; border-radius: 50%; box-shadow: 0 0 8px #4ade80; }
        
        #chat-box { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 14px; }
        .msg { max-width: 85%; padding: 12px 16px; border-radius: 14px; font-size: 14px; line-height: 1.5; white-space: pre-wrap; }
        .ai-msg { background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(56, 189, 248, 0.3); align-self: flex-start; color: #f1f5f9; }
        .user-msg { background: linear-gradient(135deg, #0284c7, #2563eb); align-self: flex-end; color: #ffffff; }
        .sender-tag { font-family: 'Orbitron', sans-serif; font-size: 10px; color: #38bdf8; margin-bottom: 4px; display: block; }
        
        .input-area { display: flex; gap: 10px; margin-top: 15px; background: rgba(15, 23, 42, 0.9); padding: 8px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); }
        input[type=text] { flex: 1; background: transparent; border: none; outline: none; padding: 10px; color: #fff; font-size: 14px; }
        button { background: #38bdf8; color: #070913; border: none; padding: 10px 24px; border-radius: 8px; font-family: 'Orbitron', sans-serif; font-weight: 700; cursor: pointer; }
    </style>
</head>
<body>
    <div class="cyber-container">
        <div class="header">
            <h1>⚡ NEXUS AUTONOMOUS CORE (OLLAMA LLM)</h1>
            <div class="status-badge"><span class="dot"></span> LOCAL AI MIND ACTIVE</div>
        </div>

        <div id="chat-box"></div>

        <div class="input-area">
            <input type="text" id="userInput" placeholder="Sawal pucho ya coding karwao..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">SEND</button>
        </div>
    </div>

    <script>
        setInterval(async () => {
            let res = await fetch('/get_messages');
            let data = await res.json();
            let chatBox = document.getElementById('chat-box');
            
            data.forEach(msg => {
                let div = document.createElement('div');
                div.className = 'msg ai-msg';
                div.innerHTML = `<span class="sender-tag">[${msg.timestamp}] ${msg.sender}</span>${msg.message}`;
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            });
        }, 1500);

        async function sendMessage() {
            let input = document.getElementById('userInput');
            let text = input.value.trim();
            if(!text) return;

            let chatBox = document.getElementById('chat-box');
            let div = document.createElement('div');
            div.className = 'msg user-msg';
            div.innerHTML = text;
            chatBox.appendChild(div);

            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            let res = await fetch('/user_speak', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            let data = await res.json();
            
            let aiDiv = document.createElement('div');
            aiDiv.className = 'msg ai-msg';
            aiDiv.innerHTML = `<span class="sender-tag">[NEXUS AI]</span>${data.reply}`;
            chatBox.appendChild(aiDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>"""
            self.wfile.write(html.encode("utf-8"))

        elif self.path == "/get_messages":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            global messages_queue
            response_data = json.dumps(messages_queue)
            messages_queue = [] 
            self.wfile.write(response_data.encode("utf-8"))

    def do_POST(self):
        if self.path == "/user_speak":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            ai_reply = brain.process_user_input(data['message'])
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"reply": ai_reply}).encode("utf-8"))

if __name__ == "__main__":
    print("🚀 NEXUS Autonomous Swarm Running on http://127.0.0.1:8080")
    server = HTTPServer(('127.0.0.1', 8080), SwarmHandler)
    server.serve_forever()
