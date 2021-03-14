import sqlite3
import random
import string
import logging
from collections import OrderedDict
from flask import Flask, jsonify, request, abort

DB_FILE = "database/MDS.db"
LOG_FILE = "log/MDS.log"
app = Flask(__name__)
logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s",
        filename=LOG_FILE, level=logging.INFO)


INSERT_PACKAGE = """
INSERT INTO packages ('id', 'destination_address', 'destination_city') 
VALUES (?, ?, ?);
"""

UPDATE_TRANSIT = """
INSERT INTO transits ('transit_id','package_id','transit_address') 
values (?,?,?);
"""

PACKAGE_DELIVERED = """
UPDATE packages SET delivered = 1 where id=?;
"""

CHECK_STATUS = """
SELECT timestamp, transit_address FROM transits where package_id=? order by timestamp asc;
"""

def DB_insert(sql, *params):
    """
    To insert into a table
    parameters:
        sql (str): insert/update query statement
        params (str): extended list of values in the sql statement
    returns:
        None
    """
    try:
        app.logger.info("connecting to DB")
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute(sql, (params))
            app.logger.info("executed insert query %s with params as %s",sql,(params))
    except Exception as err:
        app.logger.error('Query Failed: %s\nError: %s' % (sql, str(err)))

def DB_fetch(sql, *params):
    """
    To fetch rows from a table
    parameters:
        sql (str): select query statement
        params (str): extended list of values in the sql statement
    returns:
        list of rows with each row as tuple
    """
    try:
        app.logger.info("connecting to DB")
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute(sql, (params))
            app.logger.info("executed insert query %s with params as %s",sql,(params))
            return cur.fetchall()
    except Exception as err:
                app.logger.error('Query Failed: %s\nError: %s' % (sql, str(err)))

@app.errorhandler(Exception)
def handle_bad_request(error):
    """
    To handle all error codes
    parameters:
        error (Exception type): To catch the error execption
    returns:
        json object with 500 error code
    """
    app.logger.error("error occured %s", error)
    resp = jsonify("Error Occurred!!")
    resp.status_code = 500
    return resp

@app.route("/create", methods=["POST"])
def create_package():
    """
    Function to create package 
    parameters:
        destination_address (POST method argument): contains destination address
        destination_city (POST method argument): contains destination city
    returns:
        jsonified package unique id
    """
    if request.method == "POST":
        package_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
        destination_address = request.json["destination_address"]
        destination_city = request.json["destination_city"]
        #destination_address = request.form["destination_address"]
        #destination_city = request.form["destination_city"]
        app.logger.info("Creating package with package id %s", package_id)
        DB_insert(INSERT_PACKAGE, package_id, destination_address, destination_city)
        return jsonify(package_id)

@app.route("/update",methods=["PUT"])
def update_transit():
    """
    Function to add transit
    parameters:
        package_id (PUT method argument): contains uniquely identifiable package id
        transit_city (PUT method argument): contains transit city name
    returns:
        jsonified unique id
    """
    if request.method == "PUT":
        transit_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
        package_id = request.json["package_id"]
        transit_city = request.json["transit_city"]
        app.logger.info("Creating transit point with id %s", transit_id)
        DB_insert(UPDATE_TRANSIT, transit_id, package_id, transit_city)
        return jsonify(transit_id)

@app.route("/mark_delivered", methods=["PUT"])
def mark_delivered():
    """
    Function to mark delivery of package
    parameters:
        package_id (PUT method argument): contains uniquely identifiable package id
    returns:
        jsonified message to ACK
    """
    if request.method == "PUT":
        package_id = request.json["package_id"]
        app.logger.info("marking delivered for package %s", package_id)
        DB_insert(PACKAGE_DELIVERED, package_id)
        return jsonify("Thanks!!")

@app.route("/check_progress",methods=["GET"])
def check_progress():
    """
    Function to check progress
    parameters:
        package_id (PUT method argument): contains uniquely identifiable package id
    returns:
        jsonified key value pairs with key as time stamp and value as transit place
    """
    if request.method == "GET":
        package_id = request.args.get("package_id")
        app.logger.info("checking the progress for package %s",package_id)
        transits = DB_fetch(CHECK_STATUS, package_id)
        transits_dict = OrderedDict()
        for each_transit in transits:
            transits_dict[each_transit[0]] = each_transit[1]
        return jsonify(transits_dict)

if __name__ == "__main__":
    app.run(ssl_context=("key_certificate/cert.pem","key_certificate/key.pem"), debug=True, threaded=True)
