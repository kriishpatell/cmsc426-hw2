import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

carts = {}

PRODUCT_SERVICE_URL = os.environ.get('PRODUCT_SERVICE_URL', 'http://localhost:5000')

@app.route('/', methods=['GET'])
def cart_service_home():
    return "This is the cart service"

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    if user_id not in carts:
        return jsonify({'message': 'Cart not found'}), 404
    cart = carts[user_id]
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return jsonify({'cart': list(cart.values()), 'total': total})

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    quantity = request.json.get('quantity', 1)
    try:
        response = requests.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}')
        response.raise_for_status()
        product = response.json()
    except requests.RequestException as e:
        return jsonify({'message': f'Error fetching product: {str(e)}'}), 500

    if user_id not in carts:
        carts[user_id] = {}
    
    if product_id in carts[user_id]:
        carts[user_id][product_id]['quantity'] += quantity
    else:
        carts[user_id][product_id] = {
            'id': product_id,
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity
        }
    
    return jsonify({'message': 'Product added to cart'})

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    if user_id not in carts or product_id not in carts[user_id]:
        return jsonify({'message': 'Product not in cart'}), 404
    
    quantity = request.json.get('quantity', 1)
    
    if carts[user_id][product_id]['quantity'] <= quantity:
        del carts[user_id][product_id]
    else:
        carts[user_id][product_id]['quantity'] -= quantity
    
    return jsonify({'message': 'Product removed from cart'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
