#!/usr/bin/env python3
"""
Simple GenAI Bot for AWS Deployment Tutorial - FIXED VERSION
A basic chatbot that responds to user input with helpful messages.
"""

import json
import time
import random
from http.server import HTTPServer, BaseHTTPRequestHandler

class ChatBot:
    def __init__(self):
        self.responses = {
    "hello": [
        "Hi there! How can I help you today?",
        "Hello! What's on your mind?",
        "Hey! Great to see you!",
        "Hi! What can I do for you?"
    ],
    "how are you": [
        "I'm doing great! Thanks for asking.",
        "I'm fantastic and ready to help!",
        "All systems running smoothly!",
        "Feeling helpful as always!"
    ],
    "help": [
        "I can chat with you! Try saying hello, asking how I am, or just tell me what's on your mind.",
        "I'm here to help! I can respond to greetings and general questions.",
        "Need assistance? Just type a message and I'll do my best!",
        "Ask me anything or just say hi to get started!"
    ],
    "bye": [
        "Goodbye! Have a wonderful day!",
        "See you later!",
        "Take care!",
        "Catch you next time!"
    ],
    "thanks": [
        "You're welcome!",
        "Anytime!",
        "No problem!",
        "Glad I could help!"
    ],
    "who are you": [
        "I'm your friendly chatbot assistant.",
        "I'm a simple bot here to chat and help.",
        "Just a helpful program built to talk with you!"
    ],
    "what can you do": [
        "I can respond to greetings and general questions!",
        "Right now, I can chat with you and answer simple things. More to come soon!",
        "Try saying hello, asking how I am, or just start a conversation."
    ],
    "default": [
        "That's interesting! Tell me more.",
        "I see! What else would you like to talk about?",
        "Thanks for sharing that with me!",
        "Hmm, that's a good point!",
        "I appreciate you telling me that!",
        "Let’s keep the conversation going!",
        "Can you explain that a bit more?"
    ]
}

    
    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        
        # Simple keyword matching
        for keyword, responses in self.responses.items():
            if keyword in user_input and keyword != "default":
                return random.choice(responses)
        
        # Default response if no keywords match
        return random.choice(self.responses["default"])

class BotHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.bot = ChatBot()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests - return a simple web interface"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = '''<!DOCTYPE html>
<html>
<head>
    <title>GenAI assistant Bot</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 600px; 
            margin: 50px auto; 
            padding: 20px; 
        }
        .chat-container { 
            border: 1px solid #ccc; 
            height: 400px; 
            overflow-y: scroll; 
            padding: 10px; 
            margin-bottom: 10px; 
            background-color: #f9f9f9;
        }
        .user-message { 
            color: blue; 
            margin: 5px 0; 
            font-weight: bold;
        }
        .bot-message { 
            color: green; 
            margin: 5px 0; 
        }
        input[type="text"] { 
            width: 70%; 
            padding: 10px; 
            font-size: 16px;
        }
        button { 
            padding: 10px 20px; 
            background: #007cba; 
            color: white; 
            border: none; 
            cursor: pointer; 
            font-size: 16px;
        }
        button:hover {
            background: #005a8b;
        }
    </style>
</head>
<body>
    <h1>GenAI assistant Bot</h1>
    <div id="chat" class="chat-container"></div>
    <input type="text" id="messageInput" placeholder="Type your message here...">
    <button onclick="sendMessage()">Send</button>
    
    <script>
        function addMessage(message, isUser) {
            const chat = document.getElementById('chat');
            const div = document.createElement('div');
            div.className = isUser ? 'user-message' : 'bot-message';
            div.textContent = (isUser ? 'You: ' : 'Bot: ') + message;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            addMessage(message, true);
            input.value = '';
            
            // Show thinking message
            addMessage('Thinking...', false);
            
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({message: message})
            })
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error('Server responded with status: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                // Remove thinking message
                const chat = document.getElementById('chat');
                const messages = chat.getElementsByClassName('bot-message');
                const lastMessage = messages[messages.length - 1];
                if (lastMessage && lastMessage.textContent.includes('Thinking...')) {
                    chat.removeChild(lastMessage);
                }
                addMessage(data.response, false);
            })
            .catch(error => {
                console.error('Error:', error);
                // Remove thinking message
                const chat = document.getElementById('chat');
                const messages = chat.getElementsByClassName('bot-message');
                const lastMessage = messages[messages.length - 1];
                if (lastMessage && lastMessage.textContent.includes('Thinking...')) {
                    chat.removeChild(lastMessage);
                }
                addMessage('Sorry, I had trouble connecting to the server: ' + error.message, false);
            });
        }
        
        // Allow Enter key to send message
        document.getElementById('messageInput').addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Welcome message when page loads
        window.onload = function() {
            addMessage('Hello! I am your simple GenAI bot. Try saying "hello" or asking "how are you?"', false);
        };
    </script>
</body>
</html>'''
            
            self.wfile.write(html.encode())
        
        elif self.path == '/health':
            # Health check endpoint for AWS
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "healthy", "timestamp": time.time()}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle POST requests - chat API"""
        if self.path == '/chat':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                user_message = data.get('message', '')
                print(f"Received message: {user_message}")  # Debug log
                
                if user_message:
                    bot_response = self.bot.get_response(user_message)
                    response = {"response": bot_response, "timestamp": time.time()}
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
                    self.end_headers()
                    
                    response_json = json.dumps(response)
                    print(f"Sending response: {response_json}")  # Debug log
                    self.wfile.write(response_json.encode())
                else:
                    self.send_error(400, "No message provided")
            
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                self.send_error(400, "Invalid JSON")
            except Exception as e:
                print(f"Error processing request: {e}")
                self.send_error(500, "Internal server error")
        else:
            self.send_error(404)

def run_server(port=8081):
    server_address = ('', port)
    httpd = HTTPServer(server_address, BotHandler)
    print(f"🤖 GenAI Bot server starting on port {port}")
    print(f"🌐 Open your browser to: http://localhost:{port}")
    print(f"🛠️  Health check available at: http://localhost:{port}/health")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Bot server stopped. Goodbye!")
        httpd.server_close()

if __name__ == "__main__":
    run_server()