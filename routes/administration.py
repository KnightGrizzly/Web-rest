import os
import uuid

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from app import admin_required, app
from models import Menu, Orders, User
from settings import Session_db, config


@app.route("/admin/add_position", methods=["GET", "POST"])
@admin_required
def add_position():
    if request.method == "POST":

        name = request.form["name"]
        file = request.files.get("img")
        ingredients = request.form["ingredients"]
        description = request.form["description"]
        price = request.form["price"]
        weight = request.form["weight"]

        if not file or not file.filename:
            return "Файл не вибрано або завантаження не вдалося"

        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        output_path = os.path.join("static/menu", unique_filename)

        with open(output_path, "wb") as f:
            f.write(file.read())

        with Session_db() as cursor:
            new_position = Menu(
                name=name,
                ingredients=ingredients,
                description=description,
                price=price,
                weight=weight,
                file_name=unique_filename,
            )
            cursor.add(new_position)
            cursor.commit()

        flash("Позицію додано успішно!")

    return render_template(
        "admin/add_position.html", name_restaurant=config.NAME_RESTAURNAT
    )


@app.route("/menu_check", methods=["GET", "POST"])
@admin_required
def menu_check():
    if request.method == "POST":

        position_id = request.form["pos_id"]
        with Session_db() as cursor:
            position_obj = cursor.query(Menu).filter_by(id=position_id).first()
            if "change_status" in request.form:
                position_obj.active = not position_obj.active
            elif "delete_position" in request.form:
                cursor.delete(position_obj)
            cursor.commit()

    with Session_db() as cursor:
        all_positions = cursor.query(Menu).all()

    return render_template(
        "admin/check_menu.html", all_positions=all_positions, title="admin.menu"
    )


@app.route("/admin/all_orders", methods=["GET", "POST"])
@admin_required
def all_orders():
    if request.method == "POST":
        order_id = request.form.get("order_id")

        with Session_db() as cursor:
            stmt = select(Orders).where(Orders.id == order_id)
            order = cursor.scalar(stmt)
            if order and order.status == "active":
                order.status = "completed"
                cursor.commit()

        return redirect(url_for("all_orders"))

    with Session_db() as cursor:
        stmt = select(Orders, User).join(User, Orders.user_id == User.id)
        orders_results = cursor.execute(
            stmt
        ).fetchall()  # [(ordrer1 ,user), (order2, user)...]

    return render_template("admin/orders.html", orders_results=orders_results)


@app.route("/admin/all_users", methods=["GET", "POST"])
@admin_required
def all_users():
    with Session_db() as cursor:
        stmt = select(User)
        user_results = cursor.execute(
            stmt
        ).fetchall()  # [(ordrer1 ,user), (order2, user)...]

    return render_template("admin/users.html", user_results=user_results)