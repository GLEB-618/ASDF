from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html') # Не забудьте всю эту панель с разделами добавить на каждой странице; если останется время, сделайте поисковую строку для видео.

@app.route("/liking")
def liking():
    return render_template('liking.html')

@app.route("/settings")
def setting():
    return render_template('settings.html') # Добавьте тёмную тему и английский язык (Я не думаю, что здесь может ещё что-то понадобиться).

@app.route("/info")
def info():
    return render_template('info.html')

@app.route("/help")
def help():
    return render_template('help.html') # Я напишу ответы на главные вопросы, потом оформите этот раздел и добавьте нужные ссылки.

@app.route("/complaints")
def complaints():
    return render_template('complaints.html') # Это раздел для админов! Сделайте whitelist для админов и модераторов.

@app.route("/channel")
def channel():
    return render_template('channel.html')

if __name__ == '__main__':
    app.run(debug=True)