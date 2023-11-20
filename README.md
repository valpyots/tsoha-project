# message-board-application
A simple flask web application that functions as a message board. This application is my course project for "Tietokannat ja web-ohjelmointi 2023, II periodi"

Note that this application is currently not deployed anywhere. To test it:

 - Clone this repositary locally
 - Create ".env" file at the project root
 - In ".env", set DATABASE_URL=<your-psql-database-goes-here> and SECRET_KEY=<your-secret-key-goes-here>
 - Activate virtual environment and install dependencies with the following commands:
	
	$ python3 -m venv venv
	
	$ source venv/bin/activate
	
	$ pip install -r ./requirements.txt
 - Set database schema with
	
	$ psql < schema.sql
- After the previous steps, you should be able to run the application locally with
	
	$ flask run

The application currently allows an user to:

- post a new topic

- respond to existing topics

- choose a category for their post

- view their own posts on their profile

- allow others to view other user's profiles and their posts , if set to public

- browse all posts, browse post by category

The application also supports admin users, who can:

- delete any post or message

- view all profiles, even those set to private

Features that I still plan to implement:

- for admin accounts:

	- block an user from posting

- sorting posts by date or comment amount, both ascending and descending

- profile bios to describe user

- editing own user data (ie. change password, bio, profile visibility)

- better user interface

- in-app admin creation (currently admin users can only be created from the database)
