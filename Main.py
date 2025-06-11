import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.session import Session
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

sort = "id"

# Creating routes to webpages ***********************************************************************************
@app.route("/", methods = ["POST", "GET"])
def index():
    if request.method == "POST":
        try:
            action = request.form.get("action")
            if action == "Add entry":
                try:
                    description = request.form.get("description")
                    category = request.form.get("category")
                    price = float(request.form.get("price"))
                    date = request.form.get("date")
                    new_entry = DbData(description = description, category = category, price = price, date = date)
                    db.session.add(new_entry)
                    db.session.commit()
                except Exception as e:
                    functions.write_log(f"def index - Error while adding entry : {e}")
            elif action == "Delete selected":
                try:
                    selected = request.form.getlist("checked-entries") # Getlist return a list of selected items
                    if selected:
                        for i in range(len(selected)):
                            entry = db.session.get(DbData, selected[i]) # It returns an instance of DbData
                            db.session.delete(entry)
                        db.session.commit()
                except Exception as e:
                    functions.write_log(f"def index - Error while deleting selected : {e}")
            elif action == "Delete all":
                try:
                    DbData.query.delete()
                    db.session.commit()
                except Exception as e:
                    functions.write_log(f"def index - Error while deleting all : {e}")
            elif action == "Refresh":
                return redirect("/")
            elif action == "Sort":
                global sort
                sort = request.form.get("sort").lower()

            return redirect("/")
        except Exception as e:
            functions.write_log(f"Main.py - def index - Something went wrong in POST request : {e}")
            return f"Error : {e}"
    else:
        entries = DbData.query.order_by(getattr(DbData, sort)).all() # This returns a list of DbData instances

    # This is a GET request
    return render_template("index.html", today = today, entries = entries)

@app.route("/edit/<int:entry_id>", methods = ["POST", "GET"])
def edit(entry_id):
    entry = db.session.get(DbData, entry_id)
    if not entry:
        return f"Entry with id : {entry_id} not found"

    if request.method == "POST":
        entry.description = request.form.get("description")
        entry.category = request.form.get("category")
        entry.price = request.form.get("price")
        entry.date = request.form.get("date")
        db.session.commit()
        return redirect("/")


    return render_template("edit.html", entry = entry)


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

    app.run(debud = True)