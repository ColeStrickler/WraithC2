from wraithc2 import app

# create database
# 1. python
# 2. from wraithc2 import db
# 3. db.create_all()
# must rebuild database every time a new table is added


if __name__ == "__main__":
    app.run(port=5000, debug=True)