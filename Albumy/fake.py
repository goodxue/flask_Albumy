from faker import Faker

from Albumy.extensions import db
from Albumy.models import User

fake = Faker()

def fake_user(count=10):
    for i in range(count):
        user = User(name=fake.name(),
                    confirmed=True,
                    username=fake.user_name(),
                    bio=fake.sentence(),
                    location=fake.city(),
                    website=fake.url(),
                    member_since=fake.date_this_decade(),
                    email=fake.email())
        user.set_password('123456')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()