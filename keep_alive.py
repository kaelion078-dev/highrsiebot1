from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
@app.route('/health')
def home():
    return "بات Highrise فعال است!"

def run():
    app.run(host='0.0.0.0', port=10000)  # پورت Render

def keep_alive():
    t = Thread(target=run)
    t.start()