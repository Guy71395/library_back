import json
from datetime import datetime, timedelta
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library_db.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
# ///////////////////////////Define the Database//////////////////////////////////
class Book(db.Model):
    id = db.Column( db.Integer, primary_key = True)
    bName = db.Column(db.String(100))
    Author = db.Column(db.String(50))
    bYear = db.Column(db.Integer)
    bType = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    book = db.relationship('Loan', backref='book')

    def __init__(self, bName, Author, bYear, bType, active):
        self.bName = bName
        self.Author = Author
        self.bYear = bYear
        self.bType = bType
        self.active = active

class Customer(db.Model):
    id = db.Column( db.Integer, primary_key = True)
    cName = db.Column(db.String(50))
    City = db.Column(db.String(50))
    age = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    customer = db.relationship('Loan', backref='customer')

    def __init__(self, cName, City, age, active):
        self.cName = cName
        self.City = City
        self.age = age
        self.active = active

class Loan(db.Model):
    id = db.Column( db.Integer, primary_key = True)
    custID = db.Column(db.Integer, db.ForeignKey('customer.id'))
    bookID = db.Column(db.Integer, db.ForeignKey('book.id'))
    loanDate = db.Column(db.DateTime)
    returnDate = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, customer, book, loanDate, returnDate, active):
        self.custID = customer
        self.bookID = book
        self.loanDate = loanDate
        self.returnDate = returnDate
        self.active = active


# ///////////////////////////BOOKS//////////////////////////////////
@app.route('/books/', methods=['GET','POST'])
@app.route('/books/<id>', methods=['GET','PUT'])
def book_crud(id=-1):
    # GET all
    if request.method == 'GET' and id== -1:
        result = []
        for b in Book.query.all():
            result.append({
                "b_id":b.id,"bName":b.bName,'auther':b.Author,'bYear':b.bYear,'bType':b.bType,"active":b.active
                })
        return json.dumps(result)
    # GET Id
    if request.method == 'GET' and int(id) > -1:
        result = Book.query.get(id)
        showMe = {
            "b_id":result.id,"Name":result.bName,'auther':result.Author,
            'bYear':result.bYear,'bType':result.bType,"active":result.active
            }
        return showMe
    if request.method == 'POST':
        request_data = request.get_json()
        bName = request_data['bName']
        auther = request_data['auther']
        bYear = request_data['bYear']
        bType = request_data['bType']
        active=True
        newBook = Book(bName,auther,bYear,bType,active)
        db.session.add(newBook)
        db.session.commit()
        return {"msg":f"A New Book was registered : {bName}"}
    if request.method == 'PUT': #making the book inactive
        delBook = Book.query.get(id)
        request_data = request.get_json()
        u_active = request_data["active"]
        delBook.active = u_active
        db.session.commit()
        return {"msg":"Book has been set Inactive"}

# 1: add customer //DONE
# 2: get all customers //DONE
# 3: remove customer //DONE

# ///////////////////////////Customers//////////////////////////////////
@app.route('/customers/', methods=['GET','POST'])
@app.route('/customers/<id>', methods=['PUT'])
def customer_crud(id=-1):
    if request.method == 'POST':
        request_data = request.get_json()
        cName = request_data["cName"]
        City = request_data["City"]
        age = request_data["age"]
        active=True
        newCustomer = Customer(cName,City,age,active)
        db.session.add(newCustomer)
        db.session.commit()
        return {"msg":f"A New Customer was registered : {cName}"}
    if request.method == 'GET':
        result = []
        for c in Customer.query.all():
            result.append({"c_id":c.id,"cName":c.cName,'city':c.City,'age':c.age,"active":c.active})
        return json.dumps(result)
    if request.method == 'PUT':
        delCustomer = Customer.query.get(id)
        request_data = request.get_json()
        u_active = request_data["active"]
        delCustomer.active = u_active
        db.session.commit()
        return {"msg":"Customer has been set Inactive"}

# ///////////////////////////Loans//////////////////////////////////

@app.route('/loans/', methods=['GET','POST'])
@app.route('/loans/<id>', methods=['PUT'])
def loan_crud(id=id):
    if request.method == 'POST':
        request_data = request.get_json()
        customer = request_data["customer"]
        book = request_data["book"]
        loanDate = datetime.now()
        # //////////creating returndate based of book type///////////
        if Book.query.get(book).bType == 1:
            delta = timedelta(days=10)
        elif Book.query.get(book).bType == 2:
            delta = timedelta(days=5)
        elif Book.query.get(book).bType == 3:
            delta = timedelta(days=2)
        returnDate = (loanDate + delta)
        active=True
        newLoan = Loan(customer,book,loanDate,returnDate,active)
        db.session.add(newLoan)
        db.session.commit()
        return {"msg":"Succeses"}
    if request.method == 'GET':
        result = []
        for l in Loan.query.all():
            result.append({
                "l_id":l.id,"customer":Customer.query.get(l.custID).cName,
                "book":Book.query.get(l.bookID).bName,"loanDate":l.loanDate.strftime("%Y-%m-%d"),
                "returnDate":l.returnDate.strftime("%Y-%m-%d"),"active":l.active
                })
        return json.dumps(result)
    if request.method == 'PUT': # making the loan inactive
        upd_loan = Loan.query.get(id)
        request_data = request.get_json()
        u_active = request_data["active"]
        upd_loan.active = u_active
        db.session.commit()
        return {"msg":"Succeses"}

@app.route('/')
def hello():
    return 'Boooooks!'


if __name__ == '__main__':
    with app.app_context():db.create_all()
    app.run(debug = True)
