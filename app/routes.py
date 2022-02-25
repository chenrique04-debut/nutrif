from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash 

from app import db
from app.forms import LoginForm, RegisterForm
from app.models import User


def init_app(app):
    @app.route("/")
    def index():
        users = User.query.all() # Select * from users;

        # se o usuário estiver logado, exibir página de usuários
        if current_user.is_active:
            return render_template("users.html", users=users)
        return render_template("index.html")

    @app.route("/user/<int:id>")
    @login_required
    def unique(id):
        # seleciona o usuário pelo id passado e retorna ele no template de user
        user = User.query.get(id)
        return render_template("user.html", user=user)

    @app.route("/user/delete/<int:id>")
    def delete(id):
        # seleciona o usuário pelo id passado e deleta ele do banco de dados
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()

        return redirect("/")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegisterForm()

        if form.validate_on_submit():
            user = User()

            # adiciona os dados cadastrados no banco de dados
            user.name = form.name.data
            user.email = form.email.data
            # o generate_password_hash é usado para gerar uma senha criptografada antes de armazenar no banco
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            # loga o usuário e redireciona para a rota index
            login_user(user)
            return redirect(url_for("index"))

        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()

            if not user:
                # verifica se o usuário existe através do email
                flash("Credênciais incorretas")
                return redirect(url_for("login"))

            # o check_password_hash é usado para 'descriptografar' e comparar senhas
            if not check_password_hash(user.password, password):
                # verifica se a senha informada bate com a senha do usuário registrado
                flash("Credênciais incorretas")
                return redirect(url_for("login"))

            # loga o usuário e redireciona para a rota index
            login_user(user)
            return redirect(url_for("index"))

        return render_template("login.html", form=form)


    @app.route("/logout")
    @login_required
    def logout():
        # desfaz o login do usuário
        logout_user()
        return redirect(url_for("index"))
