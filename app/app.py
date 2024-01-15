from flask import Flask, jsonify, make_response, request, abort
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Routes

# Validation Functions
def validate_strength(strength):
    valid_strengths = ['Strong', 'Weak', 'Average']
    return strength in valid_strengths

def validate_description(description):
    return len(description) >= 20

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_list)

# GET /heroes/:id
from flask import jsonify

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': hero_power.power.id, 'name': hero_power.power.name, 'description': hero_power.power.description, 'strength': hero_power.strength} for hero_power in hero.powers]
        }
        return jsonify(hero_data)
    else:
        return jsonify({'error': 'Hero not found'}), 404

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_list)

# GET /powers/:id
@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)
    if power:
        power_data = {'id': power.id, 'name': power.name, 'description': power.description}
        return jsonify(power_data)
    else:
        return jsonify({'error': 'Power not found'}), 404

# PATCH /powers/:id
@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if power:
        try:
            data = request.get_json()
            if 'description' in data and validate_description(data['description']):
                power.description = data['description']
                db.session.commit()
                return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
            else:
                return jsonify({'errors': ['Validation errors']}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Power not updated successfully'}), 500
    else:
        return jsonify({'error': 'Power not found'}), 404

# POST /hero_powers

@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    try:
        # validate if strength is in the given strengths
        strength = request.form.get("strength")
        if strength not in ["Strong", "Weak", "Average"]:
            return make_response(jsonify({"errors": ["validation errors"]}), 400)

        # parse power_id and hero_id as integers
        power_id = int(request.form.get("power_id"))
        hero_id = int(request.form.get("hero_id"))

        # query the database to make sure power and hero exist
        power = Power.query.get(power_id)
        hero = Hero.query.get(hero_id)

        if power is None or hero is None:
            return make_response(jsonify({"errors": ["Invalid Power or Hero ID"]}), 400)

        # create a new HeroPower relationship
        new_hero_power = HeroPower(strength=strength, power=power, hero=hero)
        db.session.add(new_hero_power)
        db.session.commit()

        # query the updated Hero
        updated_hero = Hero.query.get(hero_id)

        response_data = {
            "id": updated_hero.id,
            "name": updated_hero.name,
            "super_name": updated_hero.super_name,
            "powers": [power.to_dict() for power in updated_hero.powers]
        }

        return make_response(jsonify(response_data), 201)

    except KeyError:
        return make_response(jsonify({"errors": ["Missing required data"]}), 400)
    except Exception as e:
        return make_response(jsonify({"errors": [str(e)]}), 500)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
