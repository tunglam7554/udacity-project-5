import unittest
from flask import Flask
import unittest
from models import setup_db, db
import json
from app import create_app

class CapstoneTestCase(unittest.TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        setup_db(app)
        return app

    def setUp(self):
        self.app = create_app(is_drop=True)
        self.client = self.app.test_client
        self.new_movie = {
            'title': 'New Movie',
            'release_date': '2024-01-01'
        }
        self.new_actor = {
            'name': 'New Actor',
            'age': 30,
            'gender': 'Male'
        }
        with open('token_test.json', 'r') as f:
            self.token = json.load(f)

        self.casting_assistant = {
            "Authorization": f'Bearer {self.token["casting_assistant"]}'
        }
        self.casting_director = {
            "Authorization": f'Bearer {self.token["casting_director"]}'
        }
        self.executive_producer = {
            "Authorization": f'Bearer {self.token["executive_producer"]}'
        }

    def tearDown(self):
        """Executed after each test"""
        db.session.remove()
        pass

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])      
        self.assertIn('movies', data)

    def test_get_movies_error(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertIn('movie', data)

    def test_create_movie_error(self):
        res = self.client().post('/movies', json={}, headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_create_movie_error_403(self):
        res = self.client().post('/movies', json={}, headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_update_movie(self):
        res = self.client().patch('/movies/1', json={'title': 'Updated Movie'}, headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('movie', data)

    def test_update_movie_error(self):
        res = self.client().patch('/movies/999', json={'title': 'Updated Movie'}, headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_update_movie_error_403(self):
        res = self.client().patch('/movies/1', json={'title': 'Updated Movie'}, headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('message', data)
        self.assertTrue(data['success'])

    def test_delete_movie_error(self):
        res = self.client().delete('/movies/999', headers=self.executive_producer)
        data = json.loads(res.data)      
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_movie_error_403(self):
        res = self.client().delete('/movies/1', headers=self.casting_assistant)
        data = json.loads(res.data)     
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.casting_assistant)
        self.assertEqual(res.status_code, 200)
        self.assertIn('actors', json.loads(res.data))

    def test_get_actors_error(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_create_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertIn('actor', data)

    def test_create_actor_error(self):
        res = self.client().post('/actors', json={}, headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_create_actor_error_403(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_update_actor(self):
        res = self.client().patch('/actors/1', json={'name': 'Updated Actor'}, headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('actor', data)

    def test_update_actor_error(self):
        res = self.client().patch('/actors/999', json={'name': 'Updated Actor'}, headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_update_actor_error_403(self):
        res = self.client().patch('/actors/1', json={'name': 'Updated Actor'}, headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('message', data)

    def test_delete_actor_error(self):
        res = self.client().delete('/actors/999', headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_actor_error_403(self):
        res = self.client().delete('/actors/1', headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        
if __name__ == "__main__":
    unittest.main()
