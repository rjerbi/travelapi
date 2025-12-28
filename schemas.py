from marshmallow import Schema, fields
from marshmallow.fields import Field
from bson import ObjectId

# Custom field for ObjectId handling
class ObjectIdField(Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)

class ClientSchema(Schema):
    _id = ObjectIdField(dump_only=True)  
    nom_complet = fields.Str(required=True)
    age = fields.Int(required=True)
    sexe = fields.Str(required=True)
    profession = fields.Str()
    destinations_preferees = fields.Str()
    email = fields.Email(required=True)
    telephone = fields.Str()
    nationalite = fields.Str()
    type_voyage_prefere = fields.Str()
    budget_estime = fields.Float()
    langues_parlees = fields.Str()

class ReservationSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    client_id = ObjectIdField(required=True)
    destination = fields.Str(required=True)
    dates = fields.Str(required=True)
    nombre_personnes = fields.Int(required=True)
    type_chambre = fields.Str()
    options_specifiques = fields.Str()
    total_frais = fields.Float(required=True)
    date_reservation = fields.DateTime(dump_only=True)

class AvisSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    client_id = ObjectIdField(required=True)
    reservation_id = ObjectIdField(allow_none=True)
    commentaire = fields.Str(required=True)
    date_avis = fields.DateTime(dump_only=True)

class AdminSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    email = fields.Email(required=True)
    mot_de_passe = fields.Str(load_only=True)

class PackageSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    rent_type = fields.Str(load_default="All")
    property_type = fields.Str(load_default="All")
    city = fields.Str(load_default="Localization")
    price_min = fields.Float(allow_none=True, load_default=None)
    price_max = fields.Float(allow_none=True, load_default=None)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
