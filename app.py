from flask import Flask
from database import init_db

app = Flask(__name__)
init_db()

from routes import main as routes_blueprint
app.register_blueprint(routes_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
