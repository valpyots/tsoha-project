from app import app
from db import db
from sqlalchemy.sql import text
import users

#Function returns all topics
def get_topic_list():
    sql = text("SELECT T.title, T.message, U.username, T.sent_at, T.id, U.id, C.name FROM topics T, users U, categories C WHERE T.user_id=U.id AND T.visible = true AND T.categoryid = C.id ORDER BY T.id DESC")
    res = db.session.execute(sql).fetchall()
    return res

#Function returns all responses to a given topic by topic id
def get_responses(topic_id):
    sql = text("SELECT M.content, U.username, M.sent_at, M.user_id FROM messages M, users U, Topics T WHERE M.user_id=U.id AND T.id = M.topic_id AND T.id = :topic_id AND M.visible = true ORDER BY M.id DESC")
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

#Function for posting a new topic
def newtopic(title, message, categoryname):
    if check_category(categoryname) == False:
        categoryid = create_category(categoryname)
    else:
        categoryid = get_category_id(categoryname)
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO topics (title, message, user_id, sent_at, visible, categoryid) VALUES (:title, :message, :user_id, NOW(), true, :categoryid)")
    db.session.execute(sql, {"title": title, "message": message, "user_id": user_id, "categoryid": categoryid})
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

#Function returns topic id for a given topic by title
def get_topic_id(topic_title):
    sql = text("SELECT T.id FROM Topic T WHERE T.title = :topic_title")
    res = db.session.execute(sql, {"topic_title":topic_title})
    return res.fetchone()

#Function returns topic title for a given topic by id
def get_topic_title(topic_id):
    sql = text("SELECT T.title FROM topics T WHERE T.id = :topic_id")
    res = db.session.execute(sql, {"topic_id":topic_id})
    return res.fetchone()

#Function returns responses to a given topic by topic id
def get_topic_message(topic_id):
    sql = text("SELECT T.message FROM topics T WHERE T.id = :topic_id")
    res = db.session.execute(sql, {"topic_id":topic_id})
    return res.fetchone()

#Function to allow topic deletion by changing database value "visibile" to false
def hide_topic(topic_id):
    if topic_id == 0:
        return False
    else:
        sql = text("UPDATE topics SET visible = false WHERE topics.id = :topic_id")
        db.session.execute(sql, {"topic_id":topic_id})
        db.session.commit()
        return True

#Function returns user id for user who posted the topic by topic id
def get_topic_user(topic_id):
    sql = text("SELECT T.user_id, U.username FROM topics T, Users U WHERE T.id = :topic_id AND T.user_id = U.id")
    res = db.session.execute(sql, {"topic_id":topic_id})
    return res.fetchall()

#Function to create category
def create_category(catname):
    sql = text("INSERT INTO categories (name) VALUES (:catname)")
    db.session.execute(sql, {"catname":catname})
    db.session.commit()
    sql = text("SELECT C.id FROM categories C WHERE c.name = :catname")
    res = db.session.execute(sql, {"catname": catname}).fetchone()
    return res[0]

#Function to return category id by category name
def get_category_id(catname):
    sql = text("SELECT C.id FROM categories C WHERE C.name = :catname")
    res = db.session.execute(sql, {"catname":catname})
    return res.fetchone()[0]

#Function to check if category already exists
def check_category(catname):
    sql = text("SELECT C.name FROM categories C WHERE C.name = :catname")
    res = db.session.execute(sql, {"catname":catname}).fetchall()
    if len(res) > 0:
        return True
    else:
        return False
    
#Function to return topic category
def get_topic_category(topic_id):
    sql = text("SELECT T.categoryid FROM Topics T WHERE T.id = :topic_id")
    res = db.session.execute(sql, {"topic_id":topic_id}).fetchone()
    return res[0]

def get_category_name(catid):
    sql = text("SELECT C.name FROM categories C WHERE C.id = :catid")
    res = db.session.execute(sql, {"catid":catid})
    return res.fetchone()[0]