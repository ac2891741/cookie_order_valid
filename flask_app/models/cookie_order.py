from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Customer:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.cookie_type = data["cookie_type"]
        self.num_of_boxes = data["num_of_boxes"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
            
        query = "SELECT * FROM cookie_orders;"

        results = connectToMySQL('cookie_orders').query_db(query)

        users = []

        for order in results:
            users.append(cls(order))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO cookie_orders (name, cookie_type, num_of_boxes) VALUES (%(name)s, %(cookie_type)s, %(num_of_boxes)s);"
        return connectToMySQL('cookie_orders').query_db(query, data)

    @classmethod
    def select_user(cls, order_id):
        query = "SELECT * FROM cookie_orders WHERE id = %(id)s;"
        data = {
            'id':order_id
        }

        result = connectToMySQL('cookie_orders').query_db(query, data)
        if result:
            order = result[0]
            return order

        return False

    @classmethod
    def update(cls, data):
        query = "UPDATE cookie_orders set name = %(name)s, cookie_type = %(cookie_type)s, num_of_boxes= %(num_of_boxes)s WHERE id = %(id)s; "
        return connectToMySQL('cookie_orders').query_db(query, data)

    @classmethod
    def remove(cls, data):
        query = "DELETE FROM cookie_orders WHERE id = %(id)s;"
        return connectToMySQL('cookie_orders').query_db(query, data)

    @staticmethod
    def validate_user(customer):
        is_valid = True
        if len(customer["name"]) <= 0 or len(customer["cookie_type"]) <= 0 or len(customer["num_of_boxes"]) <= 0:
            is_valid = False
            flash("All Fields Required")
            return is_valid
        if len(customer['name']) < 2:
            flash("Name Required, Must Be 2 Characters Long")
            is_valid = False
        if len(customer['cookie_type']) < 2:
            flash("Cookie Type Required")
            is_valid = False
        if int(customer['num_of_boxes']) < 0:
            flash("Please Enter A Valid Number Of Boxes")
            is_valid = False
        return is_valid