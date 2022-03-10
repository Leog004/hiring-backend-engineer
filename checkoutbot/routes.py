import flask
from flask_restx import Namespace, fields, Resource
from http import HTTPStatus
from models import BaseModel
from typing import Dict, List, Type
from decouple import config

API_TESTING = config('TESTING', default=False, cast=bool) # change to true when running the generator file to test routes

model = BaseModel(register_count=25)

print(f"Model successfully initialized! {model.__class__.__name__}")


"""
 ==============    NAMESPACES ================
"""

health_namespace = Namespace('health', description='Namespace for server health')

register_namespace = Namespace('register', description='Namespace for registers')

add_namespace = Namespace('add', description='Namespace for item customer to registers')

checkout_namespace = Namespace('checkout', description='Namespace for checkout')

clear_namespace = Namespace('clear', description="Clear all registers. Start a new state")


"""
 ==============    NAMESPACES MODELS ================
"""

register_model = register_namespace.model(
    'Register', {
        'register_count' : fields.Raw(description="Total count of registers operating"),
        'registers' : fields.Raw(description="register detail data"),
    }
)


add_model = add_namespace.model(
    'Add', {
        'customer_id': fields.Raw(descripton="customer id"),
        'item_id': fields.Raw(description="item id")
    }
)

checkout_model = checkout_namespace.model(
    'Checkout',
    {
        'customer_id': fields.Raw(descripton="customer id")
    }
)



"""
 ==============  NAMESPACE ROUTES  ================
"""

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
    @add_namespace.marshal_with(register_model)
    @add_namespace.expect(add_model)
    def post(self):
        """
            Add user to register with item
        """
        customer_id = ""
        item_id = ""

        if API_TESTING: 
            customer_id = flask.request.form["customer_id"]
            item_id = flask.request.form["item_id"]
        
        else:
            data = add_namespace.payload
            customer_id = data["customer_id"]
            item_id = data["item_id"]


        model.add(customer_id, item_id)

        return model, HTTPStatus.CREATED


@checkout_namespace.route('')
class Checkout(Resource):
    @checkout_namespace.marshal_with(register_model)
    @checkout_namespace.expect(checkout_model)
    def post(self):
        """
            Checkout customer from register
        """
        customer_id = ""
        
        if API_TESTING: 
            customer_id = flask.request.form["customer_id"]
        
        else:
            data = register_namespace.payload
            customer_id = data["customer_id"]


        model.checkout(customer_id)

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

    
        