# app.py
from flask import Flask
from index.index import index_bp
from result.result import result_bp

app = Flask(__name__)
app.register_blueprint(index_bp)
app.register_blueprint(result_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')