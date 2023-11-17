CREATE TABLE categories (ID SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE messages (ID SERIAL PRIMARY KEY, content TEXT, user_id INTEGER REFERENCES users, sent_at TIMESTAMP, topic_id REFERENCES topics, category_id REFERENCES categories);
CREATE TABLE users (ID SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);
CREATE TABLE topics (ID SERIAL PRIMARY KEY, category INTEGER  REFERENCES categories, message TEXT, title TEXT, user_id INTEGER REFERENCES users, sent_at TIMESTAMP);

