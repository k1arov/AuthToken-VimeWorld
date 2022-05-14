from flask import Flask, jsonify, redirect, request, session
import uuid
import requests
from app import sql

class User:

  def start_session(self, user):
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signup(self):
    print(request.form)

    data = requests.get(f"https://api.vimeworld.com/misc/token/{request.form.get('token')}").json()
    try:
      nickname = data['owner']['username']
      if sql.count_documents({"username": nickname}) == 0:
        user = {
          "_id": uuid.uuid4().hex,
          "username": nickname,
          "rating": 1000,
          "admin": False
        }
        if sql.insert_one(user):
          return self.start_session(user)
      else:
        return jsonify({"error": "Аккаунт находится в базе данных"}), 400
    except KeyError:
      return jsonify({"error": "Токен недействительный"}), 400

  def signout(self):
    session.clear()
    return redirect('/')

  def login(self):

    data = requests.get(f"https://api.vimeworld.com/misc/token/{request.form.get('token')}").json()
    nickname = data['owner']['username']

    user = sql.find_one({
      "username": nickname
    })

    if user:
      return self.start_session(user)

    return jsonify({"error": "Invalid token lol"}), 401
