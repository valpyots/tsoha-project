from app import app
from db import db
from sqlalchemy.sql import text
import users

def get_list():
    sql = text("SELECT T.title, T.message, U.username, T.sent_at FROM topics T, users U WHERE T.user_id=U.id ORDER BY T.id DESC")
    result = db.session.execute(sql)
    return result.fetchall()

#Function for posting a new topic
def newtopic(title, message):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO topics (title, message, user_id, sent_at) VALUES (:title, :message, :user_id, NOW())")
    db.session.execute(sql, {"title": title, "message": message, "user_id": user_id,})
    db.session.commit()
    return True

#Function for responding to an existing topic
def respond(content, topic_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO messages (content, user_id, sent_at, topic_id) VALUES (:content, :user_id, NOW(), :topic_id)")
    db.session.execute(sql, {"content":content, "user_id":user_id, "topic_id":topic_id})
    db.session.commit()
    return True
