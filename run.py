from testapp import create_app,db
app=create_app()

#creating database to store data
with app.app_context():
        db.create_all()

#Running the testapp in debug mode
if __name__=='__main__':
        app.run(debug=True)