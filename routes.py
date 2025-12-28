# routes.py
from flask import Blueprint, request, jsonify, abort
from extensions import mongo
from schemas import ClientSchema, ReservationSchema, AvisSchema, AdminSchema, PackageSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from datetime import datetime, timezone
from bson import ObjectId

api_bp = Blueprint('api', __name__)

# Schema instances
client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)
avis_schema = AvisSchema()
avis_list_schema = AvisSchema(many=True)
admin_schema = AdminSchema()
package_schema = PackageSchema()
packages_schema = PackageSchema(many=True)

@api_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the API!"})

@api_bp.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    required_fields = ['nom_complet', 'age', 'sexe', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    if isinstance(data.get('destinations_preferees'), list):
        data['destinations_preferees'] = ','.join(data['destinations_preferees'])
    if isinstance(data.get('langues_parlees'), list):
        data['langues_parlees'] = ','.join(data['langues_parlees'])

    if mongo.db.clients.find_one({"email": data['email']}):
        return jsonify({"error": "Email already in use"}), 400

    try:
        new_client_data = client_schema.load(data)
        result = mongo.db.clients.insert_one(new_client_data)
        new_client = mongo.db.clients.find_one({"_id": result.inserted_id})
        return jsonify(client_schema.dump(new_client)), 201
    except Exception:
        return jsonify({"error": "Failed to create client"}), 400

@api_bp.route('/clients', methods=['GET'])
def get_clients():
    clients = list(mongo.db.clients.find())
    return jsonify(clients_schema.dump(clients))

@api_bp.route('/clients/<string:id>', methods=['GET'])
def get_client(id):
    try:
        client = mongo.db.clients.find_one({"_id": ObjectId(id)})
        if not client:
            abort(404, description="Client not found")
        return jsonify(client_schema.dump(client))
    except Exception:
        return jsonify({"error": "Invalid ID format or client not found"}), 400

@api_bp.route('/clients/<string:id>', methods=['PUT'])
def update_client(id):
    data = request.get_json()
    if isinstance(data.get('destinations_preferees'), list):
        data['destinations_preferees'] = ','.join(data['destinations_preferees'])
    if isinstance(data.get('langues_parlees'), list):
        data['langues_parlees'] = ','.join(data['langues_parlees'])

    try:
        data.pop('_id', None)
        result = mongo.db.clients.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count == 0:
            abort(404, description="Client not found")
        updated_client = mongo.db.clients.find_one({"_id": ObjectId(id)})
        return jsonify(client_schema.dump(updated_client))
    except Exception:
        return jsonify({"error": "Invalid ID format or update failed"}), 400

@api_bp.route('/clients/<string:id>', methods=['DELETE'])
def delete_client(id):
    try:
        result = mongo.db.clients.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            abort(404, description="Client not found")
        return jsonify({"message": "Client deleted"}), 200
    except Exception:
        return jsonify({"error": "Invalid ID format or deletion failed"}), 400

@api_bp.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()
    try:
        if 'client_id' in data:
            data['client_id'] = ObjectId(data['client_id'])

        # Validate only expected fields
        new_res_data = reservation_schema.load(data)

        # Add date_reservation AFTER validation
        new_res_data['date_reservation'] = datetime.now(timezone.utc)

        result = mongo.db.reservations.insert_one(new_res_data)
        new_reservation = mongo.db.reservations.find_one({"_id": result.inserted_id})
        return jsonify(reservation_schema.dump(new_reservation)), 201

    except Exception as e:
        print("Error creating reservation:", str(e))
        return jsonify({"error": "Failed to create reservation", "details": str(e)}), 400

    except Exception as e:
        # Print actual error in terminal/log
        print("Error creating reservation:", str(e))
        return jsonify({"error": "Failed to create reservation", "details": str(e)}), 400

@api_bp.route('/reservations', methods=['GET'])
def get_reservations():
    client_id_str = request.args.get('client_id')
    email = request.args.get('email')
    query_filter = {}

    if email:
        client = mongo.db.clients.find_one({"email": email})
        if not client:
            return jsonify({"error": "Client not found"}), 404
        query_filter['client_id'] = client['_id']
    elif client_id_str:
        try:
            query_filter['client_id'] = ObjectId(client_id_str)
        except Exception:
            return jsonify({"error": "Invalid client_id format"}), 400
    else:
        return jsonify({"error": "client_id or email query parameter required"}), 400

    reservations = list(mongo.db.reservations.find(query_filter))
    return jsonify(reservations_schema.dump(reservations))

@api_bp.route('/reservations/<string:id>', methods=['GET'])
def get_reservation(id):
    try:
        reservation = mongo.db.reservations.find_one({"_id": ObjectId(id)})
        if not reservation:
            abort(404, description="Reservation not found")
        return jsonify(reservation_schema.dump(reservation))
    except Exception:
        return jsonify({"error": "Invalid ID format or reservation not found"}), 400

@api_bp.route('/reservations/<string:id>', methods=['PUT'])
def update_reservation(id):
    data = request.get_json()
    try:
        if 'client_id' in data:
            data['client_id'] = ObjectId(data['client_id'])
        data.pop('_id', None)
        result = mongo.db.reservations.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count == 0:
            abort(404, description="Reservation not found")
        updated_reservation = mongo.db.reservations.find_one({"_id": ObjectId(id)})
        return jsonify(reservation_schema.dump(updated_reservation))
    except Exception:
        return jsonify({"error": "Invalid ID format or update failed"}), 400

@api_bp.route('/reservations/<string:id>', methods=['DELETE'])
def delete_reservation(id):
    try:
        result = mongo.db.reservations.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            abort(404, description="Reservation not found")
        return jsonify({"message": "Reservation deleted"}), 200
    except Exception:
        return jsonify({"error": "Invalid ID format or deletion failed"}), 400

@api_bp.route('/avis', methods=['POST'])
def create_avis():
    data = request.get_json()
    try:
        if 'client_id' in data:
            data['client_id'] = ObjectId(data['client_id']) 
        if 'reservation_id' in data and data['reservation_id']:
            data['reservation_id'] = ObjectId(data['reservation_id'])

        validated_data = avis_schema.load(data)

        validated_data['date_avis'] = datetime.now(timezone.utc)

        result = mongo.db.avis.insert_one(validated_data)
        new_avis = mongo.db.avis.find_one({"_id": result.inserted_id})
        return jsonify(avis_schema.dump(new_avis)), 201

    except Exception as e:
        print("Error creating review:", str(e))
        return jsonify({"error": "Failed to create review", "details": str(e)}), 400
@api_bp.route('/avis', methods=['GET'])
def get_avis():
    avis_list = list(mongo.db.avis.find())
    return jsonify(avis_list_schema.dump(avis_list))

@api_bp.route('/avis/<string:id>', methods=['DELETE'])
def delete_avis(id):
    try:
        result = mongo.db.avis.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            abort(404, description="Review not found")
        return jsonify({"message": "Review deleted"}), 200
    except Exception:
        return jsonify({"error": "Invalid ID format or deletion failed"}), 400

@api_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin = mongo.db.admins.find_one({"email": data.get('email')})
    if not admin or not check_password_hash(admin.get('mot_de_passe'), data.get('mot_de_passe')):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=str(admin['_id']))
    return jsonify({"access_token": token}), 200

@api_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    current_admin_id = get_jwt_identity()
    try:
        admin = mongo.db.admins.find_one({"_id": ObjectId(current_admin_id)})
        if not admin:
            abort(404, description="Admin not found")
    except Exception:
        return jsonify({"error": "Invalid admin ID in token"}), 401

    clients = list(mongo.db.clients.find())
    reservations = list(mongo.db.reservations.find())
    avis = list(mongo.db.avis.find())
    packages = list(mongo.db.packages.find())

    return jsonify({
        "admin": {
            "id": str(admin['_id']),
            "email": admin['email']
        },
        "clients": clients_schema.dump(clients),
        "reservations": reservations_schema.dump(reservations),
        "avis": avis_list_schema.dump(avis),
        "packages": packages_schema.dump(packages)
    }), 200

@api_bp.route('/packages', methods=['GET'])
def get_packages():
    rent_type = request.args.get('rent_type')
    property_type = request.args.get('property_type')
    city = request.args.get('city')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)

    query_filter = {}

    if rent_type and rent_type != "All":
        query_filter['rent_type'] = {"$regex": rent_type, "$options": "i"}
    if property_type and property_type != "All":
        query_filter['property_type'] = {"$regex": property_type, "$options": "i"}
    if city and city != "Localization":
        query_filter['city'] = {"$regex": city, "$options": "i"}
    if price_min is not None:
        query_filter['price_min'] = {"$gte": price_min}
    if price_max is not None:
        query_filter['price_max'] = {"$lte": price_max}

    packages = list(mongo.db.packages.find(query_filter))
    return jsonify(packages_schema.dump(packages)), 200

@api_bp.route('/packages/<string:id>', methods=['GET'])
def get_package(id):
    try:
        package = mongo.db.packages.find_one({"_id": ObjectId(id)})
        if not package:
            abort(404, description="Package not found")
        return jsonify(package_schema.dump(package)), 200
    except Exception:
        return jsonify({"error": "Invalid ID format or package not found"}), 400

@api_bp.route('/packages', methods=['POST'])
@jwt_required()
def create_package():
    data = request.get_json()
    try:

        validated_data = package_schema.load(data)

        validated_data['created_at'] = datetime.now(timezone.utc)
        validated_data['updated_at'] = datetime.now(timezone.utc)

        result = mongo.db.packages.insert_one(validated_data)
        new_package = mongo.db.packages.find_one({"_id": result.inserted_id})
        return jsonify(package_schema.dump(new_package)), 201

    except Exception as e:
        print("Error creating package:", str(e))
        return jsonify({"error": "Failed to create package", "details": str(e)}), 400

@api_bp.route('/packages/<string:id>', methods=['PUT'])
@jwt_required()
def update_package(id):
    data = request.get_json()
    try:
        data['updated_at'] = datetime.now(timezone.utc)
        data.pop('_id', None)
        result = mongo.db.packages.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count == 0:
            abort(404, description="Package not found")
        updated_package = mongo.db.packages.find_one({"_id": ObjectId(id)})
        return jsonify(package_schema.dump(updated_package)), 200
    except Exception:
        return jsonify({"error": "Invalid ID format or update failed"}), 400

@api_bp.route('/packages/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_package(id):
    try:
        result = mongo.db.packages.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            abort(404, description="Package not found")
        return jsonify({"message": "Package deleted successfully"}), 200
    except Exception:
        return jsonify({"error": "Invalid ID format or deletion failed"}), 400

@api_bp.route('/admin/reservations/<string:id>/confirm', methods=['POST'])
@jwt_required()
def confirm_reservation(id):
    try:
        result = mongo.db.reservations.update_one({"_id": ObjectId(id)}, {"$set": {"status": "confirmed"}})
        if result.matched_count == 0:
            abort(404, description="Reservation not found")
        return jsonify({"message": "Reservation confirmed."})
    except Exception:
        return jsonify({"error": "Invalid ID format or confirmation failed"}), 400
