from model import db, User, Post, PostTag, Tag
from app import app



db.session.execute('DROP TABLE tags CASCADE')
db.session.execute('DROP TABLE posts_tags CASCADE')
db.session.execute('DROP TABLE users CASCADE')
db.session.execute('DROP TABLE posts CASCADE')
db.session.commit()

db.create_all()


user1 = User(first_name='Cassie', last_name='Gwapa')
user2 = User(first_name='Pebbles', last_name='Tabby')
user3 = User(first_name='Bambam', last_name='Squeak')

p1 = Post (title='First post', content='Bark bark', user_id=1)
p2 = Post (title='Test post', content='meow meow', user_id=2)
p3 = Post (title='Squeak', content='See a bird', user_id=3)

db.session.add_all([user1, user2, user3])
db.session.commit()
db.session.add_all([p1, p2, p3])
db.session.commit()