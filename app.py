from flask import Flask

app = Flask(__name__)

# routes
@app.route("/")
def index():
    return "Hello World from Jacob"


if __name__ == "__main__":
    app.run(debug=True)
