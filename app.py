from flask import Flask, render_template

# Flask App Initialization
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return render_template('index.html')
    
if __name__ == '__main__':
    run_flask(debug = True)
