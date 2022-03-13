import os
import flask
from flask import Flask

from models import BaseModel


app = Flask("checkoutbot")

model_name = os.getenv("MODEL_NAME")
if not model_name:
    model_name = "BaseModel"
print(f"Using model: {model_name}")
model = BaseModel.get_model(model_name=model_name)(register_count=25)
print("Model successfully initialized!")


@app.route("/health", methods=["GET"])
def get_health_check():
    return "OK"


@app.route("/registers", methods=["GET"])
def get_registers():
    return flask.make_response(dict(registers=model.registers), 200)


@app.route("/add", methods=["POST"])
def add():
    customer_id = flask.request.form["customer_id"]
    item_id = flask.request.form["item_id"]
    model.add(customer_id=customer_id, item_id=item_id)
    response = dict(
        registers=model.registers, add=dict(customer_id=customer_id, item_id=item_id)
    )
    return flask.make_response(response, 201)


@app.route("/checkout", methods=["POST"])
def checkout():
    customer_id = flask.request.form["customer_id"]
    model.checkout(customer_id=customer_id)
    response = dict(registers=model.registers, checkout=dict(customer_id=customer_id))
    return flask.make_response(response, 201)


@app.route("/state", methods=["DELETE"])
def delete_state():
    model.clear()
    return flask.make_response("", 204)


if __name__ == "__main__":
    app.run(debug=True)
