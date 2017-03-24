from project import db
from project.models import User, Person, Company, Tag, Taggable

user1 = User('aricliesenfelt@gmail.com', 'Aric Liesenfelt', 'password1', '9515706209', True, True)
user2 = User('tommyhopkins@gmail.com', 'Tommy Hopkins', 'password2', '1111111111', True, True)

person1 = Person('Mark Zuckerberg', 'zuck@facebook.com', '4158675309', 'Facebook CEO')
person2 = Person('Larry Page', 'larry@gmail.com', '4448883923', 'Google CEO')

company1 = Company('Google')
company2 = Company('Facebook')
company3 = Company('Evernote')
company4 = Company('Pinterest')

tag1 = Tag('tech')
tag2 = Tag('san francisco')

taggable1 = Taggable(1,1,'company')
taggable2 = Taggable(2,1,'company')
taggable3 = Taggable(1,1,'person')
taggable4 = Taggable(2,1,'person')
taggable5 = Taggable(1,2,'company')
taggable6 = Taggable(2,2,'company')
taggable7 = Taggable(1,2,'person')
taggable8 = Taggable(2,2,'person')

db.session.add_all([user1, user2, person1, person2, company1, company2, company3, company4, tag1, tag2,
    taggable1, taggable2, taggable3, taggable4, taggable5, taggable6, taggable7, taggable8])
db.session.commit()

