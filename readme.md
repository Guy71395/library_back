# Guy's Library

This is a library management system that allows users to view, add, and delete books, customers, and loan records. It is built using Flask, SQLAlchemy, and CORS.

## Requirements

- Flask
- SQLAlchemy
- Flask-SQLAlchemy
- Flask-CORS

## Running the Project

- the project is live on : https://guys-library.netlify.app/
- the API is live at : https://library-back-a0z7.onrender.com

## API Endpoints

The following API endpoints are available for interacting with the library management system:

- `GET /books/`: Returns a list of all books in the library
- `POST /books/`: Adds a new book to the library
- `GET /books/<id>`: Returns the book with the specified ID
- `PUT /books/<id>`: Updates the book with the specified ID's active attribute, making it inactive
- `GET /customers/`: Returns a list of all customers in the library
- `POST /customers/`: Adds a new customer to the library
- `PUT /customers/<id>`: Updates the customer with the specified ID's active attribute, making it inactive
- `GET /loans/`: Returns a list of all loans in the library
- `POST /loans/`: Adds a new loan to the library
- `PUT /loans/<id>`: Updates the loan with the specified ID's active attribute, making it inactive


