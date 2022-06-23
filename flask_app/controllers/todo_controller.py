from flask import session, render_template, request, redirect
from flask_app import app   #Importing app variable from __init__.py
from flask_app.models.todo_model import Todo    # Importing Todo class from todo_model file
from flask_app.models.user_model import User

@app.route("/todos")                         # Could put methods = ['GET'] here, but it's defaulted to be here; GET means to display
def get_all_todos():
    if User.validate_session == False:
        return redirect('/login')
    else:
        if "num_of_visits" in session:      # Validates visits to the site; if you hit refresh, the counter goes up by one
            session["num_of_visits"] += 1
        else:
            session["num_of_visits"] = 1

    list_of_todos = Todo.get_all()
    return render_template("index.html", list_todos = list_of_todos)

@app.route("/todo/new")
def display_create_todo():
    if User.validate_session == False:
        return redirect('/login')
    else:
        return render_template("todoForm.html")

@app.route("/todo/new", methods = ['POST'])             # POST is keyword to create something, in this case a new todo; other 'GET', 'PUT','DELETE' are other methods; if you don't put one, 'GET' is the default; Also, /new is a standard path to use
def create_todo():
    Todo.create(request.form)
    return redirect("/todos")

@app.route('/todo/<int:id>/update')
def get_todo_by_id(id):                     # Need data to be a dictionary because mogrify expects it in mysqlconnection
    if User.validate_session == False:
        return redirect('/login')
    else:
        data = {
            "id": id
        }
        current_todo = Todo.get_one(data)             # Call get_one in the Todo model
        return render_template('editTodoForm.html', current_todo = current_todo)

@app.route('/todo/<int:id>/update', methods=['POST'])
def update_todo_by_id(id):
    data = {
        'id': id,
        'status': request.form['status'],
        'todo': request.form['todo']
    }
    Todo.update_one(data)
    return redirect('/display/user')

@app.route('/todo/<int:id>/delete')
def delete_todo_by_id(id):
    data = {
        'id': id
    }
    Todo.delete_one(data)
    return redirect('/display/user')

"""
Functions as SQL Queries
SELECT:
def get_all()       If we're selecting everything i.e. SELECT *
def get_one()       If we're selecting one

INSERT:
def create()        If we're doing an insert

DELETE:
def delete_one()    If we're doing a delete

DELETE:
DEF update_one()    If we're doing an update/edit
def edit_one()      

"""