from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import database

class Todo:
    def __init__(self, data):    # data will be a dictionary that will hold all columns/values in dictionary
        self.id = data['id']        # match all column names exactly with self and the variables
        self.todo = data['todo']
        self.status = data['status']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # SELECT class method
    @classmethod                # All queries must be classmethod
    def get_all(cls):           # We place native SQL here
        query = "SELECT * "     # Could make lines 14, 15 as one line i.e. query = "SELECT * FROM todos;" if that's how you write it in the Workbench
        query += "FROM todos;"

        result = connectToMySQL(database).query_db(query)    #Result is a list of dictionaries of all the todos; NEED TO PUT IN YOUR PARTICULAR SCHEMA AS A VARIABLE IN __INIT__.PY IN ARGUMENT HERE
        list_todos = []

        for row in result:              # Calling one row in table todos
            list_todos.append(cls(row))

        return list_todos

    # INSERT class method
    @classmethod
    def create(cls, data):
        query = "INSERT INTO todos(todo, status, user_id)"  # Must be same values as column names in Workbench
        query += "VALUES(%(todo)s, %(status)s, %(user_id)s);"

        id_new_todo = connectToMySQL(database).query_db(query, data)
        print(id_new_todo)
        return(id_new_todo)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM todos WHERE id = %(id)s;"

        result = connectToMySQL(database).query_db(query, data)         # Result will be a list holding one todo
        
        if len(result) > 0:
            todo = cls(result[0])
            return todo
        else:
            return None

    @classmethod
    def update_one(cls, data):
        query = 'UPDATE todos '
        query += 'SET todo = %(todo)s, status = %(status)s WHERE id = %(id)s;'

        return connectToMySQL(database).query_db(query, data)

    @classmethod
    def delete_one(cls, data):
        query= 'DELETE FROM todos WHERE ID = %(id)s;'
        return connectToMySQL(database).query_db(query, data)