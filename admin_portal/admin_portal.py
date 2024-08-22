from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Dummy database for orders
orders = []

@app.route('/')
def admin_orders():
    return render_template('admin_orders.html', orders=orders)

@app.route('/api/orders')
def api_orders():
    return jsonify({'orders': orders})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received webhook data:", data)  # Debug line
    if data and 'event' in data and data['event'] == 'purchase':
        order = {
            'order_id': len(orders) + 1,
            'product_id': data['product_id'],
            'amount': data['amount']
        }
        orders.append(order)
        print("Order added:", order)  # Debug line
        return jsonify({'status': 'Order created', 'order': order}), 200
    return jsonify({'status': 'Invalid webhook data'}), 400

if __name__ == '__main__':
    app.run(port=5001, debug=True)
