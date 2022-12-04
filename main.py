import json
import mysql.connector
from flask import Flask, request, make_response, request, render_template, blueprints
from datetime import datetime,timedelta,date,time
import jwt
from fun_blueprint.fun_blueprint import fun_blueprint

con = mysql.connector.connect(host="localhost",user="root",password="Shakti123",database="flask_tutorial",auth_plugin="mysql_native_password")
cur = con.cursor(dictionary=True)
con.autocommit=True

def get_data():
    cur.execute("SELECT * from new_table")
    result = cur.fetchall()
    return json.dumps(result)

def add_data(data):
    cur.execute(f"INSERT INTO new_table(ID,NAME,EMAIL,PHONE,password,role)VALUES('{data['id']}', '{data['NAME']}', '{data['EMAIL']}', '{data['PHONE']}', '{data['password']}', '{data['role']}')")
    return "user created"

def update_data(x):
    cur.execute(f"UPDATE new_table SET NAME='{x['NAME']}', EMAIL='{x['EMAIL']}', PHONE='{x['PHONE']}', password='{x['password']}', role='{x['role']}' WHERE ID={x['ID']}")
    return "User is updated"

def del_data(id):
    cur.execute(f"DELETE FROM new_table WHERE ID={id}")
    return "User is deleted"

def patch_data(z,id):
    cur.execute(f"UPDATE new_table SET NAME='{z['NAME']}', EMAIL='{z['EMAIL']}' WHERE ID={id}")
    return "User is patched"

def encode_jwt(data):
    cur.execute(f"SELECT ID, NAME, PHONE, EMAIL, role_id FROM new_table WHERE EMAIL='{data['email']}' AND password='{data['password']}'")
    result = cur.fetchall()
    userdata = result[0]
    exp_time = datetime.now() + timedelta(minutes=15)
    exp_epoch_time = int(exp_time.timestamp())
    payload = {"payload":userdata,"exp":exp_epoch_time}
    token = jwt.encode(payload, "shakti", algorithm="HS256")
    return make_response({"token" : token}, 200)

def decode_jwt(endpoint):
   def inner1(func):
        def inner2():
            authorization = request.headers.get("authorization")
            auth = authorization.split(" ")[1]
            jwt_decoded = jwt.decode(auth, "shakti", algorithms="HS256")
            role_id = jwt_decoded['payload']['role_id']
            #print(role_id)
            cur.execute(f"SELECT roles from accessibilty_view where endpoint = '{endpoint}'")
            result = cur.fetchall()
            allowed_role = json.loads(result[0]['roles'])
            #print(allowed_role)
            if role_id in allowed_role:
                return func()
            else:
                return make_response(" ACCESS NOT ALLOWED")
        return inner2
   return inner1


app = Flask(__name__)

app.register_blueprint(fun_blueprint, url_prefix="/fun_blueprint")

@app.route("/get")
@decode_jwt("/get")
def read_data():
    return get_data()

@app.route("/add", methods=["POST"])
def send_data():
    return add_data(request.form)

@app.route("/put", methods=["PUT"])
def put_data():
    return update_data(request.form)

@app.route("/del/<y>", methods=["DELETE"])
def rem_data(y):
    return del_data(y)

@app.route("/patch/<z>", methods=["PATCH"])
def patch_data(z):
    return patch_data(request.form,z)

@app.route("/login", methods=["POST"])
def JWT_data():
    # here: login, should have both GET and POST request
    return encode_jwt(request.form)


# todo change here: protection/guard block: if name == __main__: only call app.run() if this is main entry point for app
#  this is a bit of a complicated subject, but essentially eventually you're going to make this a package, not just a script
#  a package might be imported by another module later one. If app.run() were not protected by name == main, then when this
#  script were imported it would run app.run again, which would break the program
#  __name__ is a built in special variable; it's value will only be __main__ if this is the main entry point of the app
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)