from models import db, User, Report, Relatorio
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # trocar em produção
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

# Login manager
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

        if User.query.filter_by(username=username).first():
            flash("Usuário já existe", "danger")
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256')
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


# -------------------- DASHBOARD (gráficos) -------------------- #
@app.route('/dashboard')
@login_required
def dashboard():
    # --- Gráfico de Horas Trabalhadas ---
    relatorios = Report.query.filter_by(user_id=current_user.id).all()
    datas = [r.data for r in relatorios]
    try:
        horas = [float(r.horas_trabalhadas) if r.horas_trabalhadas else 0 for r in relatorios]
    except ValueError:
        horas = [0 for _ in relatorios]

    # --- Gráfico de Manutenções (Pizza) ---
    reports = Report.query.filter_by(user_id=current_user.id).all()
    manutencao_totais = {}

    for rep in reports:
        try:
            manutencoes = json.loads(rep.manutencoes) if rep.manutencoes else []
        except:
            manutencoes = []

        for m in manutencoes:
            tipo = m.get("tipo", "Outros")
            tempo = m.get("tempo", 0)

            try:
                tempo = float(tempo)
            except:
                tempo = 0

            manutencao_totais[tipo] = manutencao_totais.get(tipo, 0) + tempo

    tipos_manutencao = list(manutencao_totais.keys())
    tempos_manutencao = list(manutencao_totais.values())

    return render_template(
        "dashboard.html",
        datas=datas,
        horas=horas,
        tipos_manutencao=tipos_manutencao,
        tempos_manutencao=tempos_manutencao
    )


# -------------------- LISTAR RELATÓRIOS -------------------- #
@app.route('/meus-relatorios')
@login_required
def meus_relatorios():
    relatorios = Report.query.filter_by(user_id=current_user.id).all()
    return render_template("meus_relatorios.html", relatorios=relatorios)


# -------------------- ADMIN - LISTA USUÁRIOS -------------------- #
@app.route('/admin/users')
@login_required
def list_users():
    if current_user.username != "admin":
        flash("Acesso não autorizado.", "danger")
        return redirect(url_for("index"))

    users = User.query.all()
    return render_template("admin_users.html", users=users)


# -------------------- ADMIN - LISTAR TODOS OS RELATÓRIOS -------------------- #
@app.route('/admin/relatorios')
@login_required
def admin_relatorios():
    if current_user.username != "admin":
        flash("Acesso não autorizado.", "danger")
        return redirect(url_for("index"))

    relatorios = Report.query.all()
    return render_template("admin_relatorios.html", relatorios=relatorios)


# -------------------- RELATÓRIO -------------------- #
@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
@login_required
def submit():
    if request.method == 'POST':
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

        new_report = Report(
            user_id=current_user.id,
            data=data_formatada,
            fazenda=fazenda,
            talhao=talhao,
            turno=turno,
            status=status,
            maquina=maquina,
            operador=operador,
            horimetro_inicial=hinicial,
            horimetro_final=hfinal,
            horas_trabalhadas=horas_trabalhadas,
            producao_ha=producao_ha,
            equipe_transporte=equipe_transporte,
            dds_cafe=dds_cafe,
            transporte_pracha=transporte_pracha,
            manutencoes=json.dumps(manutencoes, ensure_ascii=False)
        )
        db.session.add(new_report)
        db.session.commit()

        flash("Relatório salvo com sucesso!", "success")
        return redirect(url_for('index'))


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
