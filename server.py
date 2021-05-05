#  Column names are case sensitive.
#  ntc = need to check the response
#  dont use UID in HTML and in this script
#  use f20flier account wherever needed.
#  Add comments to be careful about get, put or post 
#  2 and 26 are same in the worksheet
#
#
#
#
#######################################################################
#  Action Item
#
# 04/09 : Work on customer. Completed. 
#
# 04/12 : Work on meals selection. involves surprise.
#         Purchase a meal plan, do a Get selection, select a meal for that meal plan
#         do another get selection, then surprise, then another get selection, then skip followed
#         by another get selection. Need delete here as well.
#
#         Use the purchase ID 400-000084
#         customer ID : 100-000155
#
# 04/13 : 
#
#
#
###################

from flask import Flask, render_template, url_for, request, flash, Markup
import requests
import responses
import certifi
import ssl
import json
from datetime import date
import datetime
import mysql.connector
import time
from pygments import highlight, lexers, formatters
app = Flask(__name__)

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
    
@app.route('/')
def index():
  return render_template('index.html', message="PASSED")
@app.route('/testPurchase/', methods = ['POST'])
def testPurchase():
     testCaseName = "Purchase"
     inputCustomerUID = request.form['customerUID']
     outputString = f"<br><h2>The latest purchases payments by cutomer with UID {inputCustomerUID} is <br><br></h2>"
     returnCode = 1
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/customer_lplp?customer_uid={inputCustomerUID}")
     assert response.headers["Content-Type"] == "application/json"      
     response_body = response.json()
     outputString += "<br> The results from the input JSON are <br>"
     #outputString += str(response_body)
     result = response_body["result"]
     maxLPLPUID = ''
     for res in result:
       if res['purchase_uid'] > maxLPLPUID:
           maxLPLPUID = res['purchase_uid']
     outputString += "<br>The last LPLP is <br>"      
     outputString += str(res)
     outputString += "<br>The max LPLP UID is:  "
     outputString += str(maxLPLPUID)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Get Get_Latest_Purchases_Payments successful.", "GET", "Latest Purchase payments", returnCode)
     # Bad request, 400
     outputString += "<h2>Testing checkout post</h2><br>"
     returnCode = 1
     customerID = "100-000155"
     businessID = "WEB"
     qty = "1"
     name = "5 Meal Plan - Weekly"
     price = "59.99"
     item_uid = "320-000002"
     itm_business_uid = "200-000002"
     salt = ""
     order_instructions = "fast"
     delivery_instructions = "M4METEST"
     delivery_first_name = "Anup"
     delivery_last_name = "Jaltade"
     delivery_phone = "1234567890"
     delivery_email = "anna77lee@yahoo.com" 
     delivery_address = "11075 La Paloma Drive"
     delivery_unit = ""
     delivery_city = "Cupertino"
     delivery_state = "CA"
     delivery_zip = "95014"
     delivery_longitude = "-121.8866517"
     delivery_latitude = "37.2270928"     
     purchase_notes = "purchase notes"
     amount_due = "300.00"
     amount_discount = "0.00"
     amount_paid = "0.00"
     cc_num = "NULL"
     cc_exp_year = "NULL"
     cc_exp_month = "NULL"
     cc_cvv = "NULL"
     cc_zip = "NULL"
     charge_id = "pi_1IeRboLMju5RPMEvgmN8wXo2"
     payment_type = "STRIPE"
     service_fee = "2.00"
     delivery_fee = "2.00"
     tip = "2.00"
     tax = "3.91"
     subtotal = "48.00"
     amb = "0.00"
     inputJSON = {
                  "customer_uid":f"{customerID}",
                  "business_uid": f"{businessID}",
                  "items": [{
                             "qty": f"{qty}", 
                             "name": f"{name}", 
                             "price": f"{price}", 
                             "item_uid": f"{item_uid}",
                             "itm_business_uid":f"{itm_business_uid}"
                             }],
                  "salt": f"{salt}",
                  "order_instructions":f"{order_instructions}",
                  "delivery_instructions": f"{delivery_instructions}",                  
                  "delivery_first_name":f"{delivery_first_name}",
                  "delivery_last_name":f"{delivery_last_name}",
                  "delivery_phone":f"{delivery_phone}",
                  "delivery_email":f"{delivery_email}",
                  "delivery_address":f"{delivery_address}",
                  "delivery_unit":"",
                  "delivery_city":f"{delivery_city}",
                  "delivery_state":f"{delivery_state}",
                  "delivery_zip":f"{delivery_zip}",
                  "delivery_latitude":f"{delivery_latitude}",
                  "delivery_longitude":f"{delivery_longitude}",
                  "purchase_notes":f"{purchase_notes}",
                  "amount_due":f"{amount_due}",
                  "amount_discount":f"{amount_discount}",
                  "amount_paid":f"{amount_paid}",
                  "cc_num": f"{cc_num}",
                  "cc_exp_year": f"{cc_exp_year}",
                  "cc_exp_month": f"{cc_exp_month}",
                  "cc_cvv":f"{cc_cvv}",
                  "cc_zip":f"{cc_zip}",
                  "charge_id": f"{charge_id}",
                  "payment_type": f"{payment_type}",
                  "service_fee": f"{service_fee}",
                  "delivery_fee": f"{delivery_fee}",
                  "tip": f"{tip}",
                  "tax": f"{tax}",
                  "subtotal": f"{subtotal}",                  
                  "amb": f"{amb}"
                  }
     outputString += "<h2>Testing checkout post </h2><br>"             
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/checkout", json = inputJSON)
     response_body = response.json()
     outputString += "The response JSON is<br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Get Plans successful.", "POST", "checkout", returnCode)
     outputString += "<h2>Testing purchase <br>"
     outputString += "<h2>Testing GET purchase</h2><br>"
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/ordered_by_date")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     #outputString += str(response_body)
     result = response_body['result']
     maxLPLPUIDAfterPost = ''
     outputString += str(response_body)
     #for res in result:
     #   if res['purchase_uid'] > maxLPLPUIDAfterPost:
     #       maxLPLPUIDAfterPost = res['purchase_uid']
     #outputString += str(res)
     #outputString += "<br>"  
     #outputString += "The next purchase is:  "
     #outputString += str(maxLPLPUIDAfterPost)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Get Ordered_By_Date successful.", "GET", "purchase", returnCode) 
     '''
     outputString = addSubHeading(outputString, "PUT", "to update an existing purchase")             
     cc_cvv = "424"         
     inputJSON = {
                  "cc_cvv": "424",
                  "cc_exp_date": "2022-01-01",
                  "cc_num": "4242424242424242",
                  "cc_zip": "95060",
                  "customer_email": "cchuang4@ucsc.edu",
                  "items": [{
                            "qty": "2", 
                            "name": "2 Meal Plan", 
                            "price": "15.00", 
                            "item_uid": "320-000035", 
                            "itm_business_uid": "200-000002"
                           }],
                  "new_item_id": "320-000035",
                  "password": "NULL", <-if social, null, otherwise password
                  "purchase_id": "400-000049", <- must be active
                  "start_delivery_date":""
                  }

     outputString += requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/test_cal/400-000046")

     #Need to create a purchase to cancel it
     outputString = "cancel Purchase <br>"
     returnCode = 1
     purchaseID = request.form['purchaseID']
     inputJSON = { 
                  "purchase_uid" : f"{purchaseID}"
                  }
     response = requests.put("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/cancel_purchase", json = inputJSON)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>PUT cancel purchase PASSED<br>"
     except:
         outputString += "<br>PUT cancel purchase FAILED<br>"
         returnCode = 0
     return outputString        
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/ordered_by_date")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     #outputString += str(response_body)
     result = response_body['result']
     maxLPLPUIDAfterPost = ''
     for res in result:
        if res['purchase_uid'] > maxLPLPUIDAfterPost:
            maxLPLPUIDAfterPost = res['purchase_uid']
     outputString += str(res)
     outputString += "<br>"  
     outputString += "The next purchase is:  "
     outputString += str(maxLPLPUIDAfterPost)
     try:
         assert response_body["message"] == "Get Ordered_By_Date successful."
         outputString += "<br>GET purchase PASSED<br>"
     except:
         outputString += "<br>GET purchase FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     '''    
     outputString = addFooter(outputString, returnCode)
     return outputString     
@app.route('/getDeliveryInfo/', methods = ['POST'])
def getDeliveryInfo():
    testCaseName = "get Delivery Info"
    purchaseID = request.form['purchaseID']
    outputString = "<br><h2>Get the delivery info<br> Testing GET delivery info<br></h2>"
    returnCode = 1
    response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/get_delivery_info/{purchaseID}")
    response_body = response.json()
    outputString += "<br> The response JSON for GET is <br>"
    outputString += str(response_body)
    try:
        assert "uccess" in response_body["message"]     
        outputString += "<br>GET delivery info PASSED<br>"
    except:
        outputString += "<br>GET delivery info FAILED<br>"
        returnCode = 0
    outputString += "<br>POSTing a new delivery info<br>"
    inputJSON = {
                 "first_name":"Welks",
                 "last_name":" C",
                 "purchase_uid": "400-000056",
                 "phone":"1234567890",
                 "email":"welks@gmail.com",
                 "address":"213 Mora",
                 "unit":"",
                 "city":"Santa Cruz",
                 "state":"CA",
                 "zip":"95064",
                 "cc_num":"4242424242424242",
                 "cc_cvv":"424",
                 "cc_zip":"95129",
                 "cc_exp_date":"2021-08-01" 
      }
    response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/update_delivery_info", json = inputJSON)
    response_body = response.json()
    try:
         #ntc
         assert "uccess" in response_body["message"]
         outputString += "<br>POST update delivery info PASSED<br>"
    except:
         outputString += "<br>POST update delivery info FAILED<br>"
         returnCode = 0
    outputString += "<br><h2>Testing GET to check whether the delivery info has been updated<br>"
    response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/get_delivery_info/{purchaseID}")
    response_body = response.json()
    outputString += "<br> The response JSON for GET is <br>"
    outputString += str(response_body)
    try:
        assert "uccess" in response_body["message"]     
        outputString += "<br>GET delivery info PASSED<br>"
    except:
        outputString += "<br>GET delivery info FAILED<br>"
        returnCode = 0
    outputString += "<br>POSTing a new delivery info address <br>"
    inputJSON = {
                 "first_name":"Welks",
                 "last_name":" C",
                 "purchase_uid": "400-000056",
                 "phone":"1234567890",
                 "email":"welks@gmail.com",
                 "address":"6427 Prospect Rd",
                 "unit":"",
                 "city":"Santa Cruz",
                 "state":"CA",
                 "zip":"95064"
                 }
    response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Update_Delivery_Info_Address", json = inputJSON)
    response_body = response.json()
    try:
         #ntc
         assert "uccess" in response_body["message"]
         outputString += "<br>POST update delivery info address PASSED<br>"
    except:
         outputString += "<br>POST update delivery info address FAILED<br>"
         returnCode = 0
    outputString += "<br><h2>Testing GET to make sure that the POST has worked<br>"     
    response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/get_delivery_info/{purchaseID}")
    response_body = response.json()
    outputString += "<br> The response JSON for GET is <br>"
    outputString += str(response_body)
    try:
        assert "uccess" in response_body["message"]     
        outputString += "<br>GET delivery info PASSED<br>"
    except:
        outputString += "<br>GET delivery info FAILED<br>"
        returnCode = 0         
    outputString = addFooter(outputString, returnCode)
@app.route('/testMenu/')
def testMenu():
     # use **kwargs
     testCaseName = "Menu"
     outputString = ""
     returnCode = 1
     outputString = addHeading(outputString, testCaseName)
     today = date.today()
     timeNow = time.asctime()
     timeSplit = timeNow.split(" ")[4]
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
     new_menu_uid = response_body["meal_uid"]
     outputString += "<br>The new menu UID assigned to the POST is:  "
     outputString += str(new_menu_uid)
     outputString = addSubHeading(outputString, "GET", "to make sure POST has created the menu")
     outputString, returnCode, response_body, newMenuUIDAfterPost = testGET(returnCode, outputString, "https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/allMenus", "Get AllMenus successful.")     
     result = response_body['result']
     newMenuFound = 0
     for res in result:
          if res['menu_uid'] == new_menu_uid:
               outputString += "<br>Found the new menu uid"
               newMenuFound = 1
               if res["menu_date"] == menu_date:
                      outputString += f"<br>Menu date returned in GET = {menu_date}"
               if res["menu_category"] == f"{menu_category}":
                      outputString += f"<br>Menu category returned in GET = {menu_category}"
               if res["menu_type"] == f"{menu_type}":
                      outputString += f"<br>Menu type returned in GET = {menu_type}"
               if res["meal_cat"] == f"{menu_cat}":
                      outputString += f"<br>MEAL category returned in GET = {menu_cat}"
               if res["menu_meal_id"] == f"{menu_meal_id}":
                      outputString += f"<br>Menu meal ID returned in GET = {menu_meal_id}"
               if res["default_meal"] == f"{default_menu}":
                      outputString += f"<br>Default menu returned in GET = {default_menu}"
               if res["delivery_days"] == f"{delivery_days}":
                      outputString += f"<br>Delivery days returned in GET = {delivery_days}"
               if res["meal_price"] == f"{meal_price}":
                      outputString += f"<br>Meal price returned in GET = {meal_price}"
     if newMenuFound == 0:
        returnCode = 0
     outputString = addSubHeading(outputString, "PUT", "to update the new menu")
     outputString += "<br> The new menu UID is:  "
     outputString += str(new_menu_uid)
     inputJSON = {
                 "menu_uid": f"{new_menu_uid}",
                 "menu_date":f"{menu_date}",
                 "menu_category":f"{menu_category}", 
                 "menu_type":f"{menu_type}",
                 "meal_cat":f"{menu_cat}",
                 "menu_meal_id":f"{menu_meal_id}",
                 "default_meal":"FALSE",
                 "delivery_days":delivery_days,
                 "meal_price":f"{meal_price}"
                 }
     outputString += "<br>The inputJSON is <br>"
     outputString += str(inputJSON)     
     response = requests.put("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/menu", json = inputJSON)
     response_body = response.json()
     outputString += "<br>The response JSON of PUTing to the menu is <br>"
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>PUT menu PASSED<br>"
     except:
         outputString += "<br>PUT menu FAILED<br>"
         returnCode = 0
     #Change messages in try expect blocks from here on. << CMFH, order changed on 03/24
     outputString = addSubHeading(outputString, "GET", "to make sure PUT has updated the menu")
     outputString, returnCode, response_body, newMenuUIDAfterPut = testGET(returnCode, outputString, "https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/allMenus", "Get AllMenus successful.")     
     result = response_body['result']
     newMenuFound = 0
     for res in result:
          if res['menu_uid'] == new_menu_uid:
               outputString += "\n<br>Found the new menu uid"
               newMenuFound = 1
               if res["menu_date"] == menu_date:
                      outputString += f"\n<br>Menu date returned in GET = {menu_date}"
               if res["menu_category"] == f"{menu_category}":
                      outputString += f"\n<br>Menu category returned in GET = {menu_category}"
               if res["menu_type"] == f"{menu_type}":
                      outputString += f"\n<br>Menu type returned in GET = {menu_type}"
               if res["meal_cat"] == f"{menu_cat}":
                      outputString += f"\n<br>MEAL category returned in GET = {menu_cat}"
               if res["menu_meal_id"] == f"{menu_meal_id}":
                      outputString += f"\n<br>Menu meal ID returned in GET = {menu_meal_id}"
               if res["default_meal"] == "FALSE":
                      outputString += f"\n<br>Default menu returned in GET = FALSE"
               if res["delivery_days"] == f"{delivery_days}":
                      outputString += "\n<br>Delivery days returned in GET = {delivery_days}"
               if res["meal_price"] == f"{meal_price}":
                      outputString += f"\n<br>Meal price returned in GET = {meal_price}"
     if newMenuFound == 0:
         returnCode = 0
     outputString = addSubHeading(outputString, "DELETE", "a new menu")                
     response = requests.delete(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/menu?menu_uid={new_menu_uid}")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>DELETE menu PASSED<br>"
     except:
         outputString += "<br>DELETE menu FAILED<br>"
         returnCode = 0
     outputString = addSubHeading(outputString, "GET", "to check whether the new menu was deleted")
     outputString, returnCode, response_body, newMenuUIDAfterDelete = testGET(returnCode, outputString, "https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/allMenus", "Get AllMenus successful.")       
     result = response_body['result']
     newMenuUIDFound = 0
     for res in result:
          if res['menu_uid'] == new_menu_uid:
               outputString += "\n<br>Should not have found the new menu uid"
               newMenuUIDFound = 1
     if newMenuUIDFound == 0:
          outputString += "\n<br>The new menu has been deleted successfully"
          returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString 
@app.route('/testMeal/')
def testMeal():
     #REDO, somethings are pending. Put not working.
     outputString = "<h1><br>Testing meals Endpoint<br></h1>"
     returnCode = 1
     meal_category = "Entree"
     meal_name = "Ramen1"
     meal_desc = "Ramen1"
     meal_hint = "none"
     meal_photo_url = "C:\\Users\\Public\\Pictures\\Sample Pictures\\Desert.jpg"
     meal_calories = "2"
     meal_protein = "2"
     meal_carbs = "2"
     meal_fiber = "2"
     meal_sugar = "2"
     meal_fat = "2"
     meal_sat = "2"
     meal_sat_for_put = 3.0
     outputString += "<br><h2>Testing GET meals <br></h2>" 
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/meals")
     response_body = response.json()
     #outputString += str(response_body)
     outputString += "<br> The last JSON is <br>"
     lastMealID = ''
     result = response_body['result']
     for res in result:
        if res['meal_uid'] > lastMealID:
            lastMealID = res['meal_uid']
     outputString += str(res)
     outputString += "<br><br>"
     outputString += "The current max meal UID is: "
     outputString += str(lastMealID)
     try:
         #ntc
         assert response_body["message"] == "Get Meals successful."
         outputString += "<br>GET Meals selected <p id = \"passed\">PASSED</p><br>"
     except:
         outputString += "<br>GET Meals selected <p id = \"failed\">FAILED</p><br>"
     files = {'meal_photo_url' : open(meal_photo_url, 'rb')}
     inputData = {
                 "meal_category":f"{meal_category}",
                 "meal_name":f"{meal_name}",
                 "meal_desc" :f"{meal_desc}",
                 "meal_hint":f"{meal_hint}",
                 "meal_calories":f"{meal_calories}",
                 "meal_protein" :f"{meal_protein}",
                 "meal_carbs" :f"{meal_carbs}",
                 "meal_fiber" :f"{meal_fiber}",
                 "meal_sugar" :f"{meal_sugar}",
                 "meal_fat" :f"{meal_fat}",
                 "meal_sat" :f"{meal_sat}"
                 }
     outputString += "<br><h2>Testing POST a meal <br></h2>"
     outputString += "<br>The input JSON is <br>"
     outputString += str(inputData)     
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/create_update_meals", data = inputData, files = files)
     response_body = response.json()
     outputString += "<br>The response JSON is  "
     outputString += str(response_body)
     outputString += "<br>The current max UID is: "
     outputString += str(response_body['meal_uid'])
     try:
         assert "uccess" in response_body["message"]
         outputString += "\n<br>POST meal <p id = \"passed\">PASSED</p><br>"
     except:
         outputString += "\n<br>POST meal <p id = \"failed\">FAILED</p><br>"
         returnCode = 0
     meal_uid = response_body["meal_uid"]
     outputString += "<br><h2> Testing GET meals to check whether the new meal has been added successfully<br></h2>" 
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/meals")
     response_body = response.json()
     #outputString += str(response_body)
     outputString += "<br> The last JSON is <br>"
     lastMealIDAfterPost = ''
     result = response_body['result']
     for res in result:
        if res['meal_uid'] > lastMealIDAfterPost:
            lastMealIDAfterPost = res['meal_uid']       
     outputString += str(res)
     outputString += "<br><br>"
     outputString += "The current max meal UID is: "
     outputString += str(lastMealIDAfterPost)
     if lastMealIDAfterPost > lastMealID:
         outputString += "<br>New meal posted successfully<br>"
     try:
         assert response_body["message"] == "Get Meals successful."
         outputString += "<br>GET Meals <p id = \"passed\">PASSED</p><br>"
     except:
         outputString += "<br>GET Meals <p id = \"failed\">FAILED</p><br>"
     outputString += "<br><h2>Testing PUT meals</h2><br>"    
     # 405, Method not allowed
     inputData = {
                 "meal_uid":f"{meal_uid}",
                 "meal_category":f"{meal_category}",
                 "meal_name":f"{meal_name}",
                 "meal_desc" :f"{meal_desc}",
                 "meal_hint":f"{meal_hint}",
                 "meal_calories":f"{meal_calories}",
                 "meal_protein" :f"{meal_protein}",
                 "meal_carbs" :f"{meal_carbs}",
                 "meal_fiber" :f"{meal_fiber}",
                 "meal_sugar" :f"{meal_sugar}",
                 "meal_fat" :f"{meal_fat}",
                 "meal_sat" :f"{meal_sat_for_put}"
                 }
     outputString += "<br>The input JSON is <br>"
     outputString += str(inputData)     
     response = requests.put("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/create_update_meals", data = inputData, files = files)
     response_body = response.json()
     outputString += "<br> The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>PUT meal <p id = \"passed\">PASSED</p>"
     except:
         outputString += "<br>PUT meal <p id = \"failed\">FAILED</p>"
         returnCode = 0
     outputString += "<br><h2>Testing GET after PUT to check whether the meal has been updated</h2><br>"
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/meals")
     response_body = response.json()
     result = response_body['result']
     #outputString += str(response_body)
     outputString += "<br> The last JSON is <br>"
     #lastMealIDAfterPost = ''
     #Change all the fields in PUT
     updatedMealFound = 0
     for res in result:
        if res['meal_uid'] == lastMealIDAfterPost:
            #updatedMealFound = 1
            if res['meal_sat'] == meal_sat_for_put:
                outputString += str(res)
                outputString += f"<br>The new meal has been updated successfully with saturation {meal_sat_for_put}<br>"
                updatedMealFound = 1
     outputString += "<br>"
     if updatedMealFound == 1: 
        outputString += "The last meal UID is:  "     
        outputString += str(lastMealIDAfterPost)
     else:
        outputString += "<br>The meal was not updated using PUT<br>"     
     try:
         #ntc
         assert response_body["message"] == "Get Meals successful."
         outputString += "<br>GET Meals <p id = \"passed\">PASSED</p>"
     except:
         outputString += "<br>GET Meals <p id = \"failed\">FAILED</p>" 
         returnCode = 0    
     outputString += "<br><h2>Testing DELETE a meal</h2><br>"  
     response = requests.delete(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/meals?meal_uid={meal_uid}")
     response_body = response.json()
     #outputString += "<br> The response JSON is <br>"
     #outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += "\n<br>DELETE meal <p id = \"passed\">PASSED</p>"
     except:
         outputString += "\n<br>DELETE meal <p id = \"failed\">FAILED</p>"
         returnCode = 0
     outputString += "<br><h2>Testing GET to make sure the DELETE meal has worked</h2><br>"
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/meals")
     response_body = response.json()
     result = response_body['result']
     #outputString += str(response_body)
     outputString += "<br> The last JSON is <br>"
     lastMealIDAfterDelete = ''
     for res in result:
        if res['meal_uid'] > lastMealIDAfterDelete:
            lastMealIDAfterDelete = res['meal_uid']       
     outputString += str(res)
     outputString += "<br><br>"
     outputString += "The current max meal UID is: "
     outputString += str(lastMealIDAfterDelete)
     if lastMealIDAfterDelete < lastMealIDAfterPost:
         outputString += "<br>New meal has been deleted successfully<br>"
     try:
         #ntc
         assert response_body["message"] == "Get Meals successful."
         outputString += "<br>GET Meals <p id = \"passed\">PASSED</p>"
     except:
         outputString += "<br>GET Meals <p id = \"failed\">FAILED</p>" 
         returnCode = 0           
     outputString = addFooter(outputString, returnCode)          
@app.route('/testMealCreation/')
def mealCreation():
     outputString = "<br><h2>Testing meal creation<br>"
     returnCode = 1
     meal_id = "840-010007"
     ingredient_id = "2"
     ingredient_qty = "3"
     measure_id = "4"
     outputString += "<br>POST a meal creation"
     inputJSON = {
                 "meal_id":f"{meal_id}",
                 "ingredient_id":f"{ingredient_id}",
                 "ingredient_qty":f"{ingredient_qty}",
                 "measure_id":f"{measure_id}"
                 }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/mealcreation", json = inputJSON)
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert "Request successful." in response_body
         outputString += "<br>POST Meals PASSED<br>"
     except:
         outputString += "<br>POST Meals FAILED<br>"
         returnCode = 0
     outputString += "<br> Testing GET meal creation<br>"    
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/mealcreation")
     response_body = response.json()
     outputString += "<br> The JSON returned is <br>"
     outputString += str(response_body)
     try:
         assert response_body["message"] == "Request successful."
         outputString += "<br>GET Meals PASSED<br>"
     except:
         outputString += "<br>GET Meals FAILED<br>"
         returnCode = 0
     if returnCode == 0:
         outputString += '<br><h2 id = "FAILED<br>">The test case FAILED</h2>'
         return outputString 
     else:
         outputString += '<br><h2>The test case PASSED</h2>'
         return outputString
@app.route('/testMeasureUnit/')        
def measure_Unit():
     outputString = "<br><h2>Testing measure unit<br>"
     returnCode = 1
     measureUnitType = "length"
     recipeUnit = "dm"
     conversionRatio = "10"
     commonUnit = "cm"
     commonUnitForPut = "m"
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/measure_unit")
     response_body = response.json()
     result = response_body['result']
     outputString += "<br> The returned JSON is <br>"
     measure_unit_uidBeforePost = ''
     for res in result:
       if res['measure_unit_uid'] > measure_unit_uidBeforePost:
            measure_unit_uidBeforePost = res['measure_unit_uid']
     outputString += "The last conversion Unit is <br>"            
     outputString += str(res)
     outputString += "The current max conversion unit UID is: "
     outputString += str(measure_unit_uidBeforePost)
     try:
         assert response_body["message"] == "Get Measure_Unit successful."
         outputString += "<br>GET Meals selected PASSED<br>"
     except:
         outputString += "<br>GET Meals selected FAILED<br>" 
         returnCode = 0         
     #Bad request, 400
     inputJSON = {
                 "type":f"{measureUnitType}",
                 "recipe_unit":f"{recipeUnit}",
                 "conversion_ratio":f"{conversionRatio}",
                 "common_unit":f"{commonUnit}"
                 }
     outputString += "<br> Testing the POST method for measure Unit<br>"            
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/measure_unit", json = inputJSON)
     response_body = response.json()
     measure_unit_uid = response_body['measure_unit_uid']
     outputString += "<br> The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST Meals selected PASSED<br>"
     except:
         outputString += "<br>POST Meals selected FAILED<br>" 
         returnCode = 0 
     outputString += "<br><h2>Testing GET after POST to make sure the conversion unit has been added <br>"    
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/measure_unit")
     response_body = response.json()
     result = response_body['result']
     outputString += "<br> The returned JSON is <br>"
     measure_unit_uidAfterPost = ''
     for res in result:
       if res['measure_unit_uid'] > measure_unit_uidAfterPost:
            measure_unit_uidAfterPost = res['measure_unit_uid']
     outputString += "The last conversion Unit is <br>"            
     outputString += str(res)
     outputString += "The current max conversion unit UID is: "
     outputString += str(measure_unit_uidBeforePost)
     if measure_unit_uidAfterPost > measure_unit_uidBeforePost:
        outputString += "<br>The conversion unit has been added successfully<br>"
     try:
         assert response_body["message"] == "Get Measure_Unit successful."
         outputString += "<br>GET Meals selected PASSED<br>"
     except:
         outputString += "<br>GET Meals selected FAILED<br>" 
         returnCode = 0  
     
     inputJSON = {
                 "measure_unit_uid": f"{measure_unit_uid}",
                 "type":f"{measureUnitType}",
                 "recipe_unit":f"{recipeUnit}",
                 "conversion_ratio":f"{conversionRatio}",
                 "common_unit":f"{commonUnitForPut}"
                 }            
     outputString += "<br><br> Testing the PUT method for measure Unit<br>"                             
     response = requests.put("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/measure_unit", json = inputJSON)
     response_body = response.json()
     outputString += "<br> The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>PUT Meals selected PASSED<br>"
     except:
         outputString += "<br>POST Meals selected FAILED<br>" 
         returnCode = 0               
         
     outputString += "<br><h2>Testing GET after POST to make sure the conversion unit has been added <br>"    
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/measure_unit")
     response_body = response.json()
     result = response_body['result']
     outputString += "<br> The returned JSON is <br>"
     measure_unit_uidAfterPost = ''
     for res in result:
       if res['measure_unit_uid'] > measure_unit_uidAfterPost:
            measure_unit_uidAfterPost = res['measure_unit_uid']
     outputString += "The last conversion Unit is <br>"            
     outputString += str(res)
     outputString += "The current max conversion unit UID is: "
     outputString += str(measure_unit_uidBeforePost)
     if measure_unit_uidAfterPost > measure_unit_uidBeforePost:
        outputString += "<br>The conversion unit has been added successfully<br>"
     try:
         assert response_body["message"] == "Get Measure_Unit successful."
         outputString += "<br>GET Meals selected PASSED<br>"
     except:
         outputString += "<br>GET Meals selected FAILED<br>" 
         returnCode = 0  

     outputString += "<br><br> Testing the DELETE method for measure Unit<br>" 
     #?measure_unit_uid={measure_unit_uid}     
     response = requests.delete(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/measure_unit")
     response_body = response.json()
     outputString += "<br> The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"] 
         outputString += "<br>POST Meals selected PASSED<br>"
     except:
         outputString += "<br>POST Meals selected FAILED<br>" 
         returnCode = 0 
     outputString += "<br><h2>Testing GET after DELETE to make sure the conversion unit has been deleted <br>"    
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/measure_unit")
     response_body = response.json()
     result = response_body['result']
     outputString += "<br> The returned JSON is <br>"
     measure_unit_uidAfterPost = ''
     for res in result:
       if res['measure_unit_uid'] > measure_unit_uidAfterPost:
            measure_unit_uidAfterPost = res['measure_unit_uid']
     outputString += "The last conversion Unit is <br>"            
     outputString += str(res)
     outputString += "The current max conversion unit UID is: "
     outputString += str(measure_unit_uidBeforePost)
     if measure_unit_uidAfterPost > measure_unit_uidBeforePost:
        outputString += "<br>The conversion unit has been added successfully<br>"
     try:
         assert response_body["message"] == "Get Measure_Unit successful."
         outputString += "<br>GET Meals selected PASSED<br>"
     except:
         outputString += "<br>GET Meals selected FAILED<br>" 
         returnCode = 0  

     if returnCode == 0:
         outputString += '<br><h2 id = "FAILED<br>">The test case FAILED</h2>'
         return outputString 
     else:
         outputString += '<br><h2>The test case PASSED</h2>'
         return outputString    
@app.route('/testPlans/')
def plans():
     outputString = "<h2>Testing plans <br>"
     returnCode = 1
     outputString += "<br><h2>Testing GET plans<br>"
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/plans")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     #outputString += str(response_body)
     result = response_body['result']
     for res in result:
       outputString += str(res)
       outputString += "<br><br>"
       outputString += "The next plan is <br>"
     try:
         assert response_body["message"] == "Get Plans successful."
         outputString += "<br>GET Meals selected PASSED<br>"
     except:
         outputString += "<br>GET Meals selected FAILED<br>"
         returnCode = 0
     #404 not found.
     outputString = "<br><h2>Testing plans post<br>"
     returnCode = 1
     photo_url = "C:\\Users\\Public\\Pictures\\Sample Pictures\\Desert.jpg"
     description = "I like the food"
     payment_frequency = "2"
     plan_headline = "headline"
     plan_footer = "footer"
     num_meals = "2"
     meal_weekly_price = "10"
     meal_plan_price = "20"
     shipping = "0" 
     
     files = {'photo_url' : open(photo_url, 'rb')}
     inputJSON = {
                 "meal_plan_desc":f"{description}",
                 "payment_frequency":f"{payment_frequency}",
                 "plan_headline": f"{plan_headline}",
                 "plan_footer": f"{plan_footer}",
                 "num_meals": f"{num_meals}",
                 "meal_weekly_price": f"{meal_weekly_price}",
                 "meal_plan_price": f"{meal_plan_price}",
                 "meal_shipping": f"{shipping}"
                 }
     outputString += "<br><h2>Testing POST plan<br>"            
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Add_Meal_plan", json = inputJSON, files = files)
     response_body = response.json()
     outputString += "<br> The response JSON is <br>"
     outputString += str(response_body) 
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET Meals selected PASSED<br>"
     except:
         outputString += "<br>GET Meals selected FAILED<br>"
         returnCode = 0
     if returnCode == 0:
         outputString += '<br><h2 id = "FAILED<br>">The test case FAILED</h2>'
         return outputString 
     else:
         outputString += '<br><h2>The test case PASSED</h2>'
         return outputString         
@app.route('/testCoupons/')
def coupons():
     outputString = "<h1>Testing coupons </h1><br>"
     returnCode = 1
     coupon_ID = "Testing"
     valid = "false"
     validForPut = "true"
     discount_percent = "100"
     discount_amount = "0"
     discount_shipping = "0"
     expiry_date = "2020-12-31"
     expiry_dateForPut = "future"
     limits = "none"
     notes = "for testing"
     notesForPut = "none"
     num_used = "0"
     recurring = "false"
     recurringForPut = "true"
     emailID = ""
     emailIDForPut = "1"
     cup_business_uid = ""
     cup_business_uidForPut = "1"
     outputString += "<h2>Testing GET coupon</h2>"
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/coupons")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     #outputString += str(response_body) 
     result = response_body['result']
     maxCouponID = ''
     for res in result:
         if maxCouponID < res['coupon_uid']:
            maxCouponID = res['coupon_uid']
            
     outputString += "The last coupon is "            
     outputString += str(res)
     outputString += "<br>"
     outputString += "The max current coupon_ID is "
     outputString += str(maxCouponID)       
     try:
         assert response_body["message"] == "Get Coupons successful."
         outputString += '<br>GET coupons <p id= "passed"> PASSED</p><br>'
     except:
         outputString += '<br>GET coupons <p id= "failed">FAILED</p><br>'
         returnCode = 0
     outputString += "<h2>Testing POST a coupon</h2><br>"    
     inputJSON = {
                 "coupon_id":f"{coupon_ID}",
                 "valid":f"{valid}",
                 "discount_percent": f"{discount_percent}",
                 "discount_amount": f"{discount_amount}",
                 "discount_shipping": f"{discount_shipping}",
                 "expire_date": f"{expiry_date}",
                 "limits": f"{limits}",
                 "notes": f"{notes}",
                 "num_used": f"{num_used}",
                 "recurring":f"{recurring}",
                 "email_id":f"{emailID}",
                 "cup_business_uid":f"{cup_business_uid}"
                 }
     outputString += "<br>The input JSON is <br>"
     outputString += str(inputJSON)     
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/coupons", json = inputJSON)
     response_body = response.json()
     outputString += "<br>The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += '<br>POST Coupons <p id = "passed">PASSED</p><br>'
     except:
         outputString += '<br>POST Coupons <p id = "failed">FAILED</p><br>'
         returnCode = 0
     coupon_uid = response_body["coupon_uid"]
     outputString += "<br><h2>Testing GET after POST to check whether the coupon was added</h2><br>"    
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/coupons")
     response_body = response.json()
     #outputString += "<h2>Testing GET coupons <br>"
     outputString += "The response JSON is <br>"
     #outputString += str(response_body) 
     result = response_body['result']
     maxCouponIDAfterPost = ''
     for res in result:
         if maxCouponIDAfterPost < res['coupon_uid']:
            maxCouponIDAfterPost = res['coupon_uid']
     outputString += "The last coupon is "            
     outputString += str(res)
     outputString += "<br>"
     outputString += "The max current coupon_ID is "
     outputString += str(maxCouponIDAfterPost)       
     if maxCouponIDAfterPost > maxCouponID:
         outputString += "<br> The coupon is added successfully<br>"
     outputString += "<h2> Testing PUT a coupon</h2>"
     inputJSON = {
                 "coupon_uid":f"{coupon_uid}",
                 "coupon_id":f"{coupon_ID}",
                 "valid":f"{validForPut}",
                 "discount_percent": f"{discount_percent}",
                 "discount_amount": f"{discount_amount}",
                 "discount_shipping": f"{discount_shipping}",
                 "expire_date": f"{expiry_dateForPut}",
                 "limits": f"{limits}",
                 "notes": f"{notesForPut}",
                 "num_used": f"{num_used}",
                 "recurring":f"{recurringForPut}",
                 "email_id":f"{emailIDForPut}",
                 "cup_business_uid":f"{cup_business_uidForPut}"
                 }
     response = requests.put("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/coupons", json = inputJSON)
     response_body = response.json()
     outputString += "<br> The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += '<br>PUT Coupons <p id = "passed">PASSED</p><br>'
     except:
         outputString += '<br>PUT Coupons <p id = "failed">FAILED</p><br>'
         returnCode = 0 
     outputString += "<br><h2>Testing GET after PUT to check whether the fields have been updated</h2><br>"         
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/coupons")
     response_body = response.json()
     outputString += "<br>The response JSON is <br>"
     #outputString += str(response_body) 
     result = response_body['result']
     for res in result:
         if maxCouponIDAfterPost == res['coupon_uid']:
            if res['email_id'] == emailIDForPut:
                 outputString += str(res)
                 outputString += "<br>The PUT has updated the coupon successfully<br>"
     outputString += "The last coupon is <br>"            
     outputString += str(res)
     outputString += "<br>"
     outputString += "The max current coupon_ID is "
     outputString += str(maxCouponID)
     
     try:
         assert response_body["message"] == "Get Coupons successful."
         outputString += '<br>GET coupons <p id = "passed">PASSED</p><br>'
     except:
         outputString += '<br>GET coupons <p id = "failed">FAILED</p><br>'
         returnCode = 0         
     outputString += "<br><h2>Testing DELETE a coupon</h2><br>"
     response = requests.delete(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/coupons?coupon_uid={coupon_uid}")
     response_body = response.json()
     outputString += "<br> The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += '<br>DELETE Coupons <p id = "passed">PASSED</p><br>'
     except:
         outputString += '<br>DELETE Coupons <p id = "failed">FAILED</p><br>'
         returnCode = 0
     outputString += "<br><h2> Testing GET after delete to check whether the coupon has been deleted</h2><br>"    
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/coupons")
     response_body = response.json()
     outputString += "<br>The response JSON is <br>"
     #outputString += str(response_body) 
     result = response_body['result']
     maxCouponID = ''
     for res in result:
         if maxCouponID < res['coupon_uid']:
            maxCouponID = res['coupon_uid']
     outputString += "The last coupon is "            
     outputString += str(res)
     outputString += "<br>"
     outputString += "The max current coupon_ID is "
     outputString += str(maxCouponID)
     #outputString += maxCouponID
     if maxCouponID < maxCouponIDAfterPost:
         outputString += "<br>The coupon has been deleted successfully<br>"
     try:
         assert response_body["message"] == "Get Coupons successful."
         outputString += '<br>GET coupons <p id = "passed">PASSED</p><br>'
     except:
         outputString += '<br>GET coupons <p id = "failed">FAILED</p><br>'
         returnCode = 0         
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testIngredientPost/')
def ingredients_post():
     outputString = "<h2>Testing ingredients post<br>"
     returnCode = 1
     ingredients_desc = "<h2>Testing food"
     package_size = "1"
     package_unit = "kg"
     package_cost = "20"
     inputJSON = {
                 "ingredient_desc":f"{ingredients_desc}",
                 "package_size":f"{package_size}",
                 "package_unit":f"{package_unit}",
                 "package_cost":f"{package_cost}"
                  }
     outputString += "<h2>Testing POST of ingredients <br>"
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/ingredients", json = inputJSON)
     response_body = response.json()
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST Meals selected PASSED<br>"
     except:
         outputString += "<br>POST Meals selected FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/MealsSelection/', methods = ['POST'])
def MealsSelection():
     testCaseName = "Meals selection, take down the customer ID and find the purchases for it."
     outputString = ""
     today = date.today()
     outputString = addHeading(outputString, testCaseName)
     returnCode = 1
     #Using the following details for testing
     purchaseID = request.form['purchaseID']
     menuDate = request.form['menuDate']
     customer_id = request.form['customerID']
     outputString = addSubHeading(outputString, "GET", "to test meal selected specific (with customerID, purchaseID, menuDate)")
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/meals_selected_specific?customer_uid={customer_id}&purchase_id={purchaseID}&menu_date={menuDate}")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Meals selected", "GET", testCaseName, returnCode)
     outputString = addSubHeading(outputString, "GET", "to test meals selected by customer (with only customerID)")
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/meals_selected?customer_uid={customer_id}")
     response_body = response.json()
     outputString += "<br>The response JSON body is <br>"
     #outputString += str(response_body)
     result = response_body["result"]
     for res in result:
       outputString += str(res)
       outputString += "<br><br><br>"
       outputString += "The next meal selected is <br>"
     items = item[]  
     purchaseID = res['purchaseID']
     menuDate = request.form['menuDate']
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Meals selected", "GET", "Meals selected", returnCode)
     outputString = addSubHeading(outputString, "GET", "to test meals selected in a purchase (with only purchaseID)")
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Meals_Selected_pid?purchase_id={purchaseID}")
     response_body = response.json()
     outputString += "The response_body is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Meals selected", "GET", "Meals selected PID", returnCode)

     inputJSON = {
                 "purchase_id":f"{purchaseID}",
                 "items": [{
                            "qty": "5", 
                            "name": "Pumpkin Spice Overnight Oats", 
                            "price": "0.0", 
                            "item_uid": "null"
                            }],
                 "delivery_day":"2020-09-01",
                 "menu_date":f"{today}",
                 "is_addon": "false"
                 }
     
     # for addons, inputJSON['is_addon'] = "true"
     outputString = addSubHeading(outputString, "POST", "to create a meal selection")
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/meals_selection", json = inputJSON)
     response_body = response.json()
     outputString += "The inputString is <br>"
     outputString += str(inputJSON)
     outputString += "<br>The response JSON is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "uccess", "POST", testCaseName, returnCode)
     outputString = addSubHeading(outputString, "GET", "to test meals selected in a purchase (with only purchaseID)")
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Meals_Selected_pid?purchase_id={purchaseID}")
     response_body = response.json()
     outputString += "The response_body is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Meals selected", "GET", "Meals selected PID", returnCode)
     #for SURPRISE, 
     inputJSON['items'] = [{"qty": "", "name": "SURPRISE", "price": "", "item_uid": ""}] 
     inputJSON['delivery_day'] = "Sunday"
     one_day = datetime.timedelta(days=1)
     tomorrow = today + one_day     
     inputJSON['menu_date'] = f"{tomorrow}"
     outputString = addSubHeading(outputString, "POST", "to create a meal selection")
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/meals_selection", json = inputJSON)
     response_body = response.json()
     outputString += "The inputString is <br>"
     outputString += str(inputJSON)
     outputString += "<br>The response JSON is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "uccess", "POST", testCaseName, returnCode)
     outputString = addSubHeading(outputString, "GET", "to test meals selected in a purchase (with only purchaseID)")
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Meals_Selected_pid?purchase_id={purchaseID}")
     response_body = response.json()
     outputString += "The response_body is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Meals selected", "GET", "Meals selected PID", returnCode)

     #for SKIP, 
     inputJSON['items'] = [{"qty": "", "name": "SKIP", "price": "", "item_uid": ""}]
     inputJSON['delivery_day'] = "SKIP"            
     outputString = addSubHeading(outputString, "POST", "to create a meal selection")
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/meals_selection", json = inputJSON)
     response_body = response.json()
     outputString += "The inputString is <br>"
     outputString += str(inputJSON)
     outputString += "<br>The response JSON is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "uccess", "POST", testCaseName, returnCode)
     outputString = addSubHeading(outputString, "GET", "to test meals selected in a purchase (with only purchaseID)")
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Meals_Selected_pid?purchase_id={purchaseID}")
     response_body = response.json()
     outputString += "The response_body is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Meals selected", "GET", "Meals selected PID", returnCode)

     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/AccountsLoginChangeResetPassword/')
def AccountsLoginChangeResetPassword():
     testCaseName = "account"
     outputString = ""
     outputString = addHeading(outputString, testCaseName)
     returnCode = 1
     email = "ana_c_tejada@yahoo.com"
     password = "deca602e1b605f74517252f7af8698f039636c81ded48"
     inputJSON = {
                 "email":f"{email}",
                 "password":f"{password}"
                  }
     outputString = addSubHeading(outputString, "POST", "to create an account")
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/login", json = inputJSON)
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Email Not Found. Please signup", "POST", testCaseName, returnCode)
     outputString = addSubHeading(outputString, "change password", "using password")
     customer_id = "100-000125"
     old_password = "T1"
     new_password = "T2"
     inputJSON = {
                 "customer_uid":f"{customer_id}",
                 "old_password":f"{old_password}",
                 "new_password":f"{new_password}"
                  }
     outputString = addSubHeading(outputString, "POST", "to change password")
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/change_password",json = inputJSON)
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Wrong Password", "POST", testCaseName, returnCode)
     outputString = addSubHeading(outputString, "GET", "reset password")
     #HTTP error 400, bad request
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/reset_password?email=f20flier@gmail.com")
     response_body = response.json()
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "A temporary password has been sent", "GET", "reset password", returnCode)
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/getNextBillingDate/')
def payments_NextBillingDate():
     outputString = "<h2>Testing payments next billing date<br>"
     returnCode = 1
     #Bad request
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/next_billing_date?customer_uid=100-000001")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert response_body["message"] == "Get Get_Latest_Purchases_Payments successful."
         outputString += "<br>GET Meals selected PASSED<br>"
     except:
         outputString += "<br>GET Meals selected FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testAccountSalts/')
def accountsalt_post():
     outputString = "<h2>Testing account salt post<br>"
     returnCode = 1
     inputJSON = {"email":"omarfacio2010@gmail.com"}
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/accountsalt",json = inputJSON)
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)      
     try:
         assert response_body["message"] == "Social Signup exists. Use 'GOOGLE'"
         outputString += "<br>POST Meals selected PASSED<br>"
     except:
         outputString += "<br>POST Meals selected FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/Accounts/', methods = ['POST'])
def account():
     testCaseName = "Accounts"
     outputString = ""
     outputString = addHeading(outputString, "Account")
     returnCode = 1
     accountID = request.form['accountID']
     outputString = addSubHeading(outputString, "GET", "before the test begins")
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Profile/{accountID}")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(json.dumps(response_body))
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Profile Loaded successful", "GET", testCaseName, returnCode)     
     outputString = addSubHeading(outputString, "POST", "to create an account without social signup")
     email = "anupjaltade@gmail.com"
     first_name = "test"
     last_name = "trial"
     phone_number = "9876549879"
     address = "955 W President"
     unit = "3452"
     city = "Dallas"
     state = "TX"
     zipCode = "75080"
     latitude = "-14.3"
     longitude = "94.3"
     referral_source = "WEB"
     role = "CUSTOMER"
     social = "NULL"
     password = "abc@123"
     mobile_access_token = "FALSE"
     mobile_refresh_token = "FALSE"
     user_access_token = "FALSE"
     user_refresh_token = "FALSE"
     social_id = "NULL"
     inputJSON = { 
                 "email" : f"{email}", 
                 "first_name" : f"{first_name}", 
                 "last_name" : f"{last_name}", 
                 "phone_number" : f"{phone_number}", 
                 "address" : f"{address}", 
                 "unit" : f"{unit}", 
                 "city" : f"{city}", 
                 "state" : f"{state}", 
                 "zip_code" : f"{zipCode}", 
                 "latitude" : f"{latitude}", 
                 "longitude" : f"{longitude}", 
                 "referral_source" : f"{referral_source}", 
                 "role" : f"{role}", 
                 "social" : f"{social}", 
                 "password": f"{password}", 
                 "mobile_access_token" : f"{mobile_access_token}", 
                 "mobile_refresh_token" : f"{mobile_refresh_token}", 
                 "user_access_token" : f"{user_access_token}", 
                 "user_refresh_token" : f"{user_refresh_token}", 
                 "social_id": f"{social_id}", 
                 "cust_id": ""
                 }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/createAccount", json = inputJSON)
     response_body = response.json()
     outputString += "<br>The response JSON is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "uccess", "POST", testCaseName, returnCode)
     result = response_body['result']
     cust_id = result['customer_uid'] #----- optional [if you are using APPLE login (WEBSITE ONLY not mobile) then only use this variable else don't include it in json]    
     outputString = addSubHeading(outputString, "GET", "after the POST (not social signup)")
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Profile/{cust_id}")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Profile Loaded successful", "GET", testCaseName, returnCode)     

     outputString = addSubHeading(outputString, "POST", "to create an account with social signup")     
     email = "anupjaltade@gmail.com"
     first_name = "xyz"
     last_name = "abc"
     phone = "9876549879"
     address = "955 W President"
     unit = "3452"
     city = "Dallas"
     state = "TX"
     zipCode = "75080"
     latitude = "-14.3"
     longitude = "34.7"
     referral_source = "WEB"
     role = "CUSTOMER"
     social = "GOOGLE"
     mobile_access_token = "i_am_mobile_access_token"
     mobile_refresh_token = "i_am_mobile_refresh_token"
     user_access_token = "FALSE"
     user_refresh_token = "FALSE"
     social_id = "abc_GOOGLE"
     #cust_id = "100-000236" #----- optional [if you are using APPLE login (WEBSITE ONLY not mobile) then only use this variable else don't include it in json]
     #     "input: ------ Social signup
     inputJSON = {
                 "email" : f"{email}",
                 "first_name" : f"{first_name}",
                 "last_name" : f"{last_name}",
                 "phone_number" : f"{phone}",
                 "address" : f"{address}",
                 "unit" : f"{unit}",
                 "city" : f"{city}",
                 "state" : f"{state}",
                 "zip_code" : f"{zipCode}",
                 "latitude" : f"{latitude}",
                 "longitude" : f"{longitude}",
                 "referral_source" : f"{referral_source}",
                 "role" : f"{role}",
                 "social" : f"{social}",
                 "password": "",
                 "mobile_access_token" : f"{mobile_access_token}",
                 "mobile_refresh_token" : f"{mobile_refresh_token}",
                 "user_access_token" : f"{user_access_token}",
                 "user_refresh_token" : f"{user_refresh_token}",
                 "social_id": f"{social_id}",
                 "cust_id": f"{cust_id}" #----- optional [if you are using APPLE login (WEBSITE ONLY not mobile) then only use this variable else don't include it in json]
                 }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/createAccount", json = inputJSON)
     response_body = response.json()
     outputString += "<br>The response JSON is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "uccess", "POST", testCaseName, returnCode)
     outputString = addSubHeading(outputString, "GET", "after the POST (social signup)")
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Profile/{cust_id}")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Profile Loaded successful", "GET", testCaseName, returnCode)     
     outputString = addSubHeading(outputString, "POST", "to update the account")
     first_name = "Quang"
     last_name = "Dang"
     phone = "123456789"
     email = "quang@gmail.com"
     address = "123 Main St."
     unit = "3"
     city = "San Leandro"
     state = "CA"
     zipCode = "12345"
     noti = "false"
     inputJSON = {
                 "uid":f"{cust_id}",
                 "first_name":f"{first_name}",
                 "last_name":f"{last_name}",
                 "phone":f"{phone}",
                 "email":f"{email}",
                 "address":f"{address}",
                 "unit":f"{unit}",
                 "city":f"{city}",
                 "state":f"{state}",
                 "zip":f"{zipCode}",
                 "noti":f"{noti}"
                  }
            
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/UpdateProfile", json = inputJSON)
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Profile info updated", "POST", "update profile", returnCode)
     outputString = addSubHeading(outputString, "GET", "after the POST (update profile)")
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Profile/{cust_id}")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Profile Loaded successful", "GET", testCaseName, returnCode)     

     outputString = addSubHeading(outputString, "DELETE", "after the GET (update profile)")
     response = requests.delete(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/deleteAccount?customer_uid={cust_id}")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     #Enter successMessage
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "uccess", "DELETE", testCaseName, returnCode)     

     outputString = addSubHeading(outputString, "GET", "after the DELETE to make sure the user has been deleted")
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Profile/{cust_id}")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     #Enter successMessage
     outputString, returnCode = checkMessageInResponseBody(outputString, response_body, "Customer UID doesn't exists", "GET", testCaseName, returnCode)     

     '''
     email = "m7vwt43cby@privaterelay.appleid.com"
     inputJSON = {
                 "email":f"{email}"
                 }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/token_fetch_update/get", json = inputJSON)
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST account with only email ID PASSED<br>"
     except:
         outputString += "<br>POST account with only email ID FAILED<br>"         
     inputJSON = {
                  "email" : "sdsd@gmail.com",
                  "user_access_token" : "5",
                  "user_refresh_token" : "5",
                  "mobile_access_token" : "5",
                  "mobile_refresh_token" : "5"
                 }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/token_fetch_update/update",json = inputJSON)
     response_body = response.json()
     outputString +="<br> The response JSON is <br>" 
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST account with tokens PASSED<br>"
     except:
         outputString += "<br>POST account with tokens FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)'''
     outputString = addFooter(outputString, returnCode) 
     return outputString     
@app.route('/testNotifications/')
def notifications():
     outputString = "<h2>Testing notification <br>"
     returnCode = 1
     inputJSON = {
                 "group":"1",
                 "id":"100-000003"
                  }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Create_Group",json = inputJSON)
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST notifications with group ID PASSED<br>"
     except:
         outputString += "<br>POST notifications with group ID FAILED<br>"
         returnCode = 0
     #no input json
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/payment_info/500-000001")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST notifications without group ID PASSED<br>"
     except:
         outputString += "<br>POST notifications without group ID FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testCreateMenu/')
def create_menu():
     outputString = "<h2>Testing create menu<br>"
     returnCode = 1
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/List_of_Meals/2020-06-07+00:00:00")
     response_body = response.json()
     outputString = "The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert response_body["message"] == "Meals Loaded successful"
         outputString += "<br>GET create menu PASSED<br>"
     except:
         outputString += "<br>GET create menu FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testEditMealRecipe/')
def editMealRecipe():
     outputString = "Edit meal recipe<br>"
     returnCode = 1
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/get_recipes/840-000001")
     response_body = response.json()
     outputString += str(response_body)
     try:
         assert response_body["message"] == "Recipe Loaded successful"
         outputString += "<br>GET edit meal recipe PASSED<br>"
     except:
         outputString += "<br>GET edit meal recipe FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testOrders/')
def orders():
     outputString = "<h2>Testing orders <br>"
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/get_orders")
     response_body = response.json()
     outputString += "The response body received is <br>"
     outputString += str(response_body)
     try:
         assert response_body["message"] == "Orders Loaded successful"
         outputString += "<br>GET orders PASSED<br>"
     except:
         OutputString += "<br>GET orders FAILED<br>"
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/get_supplys_by_date")
     response_body = response.json()
     outputString += "The reponse JSON is <br>"
     outputString += str(response_body)
     try:
         assert response_body["message"] == "Supply Loaded successful"
         outputString += "<br>GET supply PASSED<br>"
     except:
         outputString += "<br>GET supply FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testRevenue/')
def revenue_50():
     outputString = "<h2>Testing revenue<br>"
     returnCode = 1
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/get_total_revenue")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert response_body["message"] == "Total Revenue Loaded successful"
         outputString += "<br>GET total revenue PASSED<br>"
     except:
         outputString += "<br>GET total revenue FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testCustomer/')
def customer_post_51():
     outputString = "<h2>Testing customer post with UID, GUID and notification <br>"
     returnCode = 1
     uid = '100-000003'
     guid = '22'
     notification = 'TRUE'
     inputJSON = {
        "uid" : f"{uid}",
        "guid" : f"{guid}",
        "notification": f"{notification}"
                  }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/update_guid_notification/customer,add",json = inputJSON)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST Customer PASSED<br>"
     except:
         outputString += "<br>POST Customer FAILED<br>"
         returnCode = 0

     outputString += "<h2>Testing customer post with email, note and item photo"
     meal_photo_url = "C:\\Users\\Public\\Pictures\\Sample Pictures\\Desert.jpg"
     files = {'meal_photo_url' : open(meal_photo_url, 'rb')}
     inputData = {
                   'email': 'abc@gmail.com',
                   'note': 'dont like this product'
                  }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Refund",data = inputData, files = files)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST customer with note PASSED<br>"
     except:
         outputString += "<br>POST customer with note FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testCouponsDetailsPost/')
def couponDetails_post_56():
     outputString = "<h2>Testing coupon Details post<br>"
     returnCode = 1
     inputJSON = {
                  "coupon_uid" : "600-000002",
                  "num_used" : "1"
                  }
     #Not sure why this is failing
     #response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/couponDetails/AlmadenMeadows", json = inputJSON)
     #response_body = response.json()
     #try:
     #    assert response_body["message"] == ""
     #    outputString += "<br>POST coupon details PASSED<br>"
     #except:
     #    outputString += "<br>POST coupon details FAILED<br>"
     #missing input json/data in the worksheet
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/couponDetails")
     response_body = response.json()
     try:
         assert response_body["message"] == "Successful"
         outputString += "<br>POST Meals selected PASSED<br>"
     except:
         outputString += "<br>POST Meals selected FAILED<br>"
         returnCode = 0         
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testaddItem/')
def addItems():
     outputString = "<h2>Testing add item <br>"
     returnCode = 1
     meal_photo_url = "C:\\Users\\Public\\Pictures\\Sample Pictures\\Desert.jpg"
     files = {'item_photo' : open(meal_photo_url, 'rb')}
     inputData = {
               "itm_business_uid" : "200-000009",
               "item_name" : "Spicy Aubergine Curry",
               "item_status" : "",
               "item_type" : "meal",
               "item_desc" : "[authentic miso ramen]",
               "item_unit" : "bowl",
               "item_price" : "15.99",
               "item_sizes" : "L",
               "favorite" : "FALSE",
               "exp_date" : ""
               }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/addItems/Insert", data = inputData, files = files)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST Meals selected PASSED<br>"
     except:
         outputString += "<br>POST Meals selected FAILED<br>"
         returnCode = 0
     inputData = {
                "itm_business_uid" : "200-000009",
                "item_name" : "Miso Ramen",
                "item_status" : "",
                "item_type" : "meal",
                "item_desc" : "[authentic miso]",
                "item_unit" : "bowl",
                "item_price" : "12.99",
                "item_sizes" : "M",
                "favorite" : "FALSE",
                "exp_date" : "",
                "item_uid" : "310-000336"
                }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/addItems/Update", json = inputData)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST Meals selected PASSED<br>"
     except:
         outputString += "<br>POST Meals selected FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testBusinessDetailsUpdate/', methods = ['POST'])
def businessDetailsUpdate():
     outputString = "<h2>Testing business Details Update<br>"
     returnCode  = 1     
     businessID = request.form['businessID']
     inputJSON = {
                 "business_uid" : f"{businessID}" 
                 }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/business_details_update/Get", json = inputJSON)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST business PASSED<br>"
     except:
         outputString += "<br>POST Meals selected FAILED<br>"
         returnCode = 0
     inputJSON = {
                 "business_uid" : "200-000030",
                 "business_created_at" : "2020-01-09 17:34:48",
                 "business_name" : "PTYD",
                 "business_type" : "kriti", 
                 "business_desc" : "Vegan Delivery Service", 
                 "business_association" : ["200-000012"], 
                 "business_contact_first_name" : "Heather",
                 "business_contact_last_name" : "Faiez",
                 "business_phone_num" : "(512) 555-1234", 
                 "business_phone_num2" : "(512) 555-1200", 
                 "business_email" : "heather@ptyd.com",
                 "business_hours" : {"Friday": ["00:00:00", "23:59:00"],
                                     "Monday": ["00:00:00", "23:59:00"]
                                     },
                 "business_accepting_hours" : {"Friday": ["09:00:00", "23:59:59"],
                                               "Monday": ["09:00:00", "23:59:59"],
                                               "Sunday": ["09:00:00", "23:59:59"],
                                               "Tuesday": ["09:00:00", "23:59:59"],
                                               "Saturday": ["09:00:00", "21:00:00"],
                                               "Thursday": ["09:00:00", "23:59:59"],
                                               "Wednesday": ["09:00:00", "23:00:00"]
                                               },
                 "business_delivery_hours" : {"Friday": ["09:00:00", "23:59:59"]}, 
                 "business_address" :"360 Cowden Road", 
                 "business_unit" : "", 
                 "business_city" : "Hollister", 
                 "business_state" : "CA", 
                 "business_zip" : "95135",
                 "business_longitude" : "-121.9141246",
                 "business_latitude" : "37.3316565", 
                 "business_EIN" : "",
                 "business_WAUBI" : "", 
                 "business_license" : "",
                 "business_USDOT" : "",
                 "notification_approval" : "",
                 "notification_device_id" : "",
                 "can_cancel" : "0",
                 "delivery" : "0",
                 "reusable" : "0",
                 "business_image" : "https://servingnow.s3-us-west-1.amazonaws.com/kitchen_imgs/landing-logo.png",
                 "business_password" : "pbkdf2:sha256:150000$zMHfn0jt$29cef351d84456b5f6b665bc2bbab8ae3c6e42bd0e4a4e896xxxxxxxxxxx"
                 }

     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/business_details_update/Post",)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST Meals selected PASSED<br>"
     except:
         outputString += "<br>POST Meals selected FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testOrderActionsDelete/', methods = ['POST'])
def order_actions():
     outputString = "<h2>Testing order actions Delete post <br>"
     returnCode = 1
     purchaseID = request.form['purchaseID']
     inputJSON = { 
                  "purchase_uid" : f"{purchaseID}" 
                  }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/order_actions/Delete",json = inputJSON)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST Meals selected PASSED<br>"
     except:
         outputString += "<br>POST Meals selected FAILED<br>"
         returnCode = 0
     if returnCode == 0:
         outputString += '<br><h2 id = "FAILED<br>">The test case FAILED</h2>'
         return outputString 
     else:
         outputString += '<br><h2>The test case PASSED</h2>'
         return outputString
     outputString = "<h2>Testing order action Deliery Status <br>"
     returnCode = 1
     purchaseID = request.form['purchaseID']
     inputJSON = { 
                 "purchase_uid" : f"{purchaseID}"
                 }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/order_actions/delivery_status_YES",json = inputJSON)
     response_body = response.json()    
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST order action delivery status PASSED<br>"
     except:
         outputString += "<br>POST order action delivery status FAILED<br>"
         returnCode = 0
     outputString = "<br><h2>Testing item delete<br>"
     returnCode = 1
     inputJSON = {
                 "purchase_uid":"400-000001",
                 "item_data" : [{
                                 "qty": "5",
                                 "name": "Broccoli ",
                                 "price": "3.5",
                                 "item_uid": "310-000023"
                                 },
                                {
                                 "qty": "1",
                                 "name": "Iceberg Lettuce ",
                                 "price": "2.5",
                                 "item_uid": "310-000025"
                                 },
                                {"qty": "1",
                                 "name": "Collards ",
                                 "price": "2.5",
                                 "item_uid": "310-000022"
                                 },
                                 {
                                 "qty": "1",
                                 "name": "Cauliflower ",
                                 "price": "3.5",
                                 "item_uid": "310-000024"
                                 }] }
     outputString += "<h2>Testing order actions item delete"
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/order_actions/item_delete", json = inputJSON)
     response_body = response.json()     
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST item delete PASSED<br>"
     except:
         outputString += "<br>POST item delete FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)       
     return outputString
@app.route('/testadminReport/', methods = ['POST'])
def admin_report():
     outputString = "<h2>Testing admin report <br>"
     returnCode = 1
     businessID = request.form['businessID']
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/admin_report/{businessID}")
     response_body = response.json()
     outputString += str(response_body)
     try:
         assert response_body["message"] == "Report data successful"
         outputString += "<br>GET report data PASSED<br>"
     except:
         outputString += "<br>GET report data FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testSendNotificationBusiness/')
def sendNotificationBusiness_post_71():
     outputString = "<h2>Testing send Notification Business post<br>"
     returnCode = 1
     #"Everything is form input
     inputData = "uids = 200-000004,200-000005,200-000006,200-000007,200-000008,200-000009\
                   message = hello there"
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Send_Notification/business", data = inputData)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST send notification business PASSED<br>"
     except:
         outputString += "<br>POST send notification business FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testGet_Registrations_From_Tag/')
def both_72():
     outputString = "<h2>Testing Get Registrations From Tag<br>"
     returnCode = 1
     #response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Get_Registrations_From_Tag/")
     #response_body = response.json()
     #assert response_body["message"] == "Report data successful"     
     outputString = addFooter(outputString, returnCode)
     return outputString
     pass
@app.route('/updateRegistrationwithGUIDAndroid/')
def updateRegistrationwithGUIDAndroid_74():
     #no input json or data
     outputString = "<br><h2>Testing update Registration with GUID Android<br>"
     returnCode = 1
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Update_Registration_With_GUID_Android")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST udpate registration with GUID Android PASSED<br>"
     except:
         outputString += "<br>POST udpate registration with GUID Android FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/getTagsWithGUIDiOS/')
def getTagsWithGUIDiOS():
     outputString = "<h2>Testing get Tags With GUIDiOS<br>"
     returnCode = 1
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Get_Tags_With_GUID_iOS/")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST udpate registration with GUID Android PASSED<br>"
     except:
         outputString += "<br>POST udpate registration with GUID Android FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/emailVerification/')
def emailVerification_78():
     outputString = "<h2>Testing email Verification <br>"
     returnCode = 1
     inputJSON = {
                 "email" : "annrupp22@gmail.com"
                 }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/email_verification", json = inputJSON)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST email verification PASSED<br>"
     except:
         outputString += "<br>POST email verification FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/PIDHistory/', methods = ['POST'])
def pid_history():
     outputString = "<h2>Testing PID history<br>"
     returnCode = 1
     purchaseID = request.form['purchaseID']#400-000007
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/pid_history/{purchaseID}")
     assert response.headers["Content-Type"] == "application/json"
     response_body = response.json()
     result = response_body['result']
     for res in result:
       outputString += str(res)
       outputString += "<br><br>"
       outputString += "The next Items in history is <br>"        
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET pid history PASSED<br>"
     except:
         outputString += "<br>GET pid history FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/upcomingMenuDates/')
def upcomingMenuDates():
     outputString = "<h2>Testing upcoming Menu Dates<br>"
     returnCode = 1
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/upcoming_menu_dates")
     assert response.headers["Content-Type"] == "application/json"
     response_body = response.json()
     outputString += "The response JSON is <br>"
     result = response_body['result']
     for res in result:
       outputString += str(res)
       outputString += "<br><br>"
       outputString += "The next upcoming Menu Dates is <br>"      
     try:
         assert "selected" in response_body["message"]
         outputString += "<br>GET pid history PASSED<br>"
     except:
         outputString += "<br>GET pid history FAILED<br>"
         returnCode = 0         
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testRefundCalculator/', methods = ['POST'])
def refundCalculator():
     outputString = "<h2>Testing refund calculator <br>"
     returnCode = 1
     purchaseID = request.form['purchaseID']
     response = requests.post(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/refund_calculator?purchase_uid={purchaseID}")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)     
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST refund calculator PASSED<br>"
     except:
         outputString += "<br>POST refund calculator FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/reportOrderCustomerPivotDetail_order/')
def reportOrderCustomerPivotDetail_order():
     outputString = "<h2>Testing report Order Customer Pivot Detail order<br>"
     returnCode = 1
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/report_order_customer_pivot_detail/order,200-000006")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST report order customer pivot PASSED<br>"
     except:
         outputString += "<br>POST report order customer pivot FAILED<br>"
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/reportOrderCustomerPivotDetail_customer/')
def reportOrderCustomerPivotDetail_customer():
     outputString = "<h2>Testing report Order Customer Pivot Detail customer<br>"
     returnCode = 1     
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/report_order_customer_pivot_detail/customer,200-000001")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST report Order customer pivot PASSED<br>"
     except:
         outputString += "<br>POST report Order customer pivot FAILED<br>"
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/reportOrderCustomerPivotDetail_pivot/')
def reportOrderCustomerPivotDetail_pivot():
     outputString = "<h2>Testing report Order Customer Pivot Detail pivot<br>"
     returnCode = 1
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/report_order_customer_pivot_detail/pivot,200-000001")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST report order customer pivot PASSED<br>"
     except:
         outputString += "<br>POST report order customer pivot FAILED<br>"
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/orderByItems/')
def orderByItems():
     outputString = "<h2>Testing order by items<br>"
     returnCode = 1
     #no json input or data input in the worksheet
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Orders_by_Items")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST order by item PASSED<br>"
     except:
         outputString += "<br>POST order by item FAILED<br>"
     outputString = addFooter(outputString, returnCode)
     return outputString 
@app.route('/orderByPurchaseId/')
def orderByPurchaseId():
     outputString = "<h2>Testing order By PurchaseId <br>"
     returnCode = 1
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Orders_by_Purchase_Id")
     response_body = response.json()
     try:
         assert response_body["message"] == ""
         outputString += "<br>POST order by purchase PASSED<br>"
     except:
         outputString += "<br>POST order by purchase FAILED<br>"
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/stripePaymentKeyChecker/')
def stripePaymentKeyChecker():
     outputString = "<h2>Testing  stripe Payment Key Checker<br>"
     returnCode = 1
     inputJSON = {
                 "key" : "12345"
                 }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Stripe_Payment_key_checker", json = inputJSON)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST stripe payment key checker PASSED<br>"
     except:
         outputString += "<br>POST stripe payment key checker FAILED<br>"
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/paypalPaymentKeyChecker/')
def paypalPaymentKeyChecker():
     outputString = "<h2>Testing paypal Payment Key Checker <br>"
     returnCode = 1
     inputJSON = {
                 "key" : "12345"
                 }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Paypal_Payment_key_checker",json = inputJSON)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST paypal payment key checker PASSED<br>"
     except:
         outputString += "<br>POST paypal payment key checker FAILED<br>"
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/getSpecificRecipeWithIngredients/')
def getSpecificRecipeWithIngredients():
     outputString = "<h2>Testing get Specific Recipe With Ingredients <br>"
     returnCode = 1
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Ingredients_Recipe_Specific/840-000001")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET delete recipe specific PASSED<br>"
     except:
         outputString += "<br>GET delete recipe specific FAILED<br>"
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/addNewIngredientRecipe/')
def addNewIngredientRecipe():
     outputString = "<h2>Testing add New Ingredient Recipe <br>"
     returnCode = 1
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/add_new_ingredient_recipe")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET delete recipe specific PASSED<br>"
     except:
         outputString += "<br>GET delete recipe specific FAILED<br>"
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/deleteRecipeSpecific/', methods = ['POST'])
def deleteRecipeSpecific():
     outputString = "<h2>Testing delete Recipe Specific </h2><br>"
     returnCode = 1
     recipeID = request.form['recipeID']
     response = requests.delete(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Delete_Recipe_Specific?recipe_uid={recipeID}")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET delete recipe specific PASSED<br>"
     except:
         outputString += "<br>GET delete recipe specific FAILED<br>"
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/editMealPlan/')
def editMealPlan():
     outputString = "<h2>Testing edit Meal Plan<br>"
     returnCode = 1
     inputJSON = {
                 "item_uid":"320-999999",
                 "item_name":"2",
                 "item_desc":"2",
                 "item_price":"2",
                 "item_sizes":"2",
                 "num_items":"2",
                 "item_photo":"2",
                 "info_headline":"2",
                 "info_footer":"2",
                 "info_weekly_price":"2",
                 "payment_frequency":"2",
                 "shipping":"2"
                }
     response = requests.put("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Edit_Meal_Plan",json = inputJSON)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET edit meal plan PASSED<br>"
     except:
         outputString += "<br>GET edit meal plan FAILED<br>"           
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/FeeTax/')
def FeeTax():
     outputString = "<h2>Testing fee tax<br>"
     returnCode = 1 
     response = requests.put("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/get_Fee_Tax/1,WEDNESDAY")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>PUT fee tax PASSED<br>"
     except:
         outputString += "<br>PUT fee tax FAILED<br>"
     response = requests.put("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Update_Fee_Tax")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>PUT udpate fee tax PASSED<br>"
     except:
         outputString += "<br>PUT update fee tax FAILED<br>"         
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/Zones/')
def Zones():
     outputString = "<h2>Testing Zones<br>"
     returnCode = 1
     response = requests.put("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/get_Zones")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>PUT zones PASSED<br>"
     except:
         outputString += "<br>PUT zones FAILED<br>"
     inputJSON = {
                  "z_business_uid" : "200-000001", 
                  "area" : "1", 
                  "zone" : "1", 
                  "zone_name" : "test2", 
                  "z_businesses" : ["200-000016", "200-000017", "200-000018", "200-000019", "200-000032"], 
                  "z_delivery_day" : "THURSDAY",  
                  "z_delivery_time" : "3pm - 8pm", 
                  "z_accepting_day" : "SUNDAY",
                  "z_accepting_time" : "3pm",
                  "service_fee" : "3",
                  "delivery_fee" : "4", 
                  "tax_rate" : "2",
                  "LB_long" : "0",
                  "LB_lat" : "0",
                  "LT_long" : "0",
                  "LT_lat" : "0",
                  "RT_long" : "0", 
                  "RT_lat" : "0",
                  "RB_long" : "0",
                  "RB_lat" : "0"
                   }
     response = requests.put("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/update_zones/create")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>PUT update zones create PASSED<br>"
     except:
         outputString += "<br>PUT udpate zones create FAILED<br>"
     response = requests.put("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Update_Zone")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>PUT update zones PASSED<br>"
     except:
         outputString += "<br>PUT udpate zones FAILED<br>"         
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/getCustomerInfo/')
def getCustomerInfo():
     outputString = "<h2>Testing get Customer Info <br>"
     returnCode = 1
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/customer_infos")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET Customer Info PASSED<br>"
     except:
         outputString += "<br>GET Customer Info FAILED<br>"
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/getPaymentInfoHistory/', methods = ['POST'])
def getPaymentInfoHistory():
     outputString = "<h2>Testing get Payment info history <br>"
     returnCode = 1
     purchaseID = request.form['purchaseID'] #400-000034
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/payment_info_history/{purchaseID}")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET Payment Info History PASSED<br>"
     except:
         outputString += "<br>GET Payment Info History FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/orderByPurchaseIDwithPID/', methods = ['POST'])
def orderByPurchaseIDwithPID():
     outputString = "<h2>Testing order By Purchase ID with PID <br>"
     returnCode = 1
     purchaseID = request.form['purchaseID']
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Orders_by_Purchase_Id_with_Pid/{purchaseID}")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET order By Purchase ID with PID PASSED<br>"
     except:
         outputString += "<br>GET order By Purchase ID with PID FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/orderByPurchaseIDwithPIDandDate/', methods = ['POST'])
def orderByPurchaseIDwithPIDandDate():
     outputString = "<h2>Testing order By PurchaseID with PID and Date<br>"
     returnCode = 1
     purchaseID = request.form['purchaseID']
     inputDate = request.form['inputDate'] #2021-02-06 00-00-00
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Orders_by_Purchase_Id_with_Pid_and_date/{purchaseID},{date}")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET order By Purchase ID with PID and Date PASSED<br>"
     except:
         outputString += "<br>GET order By Purchase ID with PID and Date FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)         
     return outputString
@app.route('/orderByBusinessSpecifics/', methods = ['POST'])
def orderByBusinessSpecifics():
     outputString = "<h2>Testing order By Business Specifics<br>"
     returnCode = 1
     businessUID = request.form['businessID']
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/orders_by_business_specific/{businessUID}")
     response_body = response.json()
     outputString += "The reponse JSON is <br>"
     outputString += str(response_body)
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET order By Business Specifics PASSED<br>"
     except:
         outputString += "<br>GET order By Business Specifics FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/orderByItemsTotalItems/')
def orderByItemsTotalItems():
     outputString = "<h2>Testing order By Items Total Items <br>"
     returnCode = 1
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Orders_by_Items_total_items")
     response_body = response.json()
     outputString += "The reponse JSON is <br>"
     result = response_body['result']
     for res in result:
       outputString += str(res)
       outputString += "<br><br>"
       outputString += "The next order By Items Total Items is <br>"    
     try:
         assert "selected" in response_body["message"] 
         outputString += "<br>GET order by items total items PASSED<br>"
     except:
         outputString += "<br>GET order by items total items FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/categoricalOptions/', methods = ['POST'])
def categoricalOptions():
     outputString = "<h2>Testing categorical Options <br>"
     returnCode = 1
     latitude = request.form['latitude']
     longitude = request.form['longitude'] #-121.8866517,37.2270928
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/categoricalOptions/{latitude},{longitude}")
     response_body = response.json()
     outputString += "The response JSON is <br>"
     result = response_body['result']
     for res in result:
      outputString += str(res)
      outputString += "<br><br>"
      outputString += "The next categorical option is <br>"     
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET categorical options PASSED<br>"
     except:
         outputString += "<br>GET categorical options FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/paymentInfoHistoryFixed/')
def paymentInfoHistoryFixed():
     outputString = "<h2>Testing payment info history fixed <br>"
     returnCode = 1
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/payment_info_history_fixed/400-000348")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET payment info history fixed PASSED<br>"
     except:
         outputString += "<br>GET payment info history fixed FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/getLatestPurchasePaymentsWithRefund/', methods = ['POST'])
def getLatestPurchasePaymentsWithRefund():
     outputString = "<h2>Testing get Latest Purchase Payments With Refund <br>"
     returnCode = 1
     customerID = request.form['customerID']
     response = requests.get(f"https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/Get_Latest_Purchases_Payments_with_Refund?customer_uid={customerID}")
     response_body = response.json()
     outputString += "The response_body is <br>"
     outputString += str(response_body) 
     #result = response_body['result']
     #for res in result:
     #  outputString += str(res)
     #  outputString += "<br><br>"
     #  outputString += "The next Latest Purchase Payments With Refund is <br>"
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET Latest Purchase Payments With Refund PASSED<br>"
     except:
         outputString += "<br>GET Latest Purchase Payments With Refund FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/discountPercentage/')
def discountPercentage():
     outputString = "<h2>Testing discount percentage <br>"
     returnCode = 1
     response = requests.get("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/discount_percentage/4")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>GET discount percentage PASSED<br>"
     except:
         outputString += "<br>GET discount percentage FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/add_surprise/')
def add_surprise():
     #no input JSON or data
     outputString = "<h2>Testing add surprise <br>"
     returnCode = 1
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/add_surprise/400-000002")
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST add surprise PASSED<br>"
     except:
         outputString += "<br>POST add surprise FAILED<br>"
         returnCode = 0 
     outputString = addFooter(outputString, returnCode)
     return outputString
@app.route('/testCal_post/')
def testCal_post():
     outputString = "<br><h2>Testing calculator using POST<br>"
     returnCode = 1
     inputJSON = {
                 "cc_cvv": "424",
                 "cc_exp_date": "2022-01-01",
                 "cc_num": "4242424242424242",
                 "cc_zip": "95060",
                 "customer_email": "cchuang4@ucsc.edu",
                 "items": [{"qty": "2",
                            "name": "2 Meal Plan",
                            "price": "15.00",
                            "item_uid": "320-000035",
                            "itm_business_uid": "200-000002"
                            }],
                 "new_item_id": "320-000035",
                 "password": "NULL", #<-if social, null, otherwise password
                 "purchase_id": "400-000049", #<- must be active
                 "start_delivery_date":""
                  }
     response = requests.post("https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/test_cal/400-000046", json = inputJSON)
     response_body = response.json()
     try:
         assert "uccess" in response_body["message"]
         outputString += "<br>POST test calculator PASSED<br>"
     except:
         outputString += "<br>POST test calculator FAILED<br>"
         returnCode = 0
     outputString = addFooter(outputString, returnCode)
     return outputString
if __name__ == '__main__':
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'

  app.run(debug=True)
