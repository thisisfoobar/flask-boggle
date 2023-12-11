from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """set up before each test"""

        self.client = app.test_client()
        app.config['Testing'] = True

    def test_homepage(self):
        """Validate homepage resets session values for highscore and plays"""

        with self.client:
            response = self.client.get("/")
            self.assertEqual(session.get("highscore"),0)
            self.assertEqual(session.get("plays"),0)
            self.assertIn(b"<h1>Let's Play Boggle!</h1>", response.data)

    def test_reset_gameboard(self):
        """Validate gameboard reset"""
        
        with self.client:
            
            response = self.client.post("/reset-game")
            self.assertEqual(response.status_code,302)
            self.assertFalse(session.get("guesses"))
            self.assertEqual(response.location, "http://localhost/boggle-game")

    def follow_redirect(self):
        """Validate redirect from board reset"""
        with self.client:
            
            response = self.client.get("/reset-game", follow_redirect = True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b"<h3>High Score:",response.data)

    def test_valid_word(self):
        """Test if word is on board"""
        with self.client:
            with self.client.session_transaction() as sess:
                sess["board"] = [["D", "A", "R", "T", "Q"], 
                                ["D", "A", "R", "T", "Q"], 
                                ["D", "A", "R", "T", "Q"], 
                                ["D", "A", "R", "T", "Q"], 
                                ["D", "A", "R", "T", "Q"]]
                response = self.client.get("/check-word?word=hello")

    def test_invalid_word(self):
        """Test if word is not on board"""
        # self.client.get('/')
        # response = self.client.get('/check-word?word=howdy')
        # self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_english(self):
        """Test if word not in dict"""
        # self.client.get('/')
        # response = self.client.get('/check-word?word=notawordthatisvalid')
        # self.assertEqual(response.json['result'], 'not-a-word')
    

