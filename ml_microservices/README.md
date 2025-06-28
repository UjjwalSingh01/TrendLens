python -m venv venv

source venv/bin/activate
deactivate

pip install -r requirements.txt

python -m uvicorn main:app --reload