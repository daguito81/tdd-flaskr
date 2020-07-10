# create_db.py

from app import db

# Create the db and tables
db.create_all()

# Commit the changes
db.session.commit()
