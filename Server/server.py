from flask import Flask, request,jsonify
from sqlalchemy import Column, Integer, Text, Float, DateTime, create_engine, desc
from sqlalchemy.orm import scoped_session, sessionmaker, load_only
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from flask_restful import Resource, Api
from dataclasses import dataclass
import json
from flask_cors import CORS, cross_origin
import requests
import random


Base = declarative_base()  
metadata = Base.metadata
engine = create_engine('mysql+pymysql://root:@localhost/quizshow') #mysql
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property()

app = Flask(__name__) 
cors = CORS(app) 
api = Api(app)
base_url = "https://the-trivia-api.com/api"

class OnlineQuiz(Resource): 
    def get(self, cat, diff):
        url = base_url + "/questions?limit=1&difficulty=%s&categories=%s" %(diff,cat)
        res = requests.get(url).json()
        answers = [res[0]["correctAnswer"], res[0]["incorrectAnswers"][0], res[0]["incorrectAnswers"][1], res[0]["incorrectAnswers"][2]]
        random.shuffle(answers)
        return jsonify({"id":res[0]["id"], "answers":answers, "question": res[0]["question"]})
    
    @app.route('/getData')
    def getData():
        url = base_url + "/metadata"
        res = requests.get(url).json()
        return jsonify({"Category":res["byCategory"], "Difficulty":res["byDifficulty"]})
    
    @app.route('/getCorrect/<id>')
    def getCorrect(id):
        url = base_url + "/question/%s" %id
        res = requests.get(url).json()
        return res["correctAnswer"]
        

api.add_resource(OnlineQuiz, '/getQuestion/<diff>/<cat>')

@dataclass
class User(Base):
    __tablename__='user'
    username: str
    pwd: str
    highscore: str
    
    username = Column(Text, primary_key=True)
    pwd = Column(Text)
    highscore = Column(Integer)

class UserManagement(Resource):
    def put(self):
        data = request.get_json(force=True)["params"]
        if self.verify(data["username"]):
            return False
        info = User(username=data["username"], pwd=data["pwd"], highscore=0)
        db_session.add(info)
        db_session.flush()
        return True
    def get(self):
        data = request.get_json(force=True)["params"]
        info = User.query.get(data["username"])
        return jsonify(info)
    
    def verify(self, username):
        info = User.query.get(username)
        if info == None:
            return False
        return True
    
    @app.route('/userManagement/login', methods=['PUT'])
    def login():
        data = request.get_json(force=True)["params"]
        info = User.query.get(data["username"])
        if info == None:
            return jsonify(False)
        if info.pwd == data["pwd"]:
            return jsonify(True)
    
    @app.route('/userManagement/updateHighscore', methods=['PUT'])
    def updateHighscore():
        data = request.get_json(force=True)["params"]
        print(data["username"],data["highscore"])
        info = User.query.get(data["username"])
        print(info)
        if info == None:
            return jsonify(False)
        if info.highscore > data["highscore"]:
            return jsonify(True)
        info.highscore = data["highscore"]
        db_session.add(info)
        db_session.flush()
        return jsonify(True)
    
    @app.route('/userManagement/leaderboard', methods=['GET'])
    def getLeaderBoard():
        info = User.query.order_by(desc(User.highscore)).all()
        res = []
        for i,e in enumerate(info):
            res.append({"username":e.username, "highscore":e.highscore})
        return jsonify(res)
        

api.add_resource(UserManagement, '/userManagement')
        


@app.teardown_appcontext
def shutdown_session(exception=None):
    print("Shutdown Session")
    #db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)