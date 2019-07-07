import pymysql
from flask import Flask
app=Flask(__name__)
try:
    db=pymysql.connect("localhost","root","Sunny#2002@","food");
    c=db.cursor();
    print("data base created successfully");
    db.close();
except:
    print("error in database connection")
if __name__=="__main__":
    
    app.run(debug=True)
