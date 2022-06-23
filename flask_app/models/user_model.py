from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import database
from flask_app.models.todo_model import Todo
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:                 # Receives dictionary with fields to fill atttributes of our tables in MySQL
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def get_one(cls, data):
        query = "SELECT * "
        query += "FROM users "
        query += "WHERE email =%(email)s;"

        result = connectToMySQL(database).query_db(query, data)
        print(result)
        if len(result) > 0:             # Checking to see if there's one instance of the first_name/last_name combination, and if so, it goes to the homepage
            return cls(result[0])
        else:
            return None         # If not, it'll go back to login

    @classmethod                                                # Do this with one to many relationships; one user with many todos
    def get_one_with_todos(cls, data):
        query = "SELECT * "
        query += "FROM users JOIN todos ON users.id = todos.user_id "             # Joining the join table to the todos table
        query += "WHERE users.id = %(id)s;"

        result = connectToMySQL(database).query_db(query, data)                 # Have to pass query and the data from user_controller app.route get_user_by_id
        # Validate where someone has todos, if they do, will create user instance, then create list of todos to add to user instance
        if len(result) > 0:                             # Result is a list of dictionaries
            current_user = cls(result[0])               # Added current_user of an instance of the object
            list_todos = []
            for row in result:
                current_todo = {                        # Generating the new todo to append it to a new list
                    "id": row["todos.id"],
                    "todo": row["todo"],
                    "status": row["status"],
                    "created_at": row["todos.created_at"],
                    "updated_at": row["todos.updated_at"],
                    "user_id": row["user_id"]
                }
                todo = Todo(current_todo)
                list_todos.append(todo)        # Adding to this instance current_user new instance of list of todos
            current_user.list_todos = list_todos
            print(current_user)
            print(current_user.list_todos)
            return current_user
        return None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) "
        query+= "VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(database).query_db(query, data)
        return result

# validating login via staticmethod, receiving a dictionary
    @staticmethod
    def validate_login(data):
        isValid = True
        if data['email'] == "":
            flash("Please provide your email.", "error_email")
            isValid = False
        if data['password'] == "":
            flash("Please provide your password.", "error_password")
            isValid = False
        return isValid

# validating session
    @staticmethod
    def validate_session():
        if "id" in session:
            return True
        else:
            flash("You must be logged in to see the content of this application.")
            return False

# error_register matches to label names
    @staticmethod
    def validate_registration(data):
        isValid = True
        if data['email'] == "":
            flash("You must provide an email.", "error_register_email")
            isValid = False
        if data['password'] == "":
            flash("You must provide a password.", "error_register_password")
            isValid = False
        if data['first_name'] == "":
            flash("You must provide your first name.", "error_register_first_name")
            isValid = False
        if data['first_name'] == "":
            flash("You must provide your last name.", "error_register_last_name")
            isValid = False
        if data['password_confirmation'] != data['password']:
            flash("Your password confirmation doesn't match.", "error_register_password_confirmation")
            isValid = False
        if len(data['password']) < 4:
            flash("Password must be at least 4 characters long.", "error_register_password")
            isValid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Please provide a valid email.", "error_register_email")
            isValid = False
        return isValid