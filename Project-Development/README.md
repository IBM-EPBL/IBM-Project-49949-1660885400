# AI-powered Nutrition Analyzer for Fitness Enthusiasts - Development procedure

Make sure you are inside the Flask folder of any sprint

Create `.flaskenv` file and add the following

```
FLASK_APP=app
FLASK_DEBUG=True
FLASK_RUN_PORT=8080
```

Now create a .env file and add the following

```
DEBUG=True
```

Create a virtual environment and activate it by (for linux)

```
python3 -m ven venv
source venv/bin/activate
```

for windows :(

```
python -m venv venv
./venv/Scripts/activate.bat
```

Install all the dependencies by <br />(replace pip3 with pip for windows)

```
pip3 install -r requirements.txt
```

Now just run the `run.py` file using python
<br /> (omit the 3 for windows)

```
python3 run.py
```

Visit [http://localhost:8080](http://localhost:8080) to see the magic !!
