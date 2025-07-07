from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/liking")
def liking():
    return render_template('liking.html')

@app.route("/settings")
def setting():
    return render_template('settings.html')

@app.route("/info")
def info():
    return render_template('info.html')

@app.route("/help")
def help():
    return render_template('help.html')

@app.route("/complaints")
def complaints():
    return render_template('complaints.html')

@app.route("/channel")
def channel():
    return render_template('channel.html')

if __name__ == '__main__':
    app.run(debug=True)