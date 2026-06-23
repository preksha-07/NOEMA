from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/optimize")
def optimize():

    data = {

    "classical": {

        "cost": 2704,
        "risk": 20,
        "time": 35,

        "path": [
            [100, 120],
            [250, 120],
            [250, 270],
            [100, 270],
            [100, 120]
        ]
    },

    "optimized": {

        "cost": 461,
        "risk": 3,
        "time": 12,

        "path": [
            [430, 120],
            [580, 120],
            [580, 270],
            [430, 270],
            [430, 120]
        ]
    }
}
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)