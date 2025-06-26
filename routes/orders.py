from datetime import datetime

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from app import app
from models import Menu, Orders
from settings import Session_db, config


@app.route("/profile")
@login_required
def profile():
    with Session_db() as cursor:
        stmt = select(Orders).filter_by(user_id=current_user.id)
        us_orders = cursor.scalars(stmt)
        return render_template(
            "profile.html",
            title=f"Account {current_user.username}",
            us_orders=us_orders,
        )


@app.route("/profile/create_order", methods=["GET", "POST"])
@login_required
def create_order():
    basket = session.get("basket")

    if request.method == "POST":

        with Session_db() as cursor:
            new_order = Orders(
                order_list=basket, order_time=datetime.now(), user_id=current_user.id
            )
            cursor.add(new_order)
            cursor.commit()

            session.pop("basket")

            cursor.refresh(new_order)

            return redirect(url_for("order_details", order_id=new_order.id))
            # return redirect(url_for("menu"))

    return render_template("orders/create_order.html", basket=basket)


@app.route("/profile/my_order_details/<int:order_id>")
@login_required
def order_details(order_id):
    with Session_db() as cursor:
        stmt = select(Orders).filter_by(id=order_id)
        us_order = cursor.scalar(stmt)
        # us_order = cursor.query(Orders).filter_by(id=id).first()

        total_price = sum(
            [
                cursor.scalar(select(Menu).filter_by(name=name_product)).price
                * int(cnt)
                for name_product, cnt in us_order.order_list.items()
            ]
        )
        # total_price = sum(int(cursor.query(Menu).filter_by(name=i).first().price) * int(cnt) for i, cnt in us_order.order_list.items())
    return render_template(
        "orders/my_order.html", order=us_order, total_price=total_price
    )


@app.route("/profile/cancel_order/<int:order_id>")
@login_required
def cancel_order(order_id):
    with Session_db() as cursor:
        stmt = select(Orders).filter_by(id=order_id)
        us_order = cursor.scalar(stmt)

        # us_order.status = "disable"

        cursor.delete(us_order)
        cursor.commit()

    return redirect(url_for("profile"))