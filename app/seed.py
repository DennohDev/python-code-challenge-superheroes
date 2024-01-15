from app import db, app
from models import Hero, Power, HeroPower
from random import randint, choice

# Seeding powers
with app.app_context():
    powers_data = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
    {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
    {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]

    powers = [Power(**data) for data in powers_data]
    db.session.bulk_save_objects(powers)
    db.session.commit()

    # Seeding heroes
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]

    heroes = [Hero(**data) for data in heroes_data]
    db.session.bulk_save_objects(heroes)
    db.session.commit()

    # Adding powers to heroes
    strengths = ["Strong", "Weak", "Average"]
    for hero in Hero.query.all():
        for _ in range(randint(1, 3)):
            # get a random power
            power = Power.query.order_by(db.func.random()).first()

            # Instantiate HeroPower
            hero_power = HeroPower(hero=hero, power=power, strength=choice(strengths))

            # Add HeroPower to the session
            db.session.add(hero_power)

    # Commit the changes
    db.session.commit()

    print("🦸‍♀️ Done seeding!")

