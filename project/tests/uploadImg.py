# -*- coding: utf-8 -*-
"""
This is a test script.
This script will test te route /api
"""
import requests
import time

# Start Test
from flask import json

start = time.time()
'''
# URL
url = "http://localhost:5004/v1/images/upload"
print "URL : " + url

payload = {"urls":
    [
        "https://farm3.staticflickr.com/2879/11234651086_681b3c2c00_b_d.jpg",
        "https://farm4.staticflickr.com/3790/11244125445_3c2f32cd83_k_d.jpg",
        "https://farm4.staticflickr.com/3790/11244125445_3c2f32cd83_k_d2.jpg"
    ]
}

r = requests.post(url,headers={'Content-Type':'application/json'}, json=payload).content

print "Response: {}".format(r)

jobId = json.loads(r)["jobId"]


url = "http://localhost:5004/v1/images/upload/" + jobId
print "URL : " + url

time.sleep(5)
payload = {}
r = requests.get(url,headers={}).content

print "Response: {}".format(r)
'''
url = "http://localhost:5004/v1/images"
print "URL : " + url

payload = {}
r = requests.get(url,headers={}).content

print "Response: {}".format(r)


done = time.time()
elapsed = done - start
print "This test was done in ", elapsed, "seconds"