from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__) 
db = SQLAlchemy() 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from fbooks import routes 

