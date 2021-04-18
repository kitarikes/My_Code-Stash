from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def index():
    return "hello"

@app.route("/up", methods=["POST"])
def func():
    filename = "output.jpg"
    name = request.headers["File-Name"]
    print(name)
    img = request.get_data()

    with open(filename, 'wb') as f:
            f.write(img)
    
    return "success"


if __name__ == '__main__':
    app.run(port=6006)
