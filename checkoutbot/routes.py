from flask_restx import Namespace, fields, Resource
from http import HTTPStatus
from models import BaseModel
from typing import Dict, List, Type
import os

model_name = os.getenv("MODEL_NAME")
if not model_name:
    model_name = "BaseModel"


print(f"Using model: {model_name}")

model = BaseModel.get_model(model_name=model_name)(register_count=25)

print("Model successfully initialized!")




health_namespace = Namespace('health', description='Namespace for server health')

register_namespace = Namespace('register', description='Namespace for registers')

add_namespace = Namespace('add', description='Namespace for item customer to registers')

checkout_namespace = Namespace('checkout', description='Namespace for checkout')

clear_namespace = Namespace('clear', description="Clear all registers. Start a new state")

register_model = register_namespace.model(
    'Register', {
        'register_count' : fields.Integer(description="Total count of registers operating"),
        'registers' : fields.Raw(description="register detail data"),
    }
)


add_model = add_namespace.model(
    'Add', {
        'customer_id': fields.Integer(descripton="customer id"),
        'item_id': fields.Integer(description="item id")
    }
)

checkout_model = checkout_namespace.model(
    'Checkout',
    {
        'customer_id': fields.Integer(descripton="customer id")
    }
)


@health_namespace.route('')
class GetHealth(Resource):
    def get(self):
        """
            Get Server Health
        """
        status = "OK"

        return status, HTTPStatus.OK




@register_namespace.route('')
class Register(Resource):
    @register_namespace.marshal_with(register_model)
    @register_namespace.doc(
        description="Retrieve all orders"
    )
    def get(self):
        """
            Get Current Registers
        """
        registers = model
        return registers, HTTPStatus.OK



@add_namespace.route('')
class Register(Resource):
    @add_namespace.marshal_with(add_model)
    @add_namespace.expect(add_model)
    def post(self):
        """
            Add user to register with item
        """

        data = add_namespace.payload

        model.add(data["customer_id"], data["item_id"])

        return data, HTTPStatus.CREATED

@checkout_namespace.route('')
class Checkout(Resource):
    @checkout_namespace.marshal_with(register_model)
    @checkout_namespace.expect(checkout_model)
    def post(self):
        """
            Checkout customer from register
        """

        data = register_namespace.payload

        model.checkout(data["customer_id"])

        registers = model

        return registers, HTTPStatus.CREATED


@clear_namespace.route('')
class ClearSate(Resource):
    @clear_namespace.marshal_with(register_model)
    def delete(self):
        """
            Register cleared
        """
        model.clear()
        registers = model
        return registers, HTTPStatus.NO_CONTENT

    
        