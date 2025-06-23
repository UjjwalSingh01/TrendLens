# Backend Api for Wkly.

## Setup Steps:
### Note :
Before Setting up backend code Create database 'wklyTest'

Add your local database url to .env file
```
DATABASE_URL=
```

1. Create virtual environment
```
python3 -m venv venv
```
2. virtual environment name:
venv
- To activate:
```
source venv/bin/activate
```

3. Install Requirements.txt 
```
pip install -r requirements.txt
```

4. To start server
```
uvicorn app.main:app --port 8002 --reload
```

