Installation Steps
1. Node.js
   a. To download the Node.js, https://nodejs.org/en
   b. Check node.js version in command prompt, use command 'npm -v'.
2. Python 
   a. To download python, https://www.python.org/downloads/
   b. Check python version in command prompt, use command 'python3 --version'.
3. Python's package installer (pip)
   a. To check pip installation, use command 'pip -V'.
4. FastAPI
   a. To download FastAPI, use command 'pip install fastapi uvicorn'.
5. MongoDB
    a. To install mongoDB, https://www.mongodb.com/try/download/shell
    b. Manual of mongoDB, https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/
    c. To download mongoDB Compass (GUI), https://www.mongodb.com/try/download/compass


Database preparation:
1. Run MongoDB Compass
2. Connect to mongoDB deployment:
    a. Click 'connect' with default URI: mongodb://localhost:27017
    b. Create a new database and rename it as 'MES' 
    c. Create a collections which name as 'production_record'
    d. The name of database and collections must be the same mentioned above.
    e. For the collection, import the JSON data from '/mes/MES.{production_record}' directory


To run the application successfully:
1. Download and unzip the whole mes folder.
2. Open a new terminal.
3. Direct to the path 'path_to_the_folder/mes/vue'.
4. Run 'npm install' command and it will start downloading necessary package.
5. Run ' npm run serve' command and click on the link to launch the frontend of the application.
6. Open another new terminal.
7. Direct to the path 'path_to_the_folder/mes/python/app'.
8. Run 'uvicorn app.api:app --reload' command to lauch the backend of the application.
9. Now, you should be able to see a website that is connected to an API open in your browser.