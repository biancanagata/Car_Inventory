from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Visitor, visitor_schema, visitors_schema, Car, car_schema, cars_schema


api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'Good': 'job'}

@api.route('/visitors', methods = ['POST'])
@token_required
def create_visitor(current_user_token):
    name = request.json['name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    visitor = Visitor(name, email, phone_number, address, user_token = user_token )

    db.session.add(visitor)
    db.session.commit()

    response = visitor_schema.dump(visitor)
    return jsonify(response)

@api.route('/visitors', methods = ['GET'])
@token_required
def get_visitor(current_user_token):
    a_user = current_user_token.token
    visitors = Visitor.query.filter_by(user_token = a_user).all()
    response = visitors_schema.dump(visitors)
    return jsonify(response)


@api.route('/visitors/<id>', methods = ['GET'])
@token_required
def get_single_visitor(current_user_token, id):
    visitor = Visitor.query.get(id)
    response = visitor_schema.dump(visitor)
    return jsonify(response)


#Update endpoint
@api.route('/visitors/<id>', methods = ['POST','PUT'])
@token_required
def update_visitor(current_user_token,id):
    visitor = Visitor.query.get(id) 
    visitor.name = request.json['name']
    visitor.email = request.json['email']
    visitor.phone_number = request.json['phone_number']
    visitor.address = request.json['address']
    visitor.user_token = current_user_token.token

    db.session.commit()
    response = visitor_schema.dump(visitor)
    return jsonify(response)

# Delete Endpoint
@api.route('/visitors/<id>', methods = ['DELETE'])
@token_required
def delete_visitor(current_user_token, id):
    visitor = Visitor.query.get(id)
    db.session.delete(visitor)
    db.session.commit()
    response = visitor_schema.dump(visitor)
    return jsonify(response)
    
@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json.get('color')
    price = request.json.get('price')
    user_token = current_user_token.token

    car = Car(make=make, model=model, year=year, color=color, price=price, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response), 201

@api.route('/cars', methods=['GET'])
@token_required
def get_all_cars(current_user_token):
    cars = Car.query.filter_by(user_token=current_user_token.token).all()
    response = cars_schema.dump(cars)
    return jsonify(response), 200

@api.route('/cars/<id>', methods=['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = Car.query.get(id)
    if car.user_token != current_user_token.token:
        return jsonify({'message': 'Unauthorized'}), 403
    response = car_schema.dump(car)
    return jsonify(response), 200

@api.route('/cars/<id>', methods=['PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    if car.user_token != current_user_token.token:
        return jsonify({'message': 'Unauthorized'}), 403

    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.color = request.json.get('color')
    car.price = request.json.get('price')

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response), 200

@api.route('/cars/<id>', methods=['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    if car.user_token != current_user_token.token:
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response), 200
