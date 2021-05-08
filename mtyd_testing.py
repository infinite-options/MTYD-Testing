# To run program:  python3 io_api.py

# README:  if conn error make sure password is set properly in RDS PASSWORD section

# README:  Debug Mode may need to be set to False when deploying live (although it seems to be working through Zappa)

# README:  if there are errors, make sure you have all requirements are loaded
# pip3 install flask
# pip3 install flask_restful
# pip3 install flask_cors
# pip3 install Werkzeug
# pip3 install pymysql
# pip3 install python-dateutil

import os
import uuid
import boto3
import json
import math


from datetime import date, datetime, timedelta
import time
import calendar

from pytz import timezone
import random
import string
import stripe

from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_mail import Mail, Message

# used for serializer email and error handling
# from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
# from flask_cors import CORS

from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.security import generate_password_hash, check_password_hash


#  NEED TO SOLVE THIS
# from NotificationHub import Notification
# from NotificationHub import NotificationHub

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from twilio.rest import Client

from dateutil.relativedelta import *
from decimal import Decimal

from hashlib import sha512
from math import ceil
import string
import random

# BING API KEY
# Import Bing API key into bing_api_key.py

#  NEED TO SOLVE THIS
# from env_keys import BING_API_KEY, RDS_PW

import decimal
import sys
import json
import pytz
import pymysql
import requests

# RDS_HOST = 'pm-mysqldb.cxjnrciilyjq.us-west-1.rds.amazonaws.com'
RDS_HOST = "io-mysqldb8.cxjnrciilyjq.us-west-1.rds.amazonaws.com"
# RDS_HOST = 'localhost'
RDS_PORT = 3306
# RDS_USER = 'root'
RDS_USER = "admin"
# RDS_DB = 'feed_the_hungry'
RDS_DB = "nitya"

# app = Flask(__name__)
app = Flask(__name__, template_folder="assets")









# --------------- Stripe Variables ------------------
# these key are using for testing. Customer should use their stripe account's keys instead
import stripe


# STRIPE AND PAYPAL KEYS
paypal_secret_test_key = os.environ.get('paypal_secret_key_test')
paypal_secret_live_key = os.environ.get('paypal_secret_key_live')

paypal_client_test_key = os.environ.get('paypal_client_test_key')
paypal_client_live_key = os.environ.get('paypal_client_live_key')

stripe_public_test_key = os.environ.get('stripe_public_test_key')
stripe_secret_test_key = os.environ.get('stripe_secret_test_key')

stripe_public_live_key = os.environ.get('stripe_public_live_key')
stripe_secret_live_key = os.environ.get('stripe_secret_live_key')

stripe.api_key = stripe_secret_test_key

#use below for local testing
#stripe.api_key = "sk_test_51HyqrgLMju5RPM***299bo00yD1lTRNK" 

# ORIGINAL CODE

# stripe_public_key = "pk_test_6RSoSd9tJgB2fN2hGkEDHCXp00MQdrK3Tw"
# stripe_secret_key = "sk_test_fe99fW2owhFEGTACgW3qaykd006gHUwj1j"

# this is a testing key using ptydtesting's stripe account.
# stripe_public_key = "pk_test_51H0sExEDOlfePYdd9TVlnhVDOCmmnmdxAxyAmgW4x7OI0CR7tTrGE2AyrTk8VjftoigEOhv2RTUv5F8yJrfp4jWQ00Q6KGXDHV"
# stripe_secret_key = "sk_test_51H0sExEDOlfePYdd9UQDxfp8yoY7On272hCR9ti12WSNbIGTysaJI8K2W8NhCKqdBOEhiNj4vFOtQu6goliov8vF00cvqfWG6d"

# stripe.api_key = stripe_secret_key
# Allow cross-origin resource sharing
# cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
CORS(app)

# --------------- Mail Variables ------------------
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL")
app.config["MAIL_PASSWORD"] = os.environ.get("PASSWORD")
# app.config['MAIL_USERNAME'] = ''
# app.config['MAIL_PASSWORD'] = ''

# Setting for mydomain.com
app.config["MAIL_SERVER"] = "smtp.mydomain.com"
app.config["MAIL_PORT"] = 465

# Setting for gmail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465

app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True


# Set this to false when deploying to live application
# app.config['DEBUG'] = True
app.config["DEBUG"] = False

app.config["STRIPE_SECRET_KEY"] = os.environ.get("STRIPE_SECRET_KEY")

mail = Mail(app)

# API
api = Api(app)

# convert to UTC time zone when testing in local time zone
utc = pytz.utc


def getToday():
    return datetime.strftime(datetime.now(utc), "%Y-%m-%d")


def getNow():
    return datetime.strftime(datetime.now(utc), "%Y-%m-%d %H:%M:%S")


# Get RDS password from command line argument
def RdsPw():
    if len(sys.argv) == 2:
        return str(sys.argv[1])
    return ""


# RDS PASSWORD
# When deploying to Zappa, set RDS_PW equal to the password as a string
# When pushing to GitHub, set RDS_PW equal to RdsPw()
RDS_PW = "prashant"
# RDS_PW = RdsPw()


# s3 = boto3.client('s3')

# aws s3 bucket where the image is stored
# BUCKET_NAME = os.environ.get('MEAL_IMAGES_BUCKET')
# BUCKET_NAME = 'servingnow'
# allowed extensions for uploading a profile photo file
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


getToday = lambda: datetime.strftime(date.today(), "%Y-%m-%d")
getNow = lambda: datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

# For Push notification
isDebug = False
NOTIFICATION_HUB_KEY = os.environ.get("NOTIFICATION_HUB_KEY")
NOTIFICATION_HUB_NAME = os.environ.get("NOTIFICATION_HUB_NAME")

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

# Connect to MySQL database (API v2)
def connect():
    global RDS_PW
    global RDS_HOST
    global RDS_PORT
    global RDS_USER
    global RDS_DB

    print("Trying to connect to RDS (API v2)...")
    try:
        conn = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            port=RDS_PORT,
            passwd=RDS_PW,
            db=RDS_DB,
            cursorclass=pymysql.cursors.DictCursor,
        )
        print("Successfully connected to RDS. (API v2)")
        return conn
    except:
        print("Could not connect to RDS. (API v2)")
        raise Exception("RDS Connection failed. (API v2)")


# Disconnect from MySQL database (API v2)
def disconnect(conn):
    try:
        conn.close()
        print("Successfully disconnected from MySQL database. (API v2)")
    except:
        print("Could not properly disconnect from MySQL database. (API v2)")
        raise Exception("Failure disconnecting from MySQL database. (API v2)")


# Serialize JSON
def serializeResponse(response):
    try:
        # print("In Serialize JSON")
        for row in response:
            for key in row:
                if type(row[key]) is Decimal:
                    row[key] = float(row[key])
                elif type(row[key]) is date or type(row[key]) is datetime:
                    row[key] = row[key].strftime("%Y-%m-%d")
        # print("In Serialize JSON response", response)
        return response
    except:
        raise Exception("Bad query JSON")


# Execute an SQL command (API v2)
# Set cmd parameter to 'get' or 'post'
# Set conn parameter to connection object
# OPTIONAL: Set skipSerialization to True to skip default JSON response serialization
def execute(sql, cmd, conn, skipSerialization=False):
    response = {}
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            if cmd is "get":
                result = cur.fetchall()
                response["message"] = "Successfully executed SQL query."
                # Return status code of 280 for successful GET request
                response["code"] = 280
                if not skipSerialization:
                    result = serializeResponse(result)
                response["result"] = result
            elif cmd in "post":
                conn.commit()
                response["message"] = "Successfully committed SQL command."
                # Return status code of 281 for successful POST request
                response["code"] = 281
            else:
                response[
                    "message"
                ] = "Request failed. Unknown or ambiguous instruction given for MySQL command."
                # Return status code of 480 for unknown HTTP method
                response["code"] = 480
    except:
        response["message"] = "Request failed, could not execute MySQL command."
        # Return status code of 490 for unsuccessful HTTP request
        response["code"] = 490
    finally:
        response["sql"] = sql
        return response


# Close RDS connection
def closeRdsConn(cur, conn):
    try:
        cur.close()
        conn.close()
        print("Successfully closed RDS connection.")
    except:
        print("Could not close RDS connection.")


# Runs a select query with the SQL query string and pymysql cursor as arguments
# Returns a list of Python tuples
def runSelectQuery(query, cur):
    try:
        cur.execute(query)
        queriedData = cur.fetchall()
        return queriedData
    except:
        raise Exception("Could not run select query and/or return data")





# ===========================================================


def addHeading(outputString, heading):
    outputString += f"<h1>Testing {heading}</h1>"
    return outputString
def addSubHeading(outputString, methodType, optionalMessage=""):
    outputString += f"<h2>Testing {methodType} {optionalMessage}</h2><br>"
    return outputString
def checkMessageInResponseBody(outputString, response_body, successMessage, methodType, testCaseName, returnCode):
     try:
         assert successMessage in response_body["message"]
         outputString += f"<br><p id = \"passed\">{methodType} {testCaseName} PASSED</p><br>"
     except:
         outputString += f"<br><p id = \"failed\">{methodType} {testCaseName} FAILED</p><br>"
         returnCode = 0 
     return outputString, returnCode         
def testGET(returnCode, outputString, getURL, successMessage):
     response = requests.get(getURL)
     response_body = response.json()
     #outputString += "<p>" + str(response_body)  + "</p>" 
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, successMessage, "GET", "Menu", returnCode)     
     maxUIDFromGet = ''    
     result = response_body['result']
     for res in result:
         if maxUIDFromGet < res['menu_uid']:
              maxUIDFromGet = res['menu_uid']
     outputString += "<br>The last JSON is<br>"
     outputString += str(res)
     outputString += "<br>The current max UID is: "
     outputString += str(maxUIDFromGet)
     return outputString, returnCode, response_body, maxUIDFromGet         
def addFooter(outputString, returnCode):
     if returnCode == 0:
         outputString += '<h2 id = "failed">The test case FAILED</h2>'
     else:
         outputString += '<h2 id = "passed">The test case PASSED</h2>'
     outputString = addCssToOutputString(outputString)
     return outputString  
def addCssToOutputString(outputString):
    outputString += "<link href=\"/static/styles.css\" rel=\"stylesheet\" type=\"text/css\">"
    return outputString

# ===========================================================


# -- Queries start here -------------------------------------------------------------------------------

# -- 1.  GET Query
class testMenu(Resource):
    def post(self):


        response = {}
        items = {}
        try:
            conn = connect()
            # data = request.get_json(force=True)
            # print to Received data to Terminal
            # print("Received:", data)

            testCaseName = "Menu"
            outputString = ""
            returnCode = 1
            outputString = addHeading(outputString, testCaseName)
            today = date.today()
            print(today)
            timeNow = getNow()
            print(timeNow)
            # timeNow = time.asctime()
            timeSplit = timeNow.split(" ")[1]
            menu_date = f"{today} {timeSplit}"
            menu_category = "WKLY_SPCL_4"
            menu_type = "Weekly Soup"
            menu_cat = "Soup"
            menu_meal_id = "840-999976"
            default_menu = "TRUE"
            meal_price = "10"
            delivery_days = ["Sunday", "Monday"]
            #Get one of the JSONs from the response and use it for POST, instead of asking the user.
            outputString = addSubHeading(outputString, "GET", "before the test begins")
            outputString, returnCode, response_body, maxMenuUIDFromGet = testGET(returnCode, outputString, "https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/allMenus", "Get AllMenus successful.")     
            outputString = addSubHeading(outputString, "POST", "a new menu")
            inputJSON = {
                        "menu_date":f"{menu_date}",
                        "menu_category":f"{menu_category}", 
                        "menu_type":f"{menu_type}",
                        "meal_cat":f"{menu_cat}",
                        "menu_meal_id":f"{menu_meal_id}",
                        "default_meal":f"{default_menu}",
                        "delivery_days":delivery_days,
                        "meal_price":f"{meal_price}"
                        }
            outputString += '<br>The input JSON is '
            outputString += str(inputJSON)
            response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/menu", json = inputJSON)
            response_body = response.json()
            outputString += "<br>The response JSON of POSTing a new menu is "
            outputString += "<p>"+ str(response_body)+ "</p>"
            try:
                assert "uccess" in response_body["message"]
                outputString += "<br>POST a new menu PASSED<br>"
            except:
                outputString += "<br>POST a new menu FAILED<br>"
                returnCode = 0

            return outputString

        finally:
            disconnect(conn)









class appointments(Resource):
    def get(self):
        response = {}
        items = {}
        try:
            # Connect to the DataBase
            conn = connect()
            # This is the actual query
            query = """ # QUERY 1 
                 SELECT * FROM nitya.customers, nitya.treatments, nitya.appointments WHERE customer_uid = appt_customer_uid AND treatment_uid = appt_treatment_uid; """
            # The query is executed here
            items = execute(query, "get", conn)
            # The return message and result from query execution
            response["message"] = "successful"
            response["result"] = items["result"]
            # Returns code and response
            return response, 200
        except:
            raise BadRequest("Request failed, please try again later.")
        finally:
            disconnect(conn)

        # ENDPOINT THAT WORKS
        # http://localhost:4000/api/v2/appointments


# -- DEFINE APIS -------------------------------------------------------------------------------


# Define API routes

api.add_resource(testMenu, "/api/v2/testMenu")
api.add_resource(appointments, "/api/v2/appointments")



# Run on below IP address and port
# Make sure port number is unused (i.e. don't use numbers 0-1023)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4000)
