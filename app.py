# Import Flask dependency
from flask import Flask

# Create a new Flask app instance
app = Flask(__name__)

# Create Flask routes
# first define the root (the starting point)
@app.route('/')
def hello_world():
    return 'Hello world'

# Skill drill: create another route
@app.route('/today')
def weather_today():
    return 'The weather is nice today!'
