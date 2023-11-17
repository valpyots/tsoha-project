from app import app
from db import db
from sqlalchemy.sql import text
import users

def get_list():
    sql = text("SELECT T.title, T.message, U.username, T.sent_at, T.id FROM topics T, users U WHERE T.user_id=U.id AND T.visible = true ORDER BY T.id DESC")
    result = db.session.execute(sql)
    return result.fetchall()

def get_responses(topic_id):
    sql = text("SELECT M.content, U.username, M.sent_at FROM messages M, users U, Topics T WHERE M.user_id=U.id AND T.id = M.topic_id AND T.id = :topic_id AND M.visible = true ORDER BY M.id DESC")
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

#Function for posting a new topic
def newtopic(title, message):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO topics (title, message, user_id, sent_at, visible) VALUES (:title, :message, :user_id, NOW(), true)")
    db.session.execute(sql, {"title": title, "message": message, "user_id": user_id,})
    db.session.commit()
    return True

#Function for responding to an existing topic
def respond(content, topic_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO messages (content, user_id, sent_at, topic_id, visible) VALUES (:content, :user_id, NOW(), :topic_id, true)")
    db.session.execute(sql, {"content":content, "user_id":user_id, "topic_id":topic_id})
    db.session.commit()
    return True

def get_topic_id(topic_title):
    sql = text("SELECT T.id FROM Topic T WHERE T.title = :topic_title")
    res = db.session.execute(sql, {"topic_title":topic_title})

    return res.fetchone()

def get_topic_title(topic_id):
    sql = text("SELECT T.title FROM topics T WHERE T.id = :topic_id")
    res = db.session.execute(sql, {"topic_id":topic_id})
    return res.fetchone()

def get_topic_message(topic_id):
    sql = text("SELECT T.message FROM topics T WHERE T.id = :topic_id")
    res = db.session.execute(sql, {"topic_id":topic_id})
    return res.fetchone()

def hide_topic(topic_id):
    if topic_id == 0:
        return False
    else:
        sql = text("UPDATE topics SET visible = false WHERE topics.id = :topic_id")
        db.session.execute(sql, {"topic_id":topic_id})
        db.session.commit()
        return True
    
def get_topic_user(topic_id):
    sql = text("SELECT user_id FROM topics T WHERE T.id = :topic_id")
    res = db.session.execute(sql, {"topic_id":topic_id})
    return res.fetchone()