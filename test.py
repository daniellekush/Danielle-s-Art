import os
import unittest
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models

class TestCase(unittest.TestCase):
  def setUp(self):
    app.config.from_object('config')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    self.app = app.test_client()
    db.create_all()
    pass

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  #1 - home route works
  def test_addHomeRoute(self):
    response = self.app.get('/', follow_redirects=True)
    self.assertEqual(response.status_code, 200)

  #11 - dc route works
  def test_addDCRoute(self):
    response = self.app.get('/dc', follow_redirects=True)
    self.assertEqual(response.status_code, 200)

  #12 - logos route works
  def test_addLogosRoute(self):
    response = self.app.get('/logos', follow_redirects=True)
    self.assertEqual(response.status_code, 200)

  #13 - signup route works
  def test_addSignUpRoute(self):
    response = self.app.get('/signup', follow_redirects=True)
    self.assertEqual(response.status_code, 200)

  #14 - login route works
  def test_addLoginRoute(self):
    response = self.app.get('/login', follow_redirects=True)
    self.assertEqual(response.status_code, 200)

  #15 - account route works
  def test_addAccountRoute(self):
    response = self.app.get('/account', follow_redirects=True)
    self.assertEqual(response.status_code, 200)

  #16 - logout route works
  def test_addLogOutRoute(self):
    response = self.app.get('/logout', follow_redirects=True)
    self.assertEqual(response.status_code, 200)

  #17 - suggestions route works
  def test_addSuggestionsRoute(self):
    response = self.app.get('/', follow_redirects=True)
    self.assertEqual(response.status_code, 200)

  #2 - valid user registration
  def test_valid_user(self):
    response = self.app.post('/signup', data=dict(username='new', password='account'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    html = response.get_data(as_text=True)
    assert 'Login' in html

  #3 - suggestions redirect
  def test_suggestions_redir(self):
    response = self.app.get('/suggestions', follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    html = response.get_data(as_text=True)
    assert 'Login' in html

  #4 - account redirect
  def test_account_redir(self):
    response = self.app.get('/account', follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    html = response.get_data(as_text=True)
    assert 'Login' in html

  #5 - login as a new user
  def test_register_login(self):
    response = self.app.post('/signup', data=dict(username='new', password='account'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    
    response = self.app.post('/login', data=dict(username='new', password='account'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    html = response.get_data(as_text=True)
    assert 'Home' in html

  #6 - incorrect password
  def test_incorrect_password(self):
    response = self.app.post('/signup', data=dict(username='new', password='account'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    response = self.app.post('/login', data=dict(username='new', password='new'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    html = response.get_data(as_text=True)
    assert 'Incorrect password.' in html
    
  #7 - non unique username
  def test_username_exists(self):
    response = self.app.post('/signup', data=dict(username='new', password='account'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    response = self.app.post('/signup', data=dict(username='new', password='account'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    html = response.get_data(as_text=True)
    assert 'This username already exists.' in html

  #8 - create new suggestion
  def test_new_suggestion(self):
    response = self.app.post('/signup', data=dict(username='new', password='account'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    
    response = self.app.post('/login', data=dict(username='new', password='account'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)

    response = self.app.post('/suggestions', data=dict(sType='Other', title='Test', desc='Testing a new suggestion'), follow_redirects=True)
    html = response.get_data(as_text=True)
    assert 'No suggestions to display.' not in html
    
  #9 - suggestions as logged user
  def test_enter_suggestions(self):
    response = self.app.post('/signup', data=dict(username='new', password='account'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    
    response = self.app.post('/login', data=dict(username='new', password='account'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)

    response = self.app.get('/suggestions', follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    html = response.get_data(as_text=True)
    assert 'Suggestions' in html

  #10 - account as logged user
  def test_enter_account(self):
    response = self.app.post('/signup', data=dict(username='new', password='account'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    
    response = self.app.post('/login', data=dict(username='new', password='account'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)

    response = self.app.get('/account', follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    html = response.get_data(as_text=True)
    assert 'Account' in html

  #18 - username doesn't exist
  def test_no_user_login(self):
    response = self.app.post('/login', data=dict(username='new', password='account'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    html = response.get_data(as_text=True)
    assert 'This user does not exist.' in html

if __name__ == '__main__':
  unittest.main()
