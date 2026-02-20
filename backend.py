from flask import Flask, jsonify
from flask_cors import CORS  # allow frontend JS to fetch data

app = Flask(__name__)
CORS(app)

colleges = [
    {"name": "ABC University", "location": "New York", "courses": ["Engineering", "MBA"], "admission": "Entrance Exam"},
    {"name": "XYZ College", "location": "California", "courses": ["Science", "Arts"], "admission": "Merit Based"}
]

@app.route("/colleges")
def get_colleges():
    return jsonify(colleges)

if __name__ == "__main__":
    app.run(debug=True)