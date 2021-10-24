from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lista.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text)
    hecho = db.Column(db.Boolean, default=False)

    def __init__(self, contenido):
        self.contenido = contenido
        self.hecho = False

    def __repr__(self):
        return '<contenido %s>' % self.contenido

db.drop_all()
db.create_all()

@app.route('/')
def menu():
    tarea = Tarea.query.all()
    return render_template('index.html', tarea=tarea)


@app.route('/tarea', methods=['POST'])
def añadir_tarea():
    contenido = request.form['contenido']
    if not contenido:
        return 'Error'

    tarea = Tarea(contenido)
    db.session.add(tarea)
    db.session.commit()
    return redirect('/')


@app.route('/delete/<int:tarea_id>')
def eliminar(tarea_id):
    tarea = Tarea.query.get(tarea_id)
    if not tarea:
        return redirect('/')

    db.session.delete(tarea)
    db.session.commit()
    return redirect('/')


@app.route('/done/<int:tarea_id>')
def completar(tarea_id):
    tarea = Tarea.query.get(tarea_id)

    if not tarea:
        return redirect('/')
    if tarea.hecho:
        tarea.hecho = False
    else:
        tarea.hecho = True

    db.session.commit()
    return redirect('/')



if __name__=='__main__':
    app.run(debug=True,use_reloader=True)
    
    