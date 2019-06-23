# Webotics Project (3-in-1)

## What is webotics? 
A chrome extension that aims to increase marketers' lead generation.
The idea is to create a chrome extension that will trigger a pop up to appear at the side of the screen when certain keywords are recognised. 

## This project consists of 3 different parts:
1. webscraper
2. spacy
3. chrome extension

This project does not require any database to work.

## Installation Steps:
Run: 
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm 

If you’re having trouble installing dependencies due to:
    mkl-fft==1.0.6, or
    mkl-random==1.0.1,
    certifi==2018.11.29
Run:
    conda install -c conda-forge mkl_fft==1.0.6
    conda install -c conda-forge mkl_random==1.0.1
    conda install -c conda-forge certifi==2018.11.29

### 2. NLP with spaCy
This project utilises spaCy NLP’s pre-trained model (en_core_web_sm), updated with additional training on our side on the Named Entity Recognizer(NER) for machine learning. For more in depth understanding on spaCy, please refer to https://spacy.io/usage/spacy-101 :)

Kindly refer to \webotics\NLP\server.py  for codes regarding training of NER. 

To note:
For convenience of training multiple models without the need to change our model names in various location throughout the code, we utilised the usage of  os.path. This comes with a pitfall of needing to remove “NLP” from code line 10 in server.py everytime we run server.py:

from NLP.training_data2 import TRAIN_DATA => from training_data2 import TRAIN_DATA. 

Remember to add it back again after training of model is complete. 

For Windows users, upon git pushing the trained models, you might run into “TypeError: unhashable type: 'list'” . Apparently it is a problem with the serialization of the tokenizer on Windows. 

To make the model shareable with others, we recommend uploading the model in cloud (we used google drive :) ) 

Reference on the issue:  https://github.com/explosion/spaCy/issues/1634

phrase_matcher.py is used to generate the ent.start_char and ent.end_char for our training datasets. Due to time constraints, we hardcoded the terminology_list for our training datasets as spaCy’s pre-trained vector model is still a far cry from our ideal. 

During our training of spaCy model, sometimes CLI training stops before it finished all iterations. We have yet to find a fix for that issue, but we managed to train our model after several attempts of running the code. 

Reference for some debugging strategies:  https://github.com/explosion/spaCy/issues/2511 

### 3. Chrome Extension (This does not work under other browsers)
1. Click on the options menu at the top-right of the Chrome browser
2. Hover over `More tools` and click on `Extensions`
3. At the top-right of the browser, toggle the `Developer Mode` from OFF to ON
4. A new row of options will appear, click on `Load unpacked` and navigate under `webotics > chrome_extension`
5. Select the main folder by itself and chrome will install it based on the `manifest.json`

## Overall idea on how the Chrome Extension works
1. `manifest.json` file will contain the default settings for the extension
2. `manifest.json > browser_action` will be the visual representation of the project
3. `popup: html and js` will be the visual aspect of the chrome extension when clicked on
4. `manifest.json > content_scripts` will be specifying the condition to perform when user is viewing a webpage
5. `scripts.js` will be the process that is running based on `4` above

- Remove `certifi==2018.11.29` from requirements.txt

If you're having trouble starting flask

- Restart your terminal as well and reactivate conda source

**Create a `.env` file at the root of the directory**

This project uses `python-dotenv`. When running commands using `flask`, environment variables from `.env` are automatically loaded.

When executing `python` scripts directly e.g. `python start.py`, environment variables are not loaded and will not work except `python migrate.py` _(read the script - `migrate.py` to know why it would load the environment variables `.env`)_

Minimum environment variables that needs to be set

```
FLASK_APP='start' # based on the name of our entry point script
FLASK_ENV='development' # use this in development, otherwise 'production' or 'test'
DATABASE_URL="postgres://localhost:5432/nextagram_dev"
SECRET_KEY= #generate your own key
```

Use `os.urandom(32)` to generate a random secret key and paste that in `.env`. It's important to keep this `SECRET_KEY` private.

Since this app uses Pooled Connections, you may also want to set:

```
DB_TIMEOUT=300 # 5 minutes
DB_POOL=5
```

_(see `database.py`)_

**Create a Database**

- this application is configured to use Postgresql

```
createdb nextagram_dev
```

_\*if you name your database something else, tweak the settings in `.env`_

**Ignoring Files from Git**

Before git commiting, remember to ignore key files. Here's an example of `.gitignore`

```
.vscode
*.DS_Store
*__pycache__
*.env
```

---

## Database Migrations

```
python migrate.py
```

\*_this template is configured to use Peewee's PooledConnection, however, migrations using Peewee-DB-Evolve doesn't work well. A hack was used to not use PooledConnection when running migration. Pending investigation. There are no known side effects to run this template in production._

## Starting Server

```
flask run
```

## Starting Shell

```
flask shell
```

---

## Deploying to Production

- ensure environment variables are configured appropriately
- migrations will not run in interactive mode when FLASK_ENV is set to 'production'
- It's important to set your own `SECRET_KEY` environment variable and keep that private.

---

## Architecture

This template separates out API and Web to separate packages. Both API and Web are configured to use Flask's Blueprints.

All new models should go into it's own file/script within the models directory.

The entry point for a Flask server to start is located at `start.py`

---

## Dependencies

This template was created against `Python 3.7`. Should work with newer versions of Python. Not tested with older versions.

`Peewee` is used as ORM along with a database migration library `peewee-db-evolve`.
