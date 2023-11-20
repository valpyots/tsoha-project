CREATE TABLE categories (ID SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE messages (ID SERIAL PRIMARY KEY, content TEXT, user_id INTEGER REFERENCES users, sent_at TIMESTAMP, topic_id REFERENCES topics visible BOOLEAN);
CREATE TABLE users (ID SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, profilevisible BOOLEAN, canpost BOOLEAN, isAdmin BOOLEAN);
CREATE TABLE topics (ID SERIAL PRIMARY KEY message TEXT, title TEXT, user_id INTEGER REFERENCES users, sent_at TIMESTAMP, visible BOOLEAN, categoryid INTEGER  REFERENCES categories);

