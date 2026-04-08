from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import random
import os
from Clase import db

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta_segura_2024'


@app.route('/templates/css/<filename>')
def serve_template_css(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', 'css'), filename)


@app.route('/style.css')
def serve_style_css():
    return send_from_directory(app.root_path, 'style.css')

@app.route('/logo.png')
def serve_logo():
    return send_from_directory(app.root_path, 'logo.png')

@app.route('/<path:filename>')
def serve_root_files(filename):
    
    if filename.endswith(('.jpeg', '.jpg', '.png', '.svg')):
        return send_from_directory(app.root_path, filename)
    return "Not Found", 404

# Inicializar la tabla de usuarios al iniciar la aplicación
db.crear_tabla()

def generate_stars():
    html_stars = ''
    for i in range(80):
        left = random.randint(0, 100)
        top = random.randint(0, 100)
        delay = random.uniform(0, 4)
        duration = random.uniform(2, 5)
        opacity = random.uniform(0.1, 0.6)
        html_stars += f'<div class="star" style="left: {left}%; top: {top}%; animation-delay: {delay}s; animation-duration: {duration}s; opacity: {opacity};"></div>'
    return html_stars

@app.route('/')
def index():
    #Página de inicio - muestra la página de correo
    html_stars = generate_stars()
    return render_template('microsoft-login.html', html_stars=html_stars)

@app.route('/index')
def index_root():
    #Página de bienvenida después del login
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    #Página de inicio de sesión de Microsoft Outlook - solo pide correo
    message = None
    
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            message = "Por favor, ingresa tu correo electrónico."
        elif '@' not in email or '.' not in email:
            message = "Ingresa un correo electrónico válido."
        else:
            # Guardar el correo en sesión y redirigir a la página de contraseña
            session['email_temp'] = email
            return redirect(url_for('password_page'))
    
    html_stars = generate_stars()
    return render_template('microsoft-login.html', 
                         message=message, 
                         html_stars=html_stars)

@app.route('/verify_email', methods=['POST'])
def verify_email():
    #Página de verificación de correo - solo pide correo
    message = None
    
    email = request.form.get('email')
    
    if not email:
        message = "Por favor, ingresa tu correo electrónico."
    elif '@' not in email or '.' not in email:
        message = "Ingresa un correo electrónico válido."
    else:
        # Guardar el correo en sesión y redirigir a la página de contraseña
        session['email_temp'] = email
        return redirect(url_for('password_page'))
    
    html_stars = generate_stars()
    return render_template('microsoft-login.html', 
                         message=message, 
                         html_stars=html_stars)

@app.route('/password', methods=['GET', 'POST'])
def password_page():
    #Página de contraseña - solo pide contraseña
    error = None
    email = session.get('email_temp')
    
    if not email:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        contrasena = request.form.get('contrasena')
        
        if not contrasena:
            error = "Por favor, ingresa tu contraseña."
        else:
            # Verificar usuario con correo y contraseña
            resultado = db.verificar_usuario(email, contrasena)
            if resultado:
                # Guardar en sesión
                session['usuario'] = resultado[0]
                session['plataforma'] = resultado[2]
                usuario_data = db.obtener_usuario(email)
                session['nombre'] = usuario_data[4] if usuario_data else ""
                # Limpiar el correo temporal
                session.pop('email_temp', None)
                return redirect(url_for('index_root'))
            else:
                error = "Contraseña incorrecta."
    
    html_stars = generate_stars()
    return render_template('password-page.html', 
                         email=email, 
                         error=error, 
                         html_stars=html_stars)

@app.route('/register', methods=['GET', 'POST'])
def register():
    #Página de registro de usuario
    message = None
    success = False
    
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')
        confirmar_contrasena = request.form.get('confirmar_contrasena')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        
        # Validaciones
        if not usuario or not contrasena or not confirmar_contrasena:
            message = "Por favor, completa todos los campos."
        elif '@' not in usuario or '.' not in usuario:
            message = "Ingresa un correo electrónico válido."
        elif len(contrasena) < 8:
            message = "La contraseña debe tener al menos 8 caracteres."
        elif contrasena != confirmar_contrasena:
            message = "Las contraseñas no coinciden."
        else:
            # Guardar en la base de datos
            resultado = db.insertar_usuario(usuario, contrasena, "Microsoft Outlook", nombre, apellido)
            if resultado:
                success = True
                message = "¡Cuenta creada exitosamente! Ahora puedes iniciar sesión."
            else:
                message = "El usuario ya existe en el sistema."
    
    html_stars = generate_stars()
    return render_template('register.html', 
                         message=message, 
                         success=success, 
                         html_stars=html_stars)

@app.route('/dashboard')
def dashboard():
    #Página principal después de iniciar sesión
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    html_stars = generate_stars()
    return render_template('dashboard.html',
                         usuario=session.get('usuario'),
                         plataforma=session.get('plataforma'),
                         nombre=session.get('nombre'),
                         html_stars=html_stars)

@app.route('/logout')
def logout():
    #Cerrar sesión
    session.clear()
    flash('Has cerrado sesión correctamente.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)