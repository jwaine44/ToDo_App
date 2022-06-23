from flask import Flask

app = Flask(__name__)

app.secret_key = "secret"           # Needs to be added for session; secret_key can be set to anything in the string

database = "todos_schema"