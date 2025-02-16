from flask import Flask, request, jsonify
from database import db
from flask_login import LoginManager, login_user, current_user, UserMixin, logout_user, login_required
from models.user import User, Meal  
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'admin123'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if name and password and email:
     
     user = User.query.filter_by(name=name).first()

     if user and user.password == password:
        login_user(user)
        print(current_user.is_authenticated)
     return jsonify({'message': 'Login com sucesso'}), 200

    return jsonify({'message': 'Login deu erro'}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout com sucesso'}), 200


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if name and password and email:
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Usuário criado com sucesso'}), 201

    return jsonify({'message': 'Erro ao criar usuário'}), 400


@app.route('/meal', methods=['POST'])
@login_required
def create_meal():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    is_diet = data.get('is_diet', False)  # Se não for enviado, assume False

    if not name:
        return jsonify({'message': 'Nome da refeição é obrigatório'}), 400

    new_meal = Meal(
        user_id=current_user.id,
        name=name,
        description=description,
        is_diet=is_diet
    )

    db.session.add(new_meal)
    db.session.commit()

    return jsonify({'message': 'Refeição criada com sucesso!'}), 201



@app.route('/user/me', methods=['GET'])
@login_required
def get_user_data():
    user_data = {
        'id': current_user.id,
        'name': current_user.name,
        'email': current_user.email,
        'meals': []
    }

    meals = Meal.query.filter_by(user_id=current_user.id).all()
    for meal in meals:
        user_data['meals'].append({
            'id': meal.id,
            'name': meal.name,
            'description': meal.description,
            'date_time': meal.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_diet': meal.is_diet
        })

    return jsonify(user_data), 200


@app.route('/meal/delete', methods=['POST'])
@login_required
def delete_meal():
    data = request.get_json()
    meal_id = data.get('meal_id')

    if not meal_id:
        return jsonify({'message': 'ID da refeição é obrigatório'}), 400

    meal = Meal.query.get(meal_id)

    if not meal:
        return jsonify({'message': 'Refeição não encontrada'}), 404

    if meal.user_id != current_user.id:
        return jsonify({'message': 'Você não tem permissão para excluir esta refeição'}), 403

    db.session.delete(meal)
    db.session.commit()

    return jsonify({'message': 'Refeição excluída com sucesso!'}), 200

@app.route('/user/delete', methods=['POST'])
@login_required
def delete_user():
    user = User.query.get(current_user.id)

    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    # Excluir todas as refeições do usuário
    Meal.query.filter_by(user_id=user.id).delete()

    # Excluir o próprio usuário
    db.session.delete(user)
    db.session.commit()

    logout_user()  # Deslogar o usuário após a exclusão

    return jsonify({'message': 'Usuário e suas refeições foram excluídos com sucesso!'}), 200


@app.route('/login', methods=['GET'])
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
 