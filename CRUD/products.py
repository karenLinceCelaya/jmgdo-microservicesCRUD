from flask import Flask, jsonify, request
import json
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app = Flask("Product Server")
CORS(app)

swaggerui_blueprint = get_swaggerui_blueprint(
    '/products/docs',
    '<replace your host url>/swagger.json',
    config={'app_name': "Products microservice"}
)

app.register_blueprint(swaggerui_blueprint)

products = [
    {'id': 143, 'name': 'Notebook', 'price': 5.49},
    {'id': 144, 'name': 'Black Marker', 'price': 1.99}
]


@app.route('/swagger.json')
def static_file():
    return app.send_static_file("swagger.json")


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)


@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    id = int(id)
    product = [x for x in products if x["id"] == id][0]
    return jsonify(product)


@app.route('/products', methods=['POST'])
def add_product():
    products.append(request.get_json())
    return '', 201


@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    id = int(id)
    updated_product = json.loads(request.data)
    product = [x for x in products if x["id"] == id][0]
    for key, value in updated_product.items():
        product[key] = value
    return '', 204


@app.route('/products/<id>', methods=['DELETE'])
def remove_product(id):
    id = int(id)
    product = [x for x in products if x["id"] == id][0]
    products.remove(product)
    return '', 204

app.run(port=5000,debug=True)
