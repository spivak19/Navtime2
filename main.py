# main.py
import threading
import time
import webview
from backend.server import app


def start_flask():
    # Start Flask on localhost:5000
    app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
    # flask_thread = threading.Thread(target=start_flask)
    # flask_thread.daemon = True
    # flask_thread.start()
    
    # # Wait a moment for the server to start
    # time.sleep(1)
    
    # # Open a desktop window that loads the Flask-hosted app
    # webview.create_window('Document Management System', 'http://127.0.0.1:5000')
    # webview.start()

