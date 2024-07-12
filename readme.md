
# Dj Mango Awards - Mango D'or

Project aiming to vote for people to win the Mango D'or.


## Installation & Initialization
In order to run the server, you will need python and NodeJS to be installed in your system.

Clone the repo:
```
git clone https://github.com/javierlnmn/mango-dor.git
```

Navigate into the project folder and create a python virtualenv there:
```
cd mango-dor
python -m venv .env
```

Activate the virtualenv:
```
.env\Scripts\activate (Windows)
or
source ./.env/bin/activate (Linux / MacOS)
```

Once activated, install the requirements in the python virtualenv:
```
pip install -r requirements.txt
```

Navigate into the `/theme/static_src` directory. Then, install the Node modules:

```
npm install
```

Once everything is installed, to run the project you will need to run the server and also tailwind build (in two separated terminals):
```
python manage.py tailwind start
```
```
python manage.py runserver
```