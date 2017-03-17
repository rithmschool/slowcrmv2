from project import db
from project.models import User

user1 = User('aricliesenfelt@gmail.com', 'Aric Liesenfelt', 'password1', '9515706209', True, True)
user2 = User('tommyhopkins@gmail.com', 'Tommy Hopkins', 'password2', '1111111111', True, True)

db.session.add_all([user1, user2])
db.session.commit()

