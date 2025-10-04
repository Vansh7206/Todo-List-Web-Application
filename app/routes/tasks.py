from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task 

tasks_bp = Blueprint('tasks',__name__) #making blueprint of task

@tasks_bp.route("/")
def view_tasks():
    if 'user' not in session:
        return redirect(url_for("auth.login"))
    
    tasks = Task.query.all()  # Get all tasks for now to debug
    print(f"DEBUG: Found {len(tasks)} tasks in database")  # Debug line
    for task in tasks:
        print(f"DEBUG: Task - ID: {task.id}, Title: {task.title}, Status: {task.status}")  # Debug line
    
    return render_template("tasks.html", tasks=tasks)

#adding task
@tasks_bp.route("/add", methods=["POST"])
def add_tasks():
    if 'user' not in session:
        return redirect(url_for("auth.login"))
    
    title = request.form.get("title")
    if title:
        new_task = Task(title=title, status="Pending")
        db.session.add(new_task)
        db.session.commit()
        print(f"DEBUG: Added task - ID: {new_task.id}, Title: {new_task.title}")  # Add this line
        flash("Task added Successfully", "success")
    
    return redirect(url_for("tasks.view_tasks"))

#showing current status of task
@tasks_bp.route("/toggle/<int:task_id>", methods = ["POST"])
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        if task.status == "Pending":
            task.status == "Working"
        elif task.status == "Working":
            task.status == "Done"
        else:
            task.status == "Pending"
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))

#clearing all tasks
@tasks_bp.route("/clear", methods = ["POST"])
def clear_tasks():
    Task.query.delete()
    db.session.commit()
    flash("All tasks cleared","info")
    return redirect(url_for("tasks.view_tasks"))
