import psycopg2
import redis
import json
import os
from bottle import Bottle, request

class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)
        redis_host = os.getenv('REDIS_HOST', 'queue')
        self.queue = redis.StrictRedis(host=redis_host, port=6379, db=0)
        db_host = os.getenv('DB_HOST', 'db')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'admin')
        db_name = os.getenv('DB_NAME', 'not_existent')
        dsn = f'dbname={db_name} user={db_user} password={db_password} host={db_host}'
        self.conn = psycopg2.connect(dsn)

    def register_message(self, subject, message):
        SQL = 'INSERT into emails(subject, message) VALUES(%s, %s)'

        cur = self.conn.cursor()
        cur.execute(SQL, (subject, message))
        self.conn.commit()
        cur.close()

        msg = {'subject': subject, 'message': message}
        self.queue.rpush('sender', json.dumps(msg))
        print('Message Successfully saved!')

    def send(self):
        subject = request.forms.get('subject')
        message = request.forms.get('message')
        self.register_message(subject, message)
        return 'Message successfully saved !'

if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)