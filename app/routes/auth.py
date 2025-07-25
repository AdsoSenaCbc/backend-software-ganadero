from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Usuario
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import traceback

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        print(f"Registro - Datos recibidos: {dict(data)}")
        if Usuario.query.filter_by(correo=data.get('correo')).first():
            flash('El correo ya está registrado.', 'error')
            return redirect(url_for('auth.register'))
        if not all([data.get('nombres'), data.get('apellidos'), data.get('documento'),
                   data.get('correo'), data.get('telefono'), data.get('password')]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('auth.login'))
        new_user = Usuario(
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            documento=data['documento'],
            correo=data['correo'],
            telefono=data['telefono'],
            id_rol=int(data.get('id_rol', 2))
        )
        new_user.password = data['password']  # Usar el setter corregido
        try:
            db.session.add(new_user)
            db.session.commit()
            print(f"Usuario registrado: {new_user.correo}")
            flash('Registro exitoso. Por favor, inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            print(f"Error en registro: {str(e)}")
            print("Traceback completo:")
            traceback.print_exc()  # Mostrar el traceback completo
            flash(f'Error al registrar el usuario: {str(e)}.', 'error')
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        print(f"Login - Datos recibidos: {dict(data)}")
        user = Usuario.query.filter_by(correo=data.get('correo')).first()
        if user:
            print(f"Usuario encontrado: {user.correo}")
            password = data.get('password')
            if password is None:
                print("Campo 'password' no encontrado en el formulario")
                flash('Contraseña no proporcionada.', 'error')
                return redirect(url_for('auth.login'))
            print(f"Contraseña ingresada: {password}")
            try:
                is_valid = user.check_password(password)
                print(f"Verificación de hash: {is_valid}")
                if is_valid:
                    print("Contraseña válida, iniciando sesión...")
                    login_user(user)
                    access_token = create_access_token(identity={'id_usuario': user.id_usuario, 'nombres': user.nombres})
                    response = redirect(url_for('dashboard.index'))
                    response.set_cookie('jwt_token', access_token, httponly=True, secure=True)
                    return response
                else:
                    print("Contraseña inválida - Hash no coincide")
            except ValueError as e:
                print(f"Error al verificar hash: {e}")
        else:
            print("Usuario no encontrado")
        flash('Correo o contraseña incorrectos.', 'error')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    response = redirect(url_for('auth.login'))
    response.set_cookie('jwt_token', '', expires=0)
    flash('Has cerrado sesión.', 'success')
    return response