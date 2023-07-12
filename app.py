from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
db: SQLAlchemy = SQLAlchemy(app)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)


@app.route("/")
def index():
    notes = Notes.query.order_by(Notes.id).all()
    return render_template("index.html", notes=notes)


@app.route("/create-note", methods=["POST", "GET"])
def create_note():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        note: Notes = Notes(title=title, description=description)

        try:
            db.session.add(note)
            db.session.commit()
            return redirect("/")
        except:
            return "Error!"

    return render_template("create_note.html")


@app.route("/edit_note/<int:id>", methods=["POST", "GET"])
def edit_note(id: int):
    note = Notes.query.get(id)

    if request.method == "POST":
        note.title = request.form["title"]
        note.description = request.form["description"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Error!"
    else:
        return render_template("edit_note.html", note=note)


@app.route("/edit_note/<int:id>/delete")
def delete_note(id: int):
    note = Notes.query.get(id)

    try:
        db.session.delete(note)
        db.session.commit()
        return redirect("/")
    except:
        return "Error!"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
