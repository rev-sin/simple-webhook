from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Dummy data
products = [
    {'id': 1, 'name': 'Product 1', 'price': 10.00},
    {'id': 2, 'name': 'Product 2', 'price': 20.00}
]

# Dummy storage for orders
orders = []

# Admin portal webhook URL
ADMIN_PORTAL_WEBHOOK_URL = 'http://localhost:5001/webhook'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def products_list():
    return render_template('products.html', products=products)

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404

    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))
        order = {
            'order_id': len(orders) + 1,
            'product_id': product['id'],
            'quantity': quantity,
            'amount': product['price'] * quantity
        }
        orders.append(order)
        
        # Notify the admin portal
        response = requests.post(ADMIN_PORTAL_WEBHOOK_URL, json={
            'event': 'purchase',
            'product_id': product['id'],
            'amount': order['amount']
        })
        print("Webhook response:", response.json())  # Debug line

        return redirect(url_for('order_confirmation', order_id=order['order_id']))

    return render_template('product.html', product=product)

@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404
    return render_template('order_confirmation.html', order=order)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
