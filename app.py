# imports 
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Example: If your Destination Path in 

# My App
app = Flask(__name__)  
Scss(app)

@app.get("/healthz")
def healthz():
 return "ok", 200


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////app/instance/database.db"

db = SQLAlchemy(app)


#data class - row of data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    create = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"Task {self.id}"

with app.app_context():
    db.create_all()

# Routes to Webpages
# home page 
@app.route("/",methods=["POST" , "GET"])
def index():
    #ADD TASK 
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    #see all current taks
    else: 
        tasks = MyTask.query.order_by(MyTask.create).all()
        return render_template('index.html',tasks=tasks)   

# delete an item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error:{e} "
    
# Edit an item
@app.route("/edit/<int:id>", methods=["GET","POST"])    
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error:{e}"
        
    else:
        return render_template('edit.html', task=task)


# runner and Debugger 
if __name__ == "__main__":
    
     app.run(host="0.0.0.0", port=8001)
 
