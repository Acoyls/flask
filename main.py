from flask import Flask, jsonify
import os
from todor import create_app


app = Flask(__name__)



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=os.getenv("PORT", default=5000))
