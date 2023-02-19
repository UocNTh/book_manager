from flask import jsonify, request, make_response
from fbooks import app , db 
from flask_restful import Resource, Api
from fbooks.models import Users, Books, orders 
from fbooks.data import get_data 
from datetime import datetime 

api = Api(app) 

with app.app_context():
    db.create_all()

class UsersList(Resource) : 
    def get(self): 
        users = Users.query.all() 
        output = []
        for user in users : 
            user_data = {} 
            get_data(user,user_data)
            output.append(user_data)
        if len(output) > 0 : return jsonify({'users': output}) 
        else : return jsonify({'message': 'None'})

    def post(self): 
        data = request.get_json()
        new_user = Users(user_name = data['user_name'] , address = data['address'], phone_number = data['phone_number'] , email = data['email']) 
        db.session.add(new_user)
        db.session.commit() 
        return jsonify({'message':'New user has been created'})

class UserById(Resource): 
    def get(self,id): 
        user = Users.query.get_or_404(int(id)) 
        user_data = {} 
        get_data(user, user_data ) 
        return jsonify({'user': user_data})

    def delete(self,id):
        user = Users.query.get_or_404(int(id)) 
        db.session.delete(user) 
        db.session.commit() 
        return jsonify({'message': 'The user has been deleted'})

    def put(self,id): 
        user = Users.query.get_or_404(int(id)) 
        if not user : return jsonify({'message': 'Not found'}), 404
        data = request.get_json() 
        user.user_name = data['user_name']
        user.address = data['address']
        user.phone_number = data['phone_number']
        user.email = data['email']
        db.session.commit()
        return jsonify({'massage' : 'The changes have been saved'})
#------------------------------------------------------------------------------------------------------------------------
class BooksList(Resource) : 
    def get(self): 
        books = Books.query.all() 
        output = []
        for book in books : 
            book_data = {} 
            get_data(book,book_data)
            output.append(book_data)
        if len(output) > 0 : return jsonify({'books': output}) 
        else : return jsonify({'message': 'None'})

    def post(self): 
        data = request.get_json()
        new_book = Books(book_name = data['book_name'] , author = data['author'], publication_date = datetime.utcnow() , genre = data['genre']) 
        db.session.add(new_book)
        db.session.commit() 
        return jsonify({'message':'New book has been created'})

class BookById(Resource): 
    def get(self,id): 
        book = Books.query.get_or_404(int(id)) 
        book_data = {} 
        get_data(book, book_data) 
        return jsonify({'book': book_data})

    def delete(self,id):
        book = Books.query.get_or_404(int(id)) 
        db.session.delete(book) 
        db.session.commit() 
        return jsonify({'message': 'The book has been deleted'})

    def put(self,id): 
        book = Books.query.get_or_404(int(id)) 
        if not book : return jsonify({'message': 'Not found'}), 404
        data = request.get_json() 
        book.book_name = data['book_name']
        book.author = data['author']
        book.publication_date = datetime.utcnow()
        book.genre = data['genre']
        db.session.commit()
        return jsonify({'massage' : 'The changes have been saved'})
#------------------------------------------------------------------------------------------------------------------------
class Order(Resource) : 

    def post(self) :
        data = request.get_json() 
        user = Users.query.get_or_404(int(data['user_id'])) 
        book = Books.query.get_or_404(int(data['book_id']))
        user.mybooks.append(book) 
        db.session.add(user) 
        db.session.commit()

        return jsonify({'message': 'OK'}) 

class User_Order(Resource) : 
    def get(self, id) : 
        # Sach nguoi dung <id> da doc
        user_book = Users.query.get_or_404(int(id)) 
        user_data = {} 
        get_data(user_book, user_data) 
        user_data['mybooks'] = []
        for book in user_book.mybooks : 
            book_data = {} 
            get_data(book,book_data) 
            user_data['mybooks'].append(book_data)
        return jsonify({'user' : user_data})

class Book_Order(Resource) : 
    def get(self, id) : 
        # Sach co nhung nguoi dung <id> da doc 
        book_user  = Books.query.get_or_404(int(id)) 
        book_data = {} 
        get_data(book_user, book_data) 
        book_data['myusers'] = []
        for user in book_user.myusers : 
            user_data = {} 
            get_data(user, user_data) 
            book_data['myusers'].append(user_data)

        return jsonify({'book' : book_data})
#------------------------------------------------------------------------------------------------------------------------
api.add_resource(UsersList, '/users')
api.add_resource(UserById, '/user/<int:id>')
api.add_resource(BooksList, '/books')
api.add_resource(BookById, '/book/<int:id>')
api.add_resource(Order, '/orders') 
api.add_resource(User_Order, '/user/<int:id>/order') 
api.add_resource(Book_Order,'/book/<int:id>/order')
#------------------------------------------------------------------------------------------------------------------------
@app.errorhandler(404) 
def error_405(_error): 
    return make_response(jsonify({'error': 'Not Found'}), 404 )
@app.errorhandler(405) 
def error_405(_error): 
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405 )
