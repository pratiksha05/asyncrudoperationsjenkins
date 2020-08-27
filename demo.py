from flask import Flask

app =  Flask(__name__)

@app.route('/', methods=['GET'])
def index():

    data = {"name": "nidhi"}

    return data


if __name__ == "__main__":
    app.run("localhost", 8088, debug=True)