from flask import flash, render_template, request, session, abort
from sqlalchemy import select

from app import app
from models import Menu
from settings import  Session_db, config


@app.route('/menu')
def menu():
    with Session_db() as session:
        stmt = select(Menu).filter_by(active = True)
        all_positions = session.scalars(stmt).fetchall()
        
    return render_template('menu/menu.html', 
                           all_positions = all_positions,  
                           name_restaurant = config.NAME_RESTAURNAT)



@app.route('/position/<name>', methods = ['GET','POST'])
def position_details(name):
    if request.method == 'POST':
        position_name = request.form.get('name')
        position_num = request.form.get('num')
        
        if 'basket' not in session:
            basket = {}
            basket[position_name] = position_num
            session['basket'] = basket
        
        else:
            basket = session.get('basket')
            basket[position_name] = position_num
            session['basket'] = basket
        flash('Позицію додано у кошик!', category="successful")
    
    with Session_db() as cursor:
        stmt = select(Menu).filter_by(active = True, name = name)
        us_position = cursor.scalar(stmt)
        
    if us_position:
        return render_template('menu/position.html',
                           position = us_position,
                           name_restaurant = config.NAME_RESTAURNAT)
    else:
        abort(404)
        