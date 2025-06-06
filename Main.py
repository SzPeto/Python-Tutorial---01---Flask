from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# App setup
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Databases/database.db" # configure Flask to use a specific database

# Creating routes to webpages
@app.route("/")
def index():
    return render_template("index.html")

# Main
if __name__ == "__main__":
    app.run(debug = True)