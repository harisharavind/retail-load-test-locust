#!/usr/bin/env python3

import uuid, sys, random, os, json
from locust import HttpUser, task, constant
from datetime import datetime, timedelta

#some global vars
raworder_data = ""
test_users = ""
access_token = "dummy-loadtest" 
r_host = ""
h_host=""
starttime=""
endtime=""

class MyUser(HttpUser):
    host = "nevermind"
    #wait between executing tasks
    #wait_time = constant(5)

    # this happens only once
    def on_start(self):
        print("on_start test")
        #Read in the file
        self.read_test_orders()
        self.read_draft_raw_order()
        self.read_test_user()
        self.get_config_and_identity_token()
        self.getstarttime()
        self.getendtime()

    @task(10)
    def syncOrder(self):
        global raworder_data
        global access_token
        global r_host
        global h_host
        orderId = str(uuid.uuid4())
        customerId = 'customerid-1234'
        ordernumber = self.random_order_number()
        print("task starting test: {}".format(orderId))
        current_order = raworder_data
        #Replace the target string
        current_order = current_order.replace('@OrderID', orderId)
        current_order = current_order.replace('@CustomerID', customerId)
        current_order = current_order.replace('@OrderNumber', ordernumber)
        #Write the file out again
        #with open('orders/'+orderId+'.txt', 'w+') as order_file:
        #    order_file.write(current_order)
        #sync order
        sync_headers = {"Content-Type": "application/json", "Authorization":"Bearer "+access_token, "traceId": "loadtest"}
        response = self.client.post(r_host, data=current_order, headers=sync_headers, name="sync order")
        print("response code is {}".format(response.status_code))
    
    def GetOrder(self):
        global access_token
        global h_host
        orderId = self.random_ppe_test_order()
        print("task starting test GetOrder: {}".format(orderId))
        headers = {"Content-Type": "application/json", "Authorization":"Bearer "+access_token, "traceId": "loadtest", "channel": "store"}
        #print("Headers: {}".format(headers))
        #print("URL: {}".format(h_host+"/orders/"+orderId+"?channel=store", headers=headers, name="Get Order"))
        response = self.client.get(h_host+"/orders/"+orderId+"?channel=store", headers=headers, name="Get Order")
        print("response code is {}".format(response.status_code))

    def SearchOrder(self):
        global access_token
        global h_host
        global starttime
        global endtime
        print("task starting test Search Order")
        headers = {"Content-Type": "application/json", "Authorization":"Bearer "+access_token, "traceId": "loadtest", "channel": "store"}
        #print("Headers: {}".format(headers))
        #print("URL: {}".format(h_host+"/orders/search?limit=20&startDateTime=" + startDateTime + "&endDateTime=" + endDateTime, headers=headers, name="Search Order"))
        response = self.client.get(h_host+"/orders/search?limit=20&startDateTime=" + starttime + "&endDateTime=" + endtime, headers=headers, name="Search Order")
        print("response code is {}".format(response.status_code))
            
    def random_test_user(self):
        global test_users
        return random.choice(test_users)
        
    def random_ppe_test_order(self):
        global test_orders
        return random.choice(test_orders)

    def getstarttime(self):
        global starttime
        starttime = datetime.utcnow() - timedelta(days=1)
        starttime = str(starttime.isoformat())[:-3] + 'Z'
        print("starttime {}".format(starttime))

    def getendtime(self):
        global endtime
        endtime = datetime.utcnow() - timedelta(days=1)
        endtime = str(endtime.isoformat())[:-3] + 'Z'
        print("endtime {}".format(endtime))

    def read_draft_raw_order(self):
        global raworder_data
        with open('raworders/draft-raworder.json', 'r') as raworder_file :
            raworder_data = raworder_file.read()

    def read_test_user(self):
        global test_users
        test_users = open('TestUsers.txt','r').read().splitlines()

    def read_test_orders(self):
        global test_orders
        test_orders = open('TestOrders.txt','r').read().splitlines()

    def get_config_and_identity_token(self):
        global access_token
        global r_host
        global h_host
        with open('config/config.json','r') as identity_config :
            r_host = identity_config_data['rHost']
            h_host = identity_config_data['hHost']
        #do any initial identity/authentication related activities here
        print(access_token)   
        
    def random_order_number(self):
        ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        printable = digits + ascii_uppercase 
        res = ''.join(random.choices(printable, k = 16))
        return res
