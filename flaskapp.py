# author: Michael Castro
# description: Flask app for world database explorer


from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/countries')
def countries():
    countries_list = get_countries()
    return render_template('countries.html', countries=countries_list)

@app.route('/favorites')
def favorites():
    favorites_list = get_favorites()
    return render_template('favorites.html', favorites=favorites_list)


@app.route('/add-favorite', methods=['POST'])
def add_favorite():
    code = request.form['code']
    name = request.form['name']
    continent = request.form['continent']

    add_favorite_country(code, name, continent)
    flash(f'{name} was added to favorites.', 'success')
    return redirect(url_for('countries'))


@app.route('/update-favorite/<code>', methods=['GET', 'POST'])
def update_favorite(code):
    if request.method == 'POST':
        note = request.form['note']
        update_favorite_note(code, note)
        flash('Favorite note updated successfully.', 'warning')
        return redirect(url_for('favorites'))
    else:
        favorite = get_one_favorite(code)
        return render_template('update_favorite.html', favorite=favorite)


@app.route('/delete-favorite/<code>', methods=['POST'])
def delete_favorite(code):
    delete_favorite_country(code)
    flash('Favorite deleted successfully.', 'danger')
    return redirect(url_for('favorites'))

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
