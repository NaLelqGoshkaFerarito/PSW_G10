from flask import Flask
from base_bp import views

app = Flask(__name__)
# app.register_blueprint(views, url_prefix="/")
app.register_blueprint(views)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
