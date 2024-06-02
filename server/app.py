from flask import Flask, request, make_response, jsonify
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)

    data = request.form
    if 'name' in data:
        bakery.name = data['name']

    db.session.commit()

    return make_response(jsonify(bakery.to_dict()), 200)

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    if 'name' not in data or 'price' not in data:
        return make_response(jsonify({'error': 'Name and price are required'}), 400)

    baked_good = BakedGood(name=data['name'], price=float(data['price']))
    db.session.add(baked_good)
    db.session.commit()

    return make_response(jsonify(baked_good.to_dict()), 201)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if not baked_good:
        return make_response(jsonify({'error': 'Baked good not found'}), 404)

    db.session.delete(baked_good)
    db.session.commit()

    return make_response(jsonify({'message': 'Baked good deleted successfully'}), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
