import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from functions import Functions


# Master ********************************************************************************************************
functions = Functions()
today = datetime.datetime.now().strftime("%Y-%m-%d")

# App setup
app = Flask(__name__)
    # configure Flask database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" # It has to be in root folder
db = SQLAlchemy(app)

# Creating routes to webpages ***********************************************************************************
@app.route("/", methods = ["POST", "GET"])
def index():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    if request.method == "POST":
        try:
            description = request.form.get("description")
            category = request.form.get("category")
            price = float(request.form.get("price"))
            date = request.form.get("date")
            print(f"POST request : {description}, {category}, {price}, {date}")
            functions.write_log(f"Main.py - def index - POST request successfull")
        except Exception as e:
            functions.write_log(f"Main.py - def index - Something went wrong in POST request : {e}")
    elif request.method == "GET":
        print("GET")

    return render_template("index.html", today = today)

# Data model for database ***************************************************************************************
class DbData(db.Model):
    # You can't have the self parameter, since we are inheriting from SQLAlchemy model
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(100), nullable = False) # NULL in SQL
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    date = db.Column(db.String(20), default = today)
    functions.write_log("Main.py - class DbData loaded")

    def __repr__(self) -> str: # Repr dunder method represents the string representation of object
                               # -> This symbol means type hinting, mostly for autocomplete purposes
        return f"Task {self.id}"



# Main *******************************************************************************************************
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)