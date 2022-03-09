import flask
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


# @app.route("/health", methods=["GET"])
# def get_health_check():
#     return "OK"


# @app.route("/registers", methods=["GET"])
# def get_registers():
#     return flask.make_response(dict(registers=model.registers), 200)


# @app.route("/add", methods=["POST"])
# def add():
#     customer_id = flask.request.form["customer_id"]
#     item_id = flask.request.form["item_id"]
#     model.add(customer_id=customer_id)
#     response = dict(
#         registers=model.registers, add=dict(customer_id=customer_id, item_id=item_id)
#     )
#     return flask.make_response(response, 201)


# @app.route("/checkout", methods=["POST"])
# def checkout():
#     customer_id = flask.request.form["customer_id"]
#     model.checkout(customer_id=customer_id)
#     response = dict(registers=model.registers, checkout=dict(customer_id=customer_id))
#     return flask.make_response(response, 201)


# @app.route("/state", methods=["DELETE"])
# def delete_state():
#     model.clear()
#     return flask.make_response("", 204)


if __name__ == "__main__":
    app.run(debug=True)
