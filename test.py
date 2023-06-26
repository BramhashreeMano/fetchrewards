import requests
import json
from uuid import UUID

from unittest import TestCase


class Case1Test(TestCase):

    def test_points_calculation(self):
        post_data = {
          "retailer": "Target",
          "purchaseDate": "2022-01-01",
          "purchaseTime": "13:01",
          "items": [
            {
              "shortDescription": "Mountain Dew 12PK",
              "price": "6.49"
            },{
              "shortDescription": "Emils Cheese Pizza",
              "price": "12.25"
            },{
              "shortDescription": "Knorr Creamy Chicken",
              "price": "1.26"
            },{
              "shortDescription": "Doritos Nacho Cheese",
              "price": "3.35"
            },{
              "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
              "price": "12.00"
            }
          ],
          "total": "35.35"
        }
        response = requests.post(
            'http://localhost:8080/receipts/process',
            data=json.dumps(post_data),
            headers={
                'Content-type': 'application/json'
            }
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UUID(data['id']))
        generated_id = data['id']

        points_data = requests.get('http://localhost:8080/receipts/{}/points'.format(generated_id))
        self.assertEqual(points_data.status_code, 200)
        point_info = points_data.json()
        self.assertTrue(point_info['points'])
        self.assertEquals(point_info['points'], 28)

class Case2Test(TestCase):
    
    def test_points_calculation(self):
        post_data = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
              {
                "shortDescription": "Gatorade",
                "price": "2.25"
             },{
                "shortDescription": "Gatorade",
               "price": "2.25"
             },{
               "shortDescription": "Gatorade",
               "price": "2.25"
             },{
               "shortDescription": "Gatorade",
               "price": "2.25"
              }
           ],
           "total": "9.00"
         }
        response = requests.post(
          'http://localhost:8080/receipts/process',
           data=json.dumps(post_data),
           headers={
              'Content-type': 'application/json'
            }
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UUID(data['id']))
        generated_id = data['id']

        points_data = requests.get('http://localhost:8080/receipts/{}/points'.format(generated_id))
        self.assertEqual(points_data.status_code, 200)
        point_info = points_data.json()
        self.assertTrue(point_info['points'])
        self.assertEquals(point_info['points'], 109)
