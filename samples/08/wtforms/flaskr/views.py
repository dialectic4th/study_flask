from flask import request, redirect, url_for, render_template, flash
from flask.ext.login import current_user, login_user, login_required, \
        logout_user
from flaskr import app, db
from flaskr.models import Entry, User
from flaskr.forms import LoginForm

@app.route('/')
def show_entries():
    entries = Entry.query.order_by(Entry.id.desc()).limit(10).all()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
@login_required
def add_entry():
    entry = Entry(
            title=request.form['title'],
            text=request.form['text']
            )
    db.session.add(entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('show_entries'))
    form = LoginForm(request.form)
    error = None
    if form.validate_on_submit():
        user, authenticated = User.authenticate(db.session.query, 
                form.username.data,
                form.password.data)
        if authenticated:
            login_user(user)
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', error=error, form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('show_entries'))
