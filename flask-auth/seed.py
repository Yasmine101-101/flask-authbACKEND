#!/usr/bin/env python3

from app import create_app, db
from models import User, Note
from faker import Faker

app = create_app()
fake = Faker()

with app.app_context():

    # clear old data so re-seeding doesnt duplicate
    print("Clearing old data...")
    Note.query.delete()
    User.query.delete()
    db.session.commit()

    # create some users
    print("Seeding users...")
    user1 = User(username="yasmin")
    user1.password = "password123"

    user2 = User(username="john")
    user2.password = "password123"

    user3 = User(username="jane")
    user3.password = "password123"

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # create notes for each user using faker for realistic data
    print("Seeding notes...")
    for user in [user1, user2, user3]:
        for i in range(5):
            note = Note(
                title=fake.sentence(nb_words=4),
                content=fake.paragraph(nb_sentences=3),
                user_id=user.id
            )
            db.session.add(note)

    db.session.commit()
    print("Done seeding!")