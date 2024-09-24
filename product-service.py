from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Float, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)

@app.route('/products', methods = ['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price, 'quantity': p.quantity} for p in products])

@app.route('/products/<int:product_id>', methods = ['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'quantity': product.quantity})

@app.route('/products', methods = ['POST'])
def add_product():
    data = request.json
    new_product = Product(name = data ['name'], price = data['price'], quantity = data['quantity'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product was successfully added'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True, port = 5000)