from flask_app.config.mysqlconnection import connectToMySQL
import re	

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Guest:
    db = "log_in_schema"
    def __init__(self,guest_data):
        self.id = guest_data['id']
        self.first_name = guest_data['first_name']
        self.last_name = guest_data['last_name']
        self.email = guest_data['email']
        self.password = guest_data['password']
        self.created_at = guest_data['created_at']
        self.updated_at = guest_data['updated_at']


    @staticmethod
    def validate(guest):
        is_valid = True
        query = "SELECT * FROM guest WHERE email= %(email)s;"
        results = connectToMySQL(Guest.db).query_db(query,guest)
        print (results)

        if len(results)>=1:
            flash("email already taken")
            is_valid = False
        if not EMAIL_REGEX.match(guest['email']):
            flash("Invalid Email!")
            is_valid = False
        if len(guest['first_name']) < 3:
            flash("First name must be at least 3 characters")
            is_valid = False
        if len(guest['last_name']) < 3:
            flash("Last name must be at least 3 characters")
            is_valid = False
        if len(guest['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if guest['password'] != guest['confirm']:
            flash("Password doesn't match")
            is_valid = False
        return is_valid


    @classmethod
    def save(cls, guest_data):
        query = "INSERT INTO guest ( first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query,guest_data)

    @classmethod
    def get_all (cls):
        query = "SELECT * FROM guest;"
        results = connectToMySQL(cls.db).query_db(query)
        guest = []
        for row in results:
            guest.append(cls(row))
        return guest

    @classmethod
    def get_by_email(cls,guest_data):
        query = "SELECT  * FROM guest WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, guest_data)
        if len(results)<1:
            # return array not string!!!!
            return False
        return cls(results[0])

    @classmethod
    def get_by_id (cls, guest_data):
        query = "SELECT * FROM guest WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,guest_data)
        return cls(results[0])
