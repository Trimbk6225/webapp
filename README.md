# webapp
I use Flask to build web app or API
I create virtual environment (Terminal command :- python -m venv venv)
To activate it   (Terminal command :- source venv/bin/activate) 
Requirements is needed to be installed to run the application (Terminal command :- pip install -r requirements.txt)
Requirements test include:{
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.1.0
PyMySQL
python-dotenv==1.0.1
cryptography  
}
For database conectivity I use MySql 
before running the app i have to run some commands so the the database will connect properly
Terminal commands :- {
    flask db init
    flask db migrate
    flask db upgrade
}
There is also .env file in which the some credential are required to connet database are mentioned in this file.
so, this file will locally pasted or made at that time  will running the app.

for Assignment 2
 I need 6$ plan of digital occean 
 commands to run the applications 
 ubuntu
 ssh root@IPADRESS
 after local terminal send the file:-
  cd ..
  cd home
  chmod +x setup.sh
  ./setup.sh

  local terminal :-
  scp ~/folderpathforzipfile root@IPADRESSS:/home/
  scp ~/folderpathfor.shfile root@IPADRESSS:/home/

  For assignmrnt 3 :- 
  I created the workflow
 Assignment 4
 for aws first expor aws:-
 export AWS_PROFILE=dev

 for gcp:-

 



