import unittest
from MDS import app
import json
import sqlite3
import os

DB_FILE = "database/test_MDS.db" 

class UnitTestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            with open("database/create_db.sql") as f:
                sql = f.read()
                cur.executescript(sql)

    @classmethod
    def tearDownClass(cls):
        os.remove(DB_FILE)

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.DB_FILE = DB_FILE
        with sqlite3.connect(self.DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute("insert into packages ('id','destination_address','destination_city') values ('test_id','test_address','test_city')")

    def tearDown(self):
        with sqlite3.connect(self.DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute("delete from packages where id='test_id'")

    def test_1_create(self):
        response = self.app.post('/create', 
           data=json.dumps(dict(destination_address='test_address', destination_city="test_city")),
           content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_2_update(self):
        response = self.app.put('/update', 
           data=json.dumps(dict(package_id="test_id", transit_city="test_city1")),
           content_type='application/json')
        print(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    def test_3_check_progress(self):
        response = self.app.get('/check_progress',
            data=json.dumps(dict(package_id="test_id")),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_4_mark_delivered(self):
        response = self.app.put('/mark_delivered',
            data=json.dumps(dict(package_id="test_id")),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

