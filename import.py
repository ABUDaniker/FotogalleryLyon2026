import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "exkursion-lyon-2026-geheim" # Ersetzen Sie diesen Schlüssel

# Ordner für Uploads festlegen
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Sicherstellen, dass der Ordner existiert
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' not in request.files:
        flash('Keine Datei ausgewählt')
        return redirect(request.url)
    
    file = request.files['photo']
    if file.filename == '':
        flash('Keine Datei ausgewählt')
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        # Hier wird die Datei auf dem Server (bzw. dem Cloud-Speicher des Servers) gespeichert
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Foto erfolgreich hochgeladen!')
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/gallery')
def gallery():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html', photos=files, files=files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Passwort-Logik (kann hier angepasst werden)
        if request.form.get('password') == 'geheim123':
            session['admin'] = True
        else:
            flash('Falsches Passwort!')
            
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('admin.html', photos=files, files=files)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'Datei {filename} gelöscht.')
    return redirect(url_for('admin'))

@app.route('/delete_all', methods=['POST'])
def delete_all():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    for file in files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
        os.remove(file_path)
    flash('Alle Fotos wurden gelöscht.')
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)