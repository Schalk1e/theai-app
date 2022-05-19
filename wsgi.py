import os

from app import init_app

try:
    port = os.environ["PORT"]
except Exception as e:
    print(e)
    pass

app = init_app()

if __name__ == "__main__":
    if port:
        app.run(host="0.0.0.0", debug=True, port=port)
    else:
        app.run(host="0.0.0.0", debug=True)
