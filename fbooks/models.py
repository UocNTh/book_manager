from datetime import datetime 
from fbooks import db 


orders = db.Table('orders', 
                db.Column('user_id', db.Integer , db.ForeignKey('users.user_id')) , 
                db.Column('book_id', db.Integer , db.ForeignKey('books.book_id'))
                )

class Users(db.Model) : 
    user_id = db.Column(db.Integer, primary_key=True, autoincrement = True )
    user_name = db.Column(db.String(50), nullable = False )
    address = db.Column(db.String(80))
    phone_number = db.Column(db.String(12))
    email = db.Column(db.String(100)) 

    mybooks = db.relationship('Books', secondary = orders , backref = 'users') 

    def __repr__(self) : 
        return f"user_id: {self.user_id} user_name: {self.user_name}"  

class Books(db.Model) : 
    book_id = db.Column(db.Integer, primary_key=True, autoincrement = True )
    book_name = db.Column(db.String(50), nullable = False )
    author = db.Column(db.String(50), nullable = False ) 
    publication_date = db.Column(db.DateTime, default=datetime.now )
    genre= db.Column(db.String(100)) 

    myusers = db.relationship('Users', secondary = orders , backref = 'books') 

    def __repr__(self) : 
        return f"book_id: {self.book_id} book_name: {self.book_name}"
