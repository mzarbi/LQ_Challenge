# project/server/tests/test_main.py
import json
import requests
import unittest
from unittest import TestCase

import time

import sys


class TestMainBlueprint(TestCase):

    LOGGING = 'True'
    def test_index(self):
        # Ensure Flask is setup.
        print("\n")
        self.assertEqual(True,True)

    def test_upload_one_image(self):
        url = "http://web:5000/v1/images/upload"
        payload = {"urls":
            [
                "https://farm3.staticflickr.com/2879/11234651086_681b3c2c00_b_d.jpg"
            ]
        }

        r = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload).content
        if(self.LOGGING == 'True'):
            print ("\nRESPONSE> " + str(json.loads(r)))
        jobId = json.loads(r)["jobId"]
        self.assertIsNotNone(jobId)

    def test_upload_multiple_images(self):
        url = "http://web:5000/v1/images/upload"
        payload = {"urls":
            [
                "https://farm3.staticflickr.com/2879/11234651086_681b3c2c00_b_d.jpg",
                "https://farm4.staticflickr.com/3790/11244125445_3c2f32cd83_k_d.jpg",
                "https://farm4.staticflickr.com/3790/11244125445_3c2f32cd83_k_d2.jpg"
            ]
        }

        r = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload).content
        if (self.LOGGING == 'True'):
            print ("\nRESPONSE> " + str(json.loads(r)))
        jobId = json.loads(r)["jobId"]
        self.assertIsNotNone(jobId)

    def test_submit_job_then_fetch_status_short_delay(self):
        url = "\nhttp://web:5000/v1/images/upload"
        payload = {"urls":
            [
                "https://farm3.staticflickr.com/2879/11234651086_681b3c2c00_b_d.jpg",
                "https://farm4.staticflickr.com/3790/11244125445_3c2f32cd83_k_d.jpg",
                "https://farm4.staticflickr.com/3790/11244125445_3c2f32cd83_k_d2.jpg"
            ]
        }

        r = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload).content
        jobId = json.loads(r)["jobId"]
        self.assertIsNotNone(jobId)
        time.sleep(0.5)

        url = "http://web:5000/v1/images/upload/" + jobId
        r = requests.get(url, headers={}).content
        if (self.LOGGING == 'True'):
            print ("RESPONSE> " + str(json.loads(r)))
        response = json.loads(r)
        self.assertIsNotNone(response)

    def test_submit_job_then_fetch_status_long_delay(self):
        url = "\nhttp://web:5000/v1/images/upload"
        payload = {"urls":
            [
                "https://farm3.staticflickr.com/2879/11234651086_681b3c2c00_b_d.jpg",
                "https://farm4.staticflickr.com/3790/11244125445_3c2f32cd83_k_d.jpg",
                "https://farm4.staticflickr.com/3790/11244125445_3c2f32cd83_k_d2.jpg"
            ]
        }

        r = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload).content
        jobId = json.loads(r)["jobId"]
        self.assertIsNotNone(jobId)
        time.sleep(5)

        url = "http://web:5000/v1/images/upload/" + jobId
        r = requests.get(url, headers={}).content
        if (self.LOGGING == 'True'):
            print ("RESPONSE> " + str(json.loads(r)))
        response = json.loads(r)
        self.assertIsNotNone(response)

    def test_fetch_all_uploaded_images(self):
        url = "http://web:5000/v1/images"
        r = requests.get(url, headers={}).content
        if (self.LOGGING == 'True'):
            print ("RESPONSE> " + str(json.loads(r)))
        response = json.loads(r)
        self.assertIsNotNone(response)



if __name__ == '__main__':
    unittest.main()
