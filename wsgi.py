from api import app

# WSGI сервер запущенный на localhost
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)

