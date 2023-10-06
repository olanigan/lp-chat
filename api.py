from flask import Flask, request
from chain import chat_chain

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to LP Chat API", 200

@app.route('/api', methods=['GET', 'POST'])
def index():
    """Prints the POST request message."""
    message = request.get_json()
    message = message['message']
    print(f"Received message: {message}")
    # return "Welcome to LP Chat API", 200
    print('Loading Store&Chain for HTTP')
    return chat_chain(message), 200

if __name__ == "__main__":
    app.run(port=5002)