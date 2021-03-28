from flask import Flask
from threading import Thread
from waitress import serve
from datetime import datetime, timezone, timedelta
import os

# Gets an instance of a WGSI application
app = Flask('')


# Logs a message whenever the server page is accessed
@app.route('/')
def home():
    print(datetime.now(timezone(timedelta(minutes=30, hours=5))))
    print("GET request, home route \n\n")
    return "Hello. I am alive!"


# Serves the application using waitress
def run():
    port = int(os.environ.get("PORT", 5000))
    serve(app, listen='*:' + port)


# Keeps the application alive somehow
def keep_alive():
    t = Thread(target=run)
    t.start()
