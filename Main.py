import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

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
            new_entry = DbData(description = description, category = category, price = price, date = date)
            db.session.add(new_entry)
            db.session.commit()
            functions.write_log(f"Main.py - def index - POST request successfull")
            return redirect("/")
        except Exception as e:
            functions.write_log(f"Main.py - def index - Something went wrong in POST request : {e}")
            return f"Error : {e}"
    else:
        entries = DbData.query.order_by(DbData.date).all()
        for i in range(len(entries)):
            print(
                f"{entries[i].id}, {entries[i].description}, {entries[i].category}, "
                f"{entries[i].price}, {entries[i].date}"
            )

    return render_template("index.html", today = today, entries = entries)

# Data model for database ***************************************************************************************
class DbData(db.Model):
    # You can't have the self parameter, since we are inheriting from SQLAlchemy model
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
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