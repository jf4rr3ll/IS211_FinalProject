#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Final Project 12 Module"""

from flask import Flask, request, session, g, redirect, url_for, render_template, flash
import sqlite3
import time
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "super secret key"
USERNAME = 'admin'
PASSWORD = 'p@ssw0rd'


def connect_db():
    return sqlite3.connect('blog.db')


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME:
            error = 'The system does not recognize that username.'
            return render_template('login.html', error=error)
        elif request.form['password'] != PASSWORD:
            error = 'The password is incorrect; please try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            return redirect('/dashboard')
    else:
        return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out')
    return redirect(url_for('/login'))


@app.route('/dashboard', methods=['GET', 'POST'])
def loaddashboard():
    if session['logged_in'] == False:
        return redirect('/login')
    else:
        g.db = connect_db()
        cur = g.db.execute('SELECT Author, Title, Date FROM posts ORDER BY Date ASC')
        posts = [dict(author=row[1], title=row[2], date=row[4]) for row in cur.fetchall()]
        g.db.close()
        return render_template('dashboard.html', posts=posts)


@app.route('/new', methods=['GET', 'POST'])
def createnew():
    if session['logged_in'] == False:
        return redirect('/login')
    else:
        if request.method == 'GET':
            return render_template('new.html')
        if request.method == 'POST':
            g.db.execute('INSERT INTO entries (Author, Title, Content, Date) VALUES (?, ?, ?, ?)', (USERNAME,
                                                                                             request.form['title'],
                                                                                             request.form['content'],
                                                                                             (time.strftime("%d/%m/%Y"))))
            g.db.commit()
            return redirect(url_for('dashboard'))
        return render_template('dashboard.html')

@app.route('/edit/<postid>', methods=['GET', 'POST'])
def editpost(postid):
    if session['logged_in'] == False:
        return redirect('/login')
    else:
        if request.method == 'GET':
            cur = g.db.execute('SELECT PostID, Title, Content FROM entries WHERE PostID = ?', (postid))
            posts = [dict(id=row[0], title=row[2], content=row[3]) for row in cur.fetchall()]
            return render_template('edit.html', posts=posts)
        elif request.method == 'POST':
            g.db.execute('UPDATE posts SET Title = ?, Content = ?, Date = ? WHERE PostID = ?)', (request.form['title'],
                                                                                             request.form['content'],
                                                                                             (time.strftime("%d/%m/%Y")),
                                                                                             postid))
            g.db.commit()
            return redirect(url_for('dashboard'))
        return render_template('dashboard.html')

@app.route('/delete/<postid>', methods=['GET','POST'])
def deletepost(postid):
    if session['logged_in'] == False:
        return redirect('/login')
    else:
        g.db = connect_db()
        g.db.execute('DELETE FROM posts WHERE PostID = %s' % (postid))
        g.db.commit()
        return redirect(url_for('dashboard'))


@app.route('/feed', methods=['GET', 'POST'])
def viewfeed():
    if session['logged_in'] == False:
        return redirect('/login')
    else:
        g.db = connect_db()
        cur = g.db.execute('SELECT * FROM posts ORDER BY Date ASC')
        posts = [dict(author=row[1], title=row[2], content=row[3], date=row[4]) for row in cur.fetchall()]
        g.db.close()
        return render_template('dashboard.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)