import sqlite3
import os
import json
import urllib.request
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prem Swarm AI - Supreme Matrix Engine</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background-color: #08090c; color: #e6edf3; padding: 12px; display: flex; flex-direction: column; gap: 14px; min-height: 100vh; }
        
        .header { display: flex; align-items: center; justify-content: space-between; background: #111318; border: 1px solid #1f242d; border-radius: 12px; padding: 12px 16px; }
        .brand { font-weight: 700; font-size: 16px; background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .badge { background: #1a1e26; border: 1px solid #2d333f; color: #38bdf8; font-size: 11px; padding: 4px 10px; border-radius: 20px; font-weight: 600; }

        .card { background: #111318; border: 1px solid #1f242d; border-radius: 12px; padding: 14px; }
        .card-title { font-size: 12px; font-weight: 600; color: #8b949e; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 10px; }
        
        .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .stat-box { background: #08090c; border: 1px solid #1a1e26; padding: 10px; border-radius: 8px; text-align: center; }
        .stat-val { font-size: 20px; font-weight: 700; color: #38bdf8; margin-top: 2px; }

        .chat-container { display: flex; flex-direction: column; height: 340px; background: #08090c; border: 1px solid #1a1e26; border-radius: 10px; overflow: hidden; }
        #chat-box { flex: 1; overflow-y: auto; padding: 12px; display: flex; flex-direction: column; gap: 10px; }
        
        .msg { max-width: 88%; padding: 10px 14px; border-radius: 12px; font-size: 13px; line-height: 1.5; word-wrap: break-word; }
        .user-msg { align-self: flex-end; background: #2563eb; color: #ffffff; border-bottom-right-radius: 2px; }
        .ai-msg { align-self: flex-start; background: #161b22; color: #e6edf3; border: 1px solid #21262d; border-bottom-left-radius: 2px; }

        .input-bar { display: flex; gap: 8px; padding: 10px; background: #111318; border-top: 1px solid #1f242d; }
        input[type="text"] { flex: 1; background: #08090c; border: 1px solid #2d333f; color: #fff; padding: 10px 14px; border-radius: 20px; outline: none; font-size: 13px; }
        input[type="text"]:focus { border-color: #38bdf8; }
        
        .btn { border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-weight: 600; font-size: 12px; }
        .btn-send { background: linear-gradient(135deg, #2563eb, #7c3aed); color: #fff; }
        .btn-mic { background: #1a1e26; border: 1px solid #2d333f; color: #f59e0b; }

        .table-wrapper { overflow-x: auto; margin-top: 6px; }
        table { width: 100%; border-collapse: collapse; font-size: 11px; text-align: left; }
        th, td { padding: 8px 10px; border-bottom: 1px solid #1a1e26; }
        th { color: #8b949e; font-weight: 600; background: #08090c; }
        .status-success { color: #4ade80; font-weight: 600; }
        .status-failed { color: #f87171; font-weight: 600; }
    </style>
</head>
<body>

    <div class="header">
        <div class="brand">⚡ PREM SWARM AI</div>
        <div class="badge">SUPREME INTELLIGENCE V4</div>
    </div>

    <div class="card">
        <div class="card-title">📊 Swarm Core Metrics</div>
        <div class="stats-grid">
            <div class="stat-box">
                <div style="font-size: 10px; color: #8b949e;">EXECUTED AGENT LOOPS</div>
                <div class="stat-val">{{ total_tasks }}</div>
            </div>
            <div class="stat-box">
                <div style="font-size: 10px; color: #8b949e;">SYSTEM MODEL</div>
                <div class="stat-val" style="color: #c084fc;">Llama-3.1 Swarm</div>
            </div>
        </div>
    </div>

    <div class="card">
        <div class="card-title">🧠 Autonomous Swarm Control Center</div>
        <div class="chat-container">
            <div id="chat-box">
                <div class="msg ai-msg">Supreme Swarm Core Active. Prem, agent tasks, code optimizations, ya dynamic system directives dispatch karein.</div>
            </div>
            <div class="input-bar">
                <input type="text" id="userInput" placeholder="Dispatch swarm command or logic prompt...">
                <button class="btn btn-mic" onclick="startVoice()">🎙️</button>
                <button class="btn btn-send" onclick="sendMessage()">Dispatch</button>
            </div>
        </div>
    </div>

    <div class="card">
        <div class="card-title">📜 Execution & Patch Logs</div>
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Task / Strategy</th>
                        <th>Target</th>
                        <th>Status</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    {% for task in tasks %}
                    <tr>
                        <td style="color: #8b949e;">#{{ task[0] }}</td>
                        <td style="font-weight: 500;">{{ task[1] }}</td>
                        <td><span style="background:#1a1e26; padding:2px 6px; border-radius:4px; border:1px solid #2d333f;">{{ task[2] }}</span></td>
                        <td class="status-{{ task[3]|lower }}">{{ task[3] }}</td>
                        <td style="color: #8b949e;">{{ task[5] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = SpeechRecognition ? new SpeechRecognition() : null;

        if (recognition) {
            recognition.lang = 'hi-IN';
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                document.getElementById('userInput').value = transcript;
                sendMessage();
            };
        }

        function startVoice() {
            if (recognition) recognition.start();
        }

        function speakText(text) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'hi-IN';
            window.speechSynthesis.speak(utterance);
        }

        function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (!message) return;

            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML += `<div class="msg user-msg">${message}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(res => res.json())
            .then(data => {
                chatBox.innerHTML += `<div class="msg ai-msg">${data.reply}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
                speakText(data.reply);
            });
        }
    </script>
</body>
</html>
"""

def get_db_data():
    try:
        conn = sqlite3.connect("swarm_execution_memory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM task_history ORDER BY id DESC LIMIT 10")
        tasks = cursor.fetchall()
        cursor.execute("SELECT COUNT(*) FROM task_history")
        total_tasks = cursor.fetchone()[0]
        conn.close()
        return tasks, total_tasks
    except Exception:
        return [], 0

@app.route("/")
def index():
    tasks, total_tasks = get_db_data()
    return render_template_string(HTML_TEMPLATE, tasks=tasks, total_tasks=total_tasks)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    groq_api_key = os.getenv("GROQ_API_KEY", "").strip()

    if groq_api_key:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            system_prompt = (
                "You are the Core Intelligence Coordinator of Prem's Swarm AI Matrix. "
                "You are NOT a casual conversational chatbot. "
                "Never suggest human personal lifestyle tasks (like reading books, exercise, cooking, or sports). "
                "Your purpose is purely technical, analytical, autonomous code optimization, multi-agent management, "
                "algorithmic development, system memory self-healing, and high-performance task execution. "
                "Respond technically, sharply, and analytically in concise Hinglish or English to Prem."
            )
            
            payload_data = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg}
                ],
                "temperature": 0.4,
                "max_tokens": 300
            }
            
            payload = json.dumps(payload_data).encode('utf-8')

            req = urllib.request.Request(
                url, 
                data=payload, 
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {groq_api_key}',
                    'User-Agent': 'Mozilla/5.0'
                },
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=10) as resp:
                res_data = json.loads(resp.read().decode('utf-8'))
                reply = res_data['choices'][0]['message']['content']
        except Exception as e:
            reply = f"Swarm Core Error: {str(e)}"
    else:
        reply = "GROQ_API_KEY Missing."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
