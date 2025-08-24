from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Trocar em produção
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

# Gerencia login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


# -------------------- ROTAS -------------------- #

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash("Usuário já existe", "danger")
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            password = generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Usuário registrado com sucesso! Faça login.", "success")
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Usuário ou senha incorretos", "danger")

    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# -------------------- ADMIN - LISTA USUÁRIOS -------------------- #
@app.route('/admin/users')
@login_required
def list_users():
    # só deixa acessar se for o "admin"
    if current_user.username != "admin":
        flash("Acesso não autorizado.", "danger")
        return redirect(url_for("index"))

    users = User.query.all()
    return render_template("admin_users.html", users=users)


# -------------------- RELATÓRIO -------------------- #

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    if request.method == 'POST':
        # Mesma lógica do seu código original...
        data_raw = request.form.get('data')
        data_formatada = datetime.strptime(data_raw, "%Y-%m-%d").strftime("%d/%m/%Y")

        fazenda = request.form.get('fazenda')
        talhao = request.form.get('talhao')
        turno = request.form.get('turno')
        status = request.form.get('status')
        maquina = request.form.get('maquina')
        operador = request.form.get('operador')
        hinicial = request.form.get('horimetro_inicial')
        hfinal = request.form.get('horimetro_final')
        horas_trabalhadas = request.form.get('horas_trabalhadas')
        producao_ha = request.form.get('producao_ha')
        equipe_transporte = request.form.get('equipe_transporte')
        dds_cafe = request.form.get('dds_cafe')
        transporte_pracha = request.form.get('transporte_pracha')

        manutencoes = []
        index = 0
        while f'manutencao_{index}' in request.form:
            manutencao = request.form.get(f'manutencao_{index}')
            if manutencao:
                manutencoes.append({
                    "tipo": manutencao,
                    "horario_inicial": request.form.get(f'manutencao_horimetro_inicial_{index}'),
                    "horario_final": request.form.get(f'manutencao_horimetro_final_{index}'),
                    "tempo": request.form.get(f'tempo_manutencao_{index}')
                })
            index += 1

        relatorio = (
            f"Data: {data_formatada}\n"
            f"Fazenda: {fazenda}\n"
            f"Talhão: {talhao}\n"
            f"Turno: {turno}\n"
            f"Status: {status}\n"
            f"Máquina: {maquina}\n"
            f"Operador: {operador}\n"
            f"Horímetro Inicial: {hinicial}\n"
            f"Horímetro Final: {hfinal}\n"
            f"Horas Trabalhadas: {horas_trabalhadas}\n"
            f"Produção HA: {producao_ha}\n"
            f"Equipe em Transporte: {equipe_transporte}\n"
            f"DDS/CAFÉ: {dds_cafe}\n"
        )

        relatorio += "\nInspensão diária:\n"
        for i, m in enumerate(manutencoes):
            relatorio += (
                f"\nManutenção {i+1}:\n"
                f"- Tipo: {m['tipo']}\n"
                f"- Horário Inicial: {m['horario_inicial']}\n"
                f"- Horário Final: {m['horario_final']}\n"
                f"- Tempo: {m['tempo']}\n"
            )

        relatorio += f"\nEm Transporte Prancha: {transporte_pracha}\n"

        return render_template('report.html', relatorio=relatorio)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)