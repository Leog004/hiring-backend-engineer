import flask
from flask_restx import Namespace, fields, Resource
from http import HTTPStatus
from models import BaseModel
from decouple import config
from werkzeug.exceptions import Conflict, BadRequest
from utils import checkIfInteger

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
        #'register_count' : fields.Integer(description="Total count of registers operating"),
        'registers' : fields.Raw(description="register detail data"),
    }
)


add_model = add_namespace.model(
    'Add', {
        'customer_id': fields.Integer(descripton="customer id", required=True),
        'item_id': fields.Integer(description="item id", required=True)
    }
)

checkout_model = checkout_namespace.model(
    'Checkout',
    {
        'customer_id': fields.Integer(descripton="customer id", required=True)
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
        description="Retrieve all registers"
    )
    def get(self):
        """
            Get Current Registers
        """
        registers = model
        return registers, HTTPStatus.OK


@add_namespace.route('')
class AddItemRegister(Resource):
    @add_namespace.marshal_with(register_model)
    @add_namespace.expect(add_model)
    def post(self):
        """
            Add item to user. 
            Add user to register with item
        """

        try: 
            customer_id = ""
            item_id = ""

            if API_TESTING: 

                customer_id = flask.request.form["customer_id"]
                item_id = flask.request.form["item_id"]
            
            else:
                data = add_namespace.payload

                if checkIfInteger(**data) is False:
                    raise ValueError("value inserted was not an itenger or value must be greater than 0")

                customer_id = data["customer_id"]
                item_id = data["item_id"]


            model.add(customer_id, item_id)

            #response = dict(registers=model.registers, add = dict(customer_id=customer_id, item_id=item_id))

            return model, HTTPStatus.CREATED

        except Exception as e:
            raise BadRequest(f"Bad request was made: error: {e}")



@checkout_namespace.route('')
class Checkout(Resource):
    @checkout_namespace.marshal_with(register_model)
    @checkout_namespace.expect(checkout_model)
    def post(self):
        """
            Checkout customer from register
        """
        try: 
            customer_id = ""
            
            if API_TESTING: 
                customer_id = flask.request.form["customer_id"]
            
            else:
                data = register_namespace.payload

                if checkIfInteger(**data) is False:
                    raise ValueError("value inserted was not an itenger or value must be greater than 0")
                
                customer_id = data["customer_id"]


            model.checkout(customer_id)

            registers = model

            return registers, HTTPStatus.CREATED

        except Exception as e:
            raise BadRequest(f"Bad request was made: error: {e}")


@clear_namespace.route('')
class ClearSate(Resource):
    @clear_namespace.marshal_with(register_model)
    def delete(self):
        """
            All states cleared
        """
        model.clear()
        #registers = model
        return "", HTTPStatus.NO_CONTENT

    
        