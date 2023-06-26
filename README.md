# Echo service
CRUD operations are supported in echo service which creates mock endpoints

1. Each request is validated using the pydantic models
2. On being valid data is passed on to the database.
3. Database for local is sqlite but also, supports AWS based postgres DB.
4. IAAC is terraform whose files are included in .tf folder.


# Steps to execute -
1. Create a virtual env with command -> python3 -m venv venv
2. Activate the virtual env with comand  -> source venv/bin/activate
3. Install the libraries with command -> pip install -r requirements.txt
4. If planning to use with local SQLlite db then no changes required goto
step 11
5. If planning to use AWS postgres db then follow steps 6-10
6. Goto .tf folder and hit terraform init after adding AWS keys
7. Type the command terraform apply
8. Hit Yes when asked to authorize
9. Take the endpoint shown on the console and change POSTGRES_DATABASE_URL
in settings.py
10. Change DATABASE_LOCAL in settings.py to False
11. Run with command -> uvicorn main:app --reload
12. Now hit the API you should be able to use it
