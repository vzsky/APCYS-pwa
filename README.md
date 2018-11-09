# APCYS Progressive web application developing repo.

- ## Setting up
  1. Setting up working virtual environment (python 3) 
  ```
  mkvirtualenv venv
  ```
  2. Work on the environment 
  ```
  workon venv
  ```
  3. Install all the requirements 
  ```
  pip install -r req.txt
  ```
  4. Configure the settings

  5. Run the program on the server 
  ``` 
  python app.py
  ```
  the program should be opened on 0.0.0.0:7000

- ## Configuration

  Edit following lines 
  ```
  app.config['SECRET_KEY'] = 'secret'
  app.config['MYSQL_DATABASE_USER'] = 'root'
  app.config['MYSQL_DATABASE_PASSWORD'] = ''
  app.config['MYSQL_DATABASE_DB'] = 'APCYS'
  app.config['MYSQL_DATABASE_HOST'] = '10.205.240.11'

  port = 7000x
```
To match the mysql server config. and port