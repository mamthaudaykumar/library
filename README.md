**NOTES**
1. Api spec added to library -> app -> resources -> api_spec.yaml. Please use https://editor.swagger.io/ to view the apis

**Server Start-Up Guide**
1. Pre-Requisites: python, pip
2. In pycharm terminal -> open .venv
2. Run the command to install the libraries for app startup **pip install -r requirements.txt**
3. Once installation successful, run command **uvicorn main:app --reload --port 8080**
4. Once eerver succesfully started can view swagger on url http://127.0.0.1:8080/docs#/


**What all Covered in the service:**
1. Microservice written using fast-api framework
2. Basic CRUD
2. seed-data on startup
3. async notification
4. Basic search api
5. Wishlist
6. Book status change
7. 1 test - pytest - just for sample
8. Added migartion - just for sample
9. NOT DONE - Linting
10. NOT DONE - mock/monkey patch testing
11. NOT DONE - Logging - but it can be any log handler of our interest


**Migration: Added just for sample**

sqlalchemy.url = sqlite:///./test.db
- alembic init alembic
- alembic revision --autogenerate -m "Create books tables"
- alembic upgrade head
