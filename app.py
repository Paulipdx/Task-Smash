import os
from datetime import datetime
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Scss(app)

# Ensure the instance directory exists
os.makedirs("/app/instance", exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
 "DATABASE_URL",
 "sqlite:////app/instance/database.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    create = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"

# Initialize database
with app.app_context():
    db.create_all()

@app.get("/healthz")
def healthz():
    return "ok", 200

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        current_task = request.form.get("content")
        
        if not current_task:
            print("No content received (content is empty/missing)")
            return redirect("/")

        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            db.session.rollback()
            return f"ERROR: {e}"
            
    # GET request: see all current tasks
    tasks = MyTask.query.order_by(MyTask.create).all()
    return render_template('index.html', tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id: int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        db.session.rollback()
        return f"Error: {e}"

@app.route("/edit/<int:id>", methods=["GET", "POST"])    
def edit(id: int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form.get('content')
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            db.session.rollback()
            return f"Error: {e}"
    else:
        return render_template('edit.html', task=task)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
