from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Bounty Bug Project!"

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/about')
def about():
    return "This is the About Page of Bounty Bug Project!"
