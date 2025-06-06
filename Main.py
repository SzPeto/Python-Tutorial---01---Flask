from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from functions import Functions

def main():
    # Master
    functions = Functions()
    functions.create_file("Log\\log.txt")
    functions.create_dir("Databases")

    # App setup
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Databases/database.db" # configure Flask to use a specific database

    # Creating routes to webpages
    @app.route("/")
    def index():
        return render_template("index.html")

    app.run(debug=True)

# Main
if __name__ == "__main__":
    main()