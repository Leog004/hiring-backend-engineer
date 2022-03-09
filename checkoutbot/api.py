from flask import Flask
from flask_restx import Api
from routes import register_namespace, health_namespace, add_namespace, checkout_namespace, clear_namespace



app = Flask("checkoutbot")


api=Api(app,doc='/docs')
api.add_namespace(health_namespace)
api.add_namespace(register_namespace)
api.add_namespace(add_namespace)
api.add_namespace(checkout_namespace)
api.add_namespace(clear_namespace)


if __name__ == "__main__":
    app.run(debug=True)
