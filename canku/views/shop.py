#-*- coding:UTF-8-*-
import random
from flask import request, render_template, Blueprint, jsonify, redirect, url_for
from flask.ext.login import login_required
from canku import utils
from canku.extensions import db
from canku.models import Shop, Order, FoodCategory, Food, Group, City
import json

blue_print = Blueprint("shop", __name__)


@blue_print.route('/add', methods=["GET", "POST"])
@login_required
def add():
    """添加店铺页面"""
    if request.method == "GET":
        return render_template('/shop/add.html')
    elif request.method == "POST":
        if utils.get_currentt_user_group_id():
            name = request.form['name']
            tel = request.form['tel']
            address = request.form['address']
            city_id = utils.get_currentt_user_group().city_id

            if not name or not tel or not address or not city_id:
                return redirect("/action=add_shop_fail")

            shop = Shop(name, address, tel, city_id, utils.get_currentt_user_id())
            utils.get_currentt_user_group().shops.append(shop)
            db.session.add(shop)
            db.session.commit()

            return redirect(url_for('shop.edit_food', id=shop.id))
        else:
            return redirect("/")


@blue_print.route('/edit_food')
@login_required
def edit_food():
    """编辑美食页面"""
    id = request.args.get('id')

    if not id:
        return redirect("/")
    else:
        id = int(id)

    #检查小组是否已经添加这个店铺
    group = Group.query.filter(Group.id == utils.get_currentt_user_group_id(), Shop.id == id).first()

    if group:
        shop = Shop.query.get(id)
        return render_template("/shop/edit_food.html", shop=shop)
    else:
        return redirect('/')


@blue_print.route("/add_category", methods=["POST"])
@login_required
def add_food_category():
    """添加美食分类，仅提供POST方法"""
    category_name = request.form.get('name')
    shop_id = request.form.get('id')
    fc = FoodCategory(category_name, shop_id)
    db.session.add(fc)
    db.session.commit()
    return '{"msg":"success","id":' + str(fc.id) + '}'


@blue_print.route("/remove_category", methods=["POST"])
@login_required
def remove_food_category():
    """删除美食分类，仅提供POST方法"""
    cate_id = request.form.get('id')
    db.session.query(Food).filter(Food.foodcategory_id == cate_id).delete()
    db.session.query(FoodCategory).filter(FoodCategory.id == cate_id).delete()
    db.session.commit()
    return '{"msg":"success"}'


@blue_print.route("/update_food", methods=["POST"])
@login_required
def update_food():
    """更新/添加美食，仅提供POST方法"""
    fcid = request.form.get('fcid')
    id = request.form.getlist('id')
    name = request.form.getlist('name')
    price = request.form.getlist('price')
    week = request.form.getlist('week')

    foodcategory = FoodCategory.query.filter_by(id=fcid).first()

    if len(id) > 0:
        for i in range(0, len(name)):
            if id[i] and name[i] and price[i] > 0 and week[i]:

                if id[i] == '0':
                    #增加的（id = 0 ）
                    foodcategory.foods.append(
                        Food(name[i], price[i], foodcategory.shop_id, week[i], fcid))
                else:
                    #更新的（id !=0）
                    Food.query.filter_by(id=id[i]).update(
                        {Food.name: name[i], Food.price: price[i], Food.week: week[i]})

        db.session.commit()

        return jsonify(msg="success", fl=[i.serialize for i in foodcategory.foods])
    else:
        return '{"msg":"error"}'


@blue_print.route('/explore')
@login_required
def shop_explore():
    city_id = utils.get_currentt_user_group().city_id

    city = City.query.filter_by(id=city_id).first()

    if city:
        shops = Shop.query.filter(Shop.city_id == city_id).all()
        return render_template('/shop/explore.html', shops=shops, city=city, city_id=city_id)
    else:
        return redirect('/')


@blue_print.route('/fav', methods=["POST"])
@login_required
def shop_fav():
    shop_id = request.form['shop_id']
    group_id = utils.get_currentt_user_group_id()

    if group_id:
        result = Group.query.filter(Group.shops.any(id=shop_id)).first()
        group = Group.query.filter(Group.id == group_id, Shop.id == shop_id).first()
        shop = Shop.query.get(shop_id)

        if result:
            group.shops.remove(shop)
            stat = 0
        else:
            group.shops.append(shop)
            stat = 1

        db.session.commit()

        return '{"msg":"success", "stat":' + str(stat) + '}'
    else:
        return redirect("/")


@blue_print.route('/fav_list')
@login_required
def shop_fav_list():
    group = Group.query.get(utils.get_currentt_user_group_id())
    return jsonify(msg="success", shops=[i.serialize for i in group.shops])


@blue_print.route('/<int:id>')
@login_required
def shop(id):
    shop = Shop.get(id)
    week = utils.get_weekday()
    return render_template('/shop/item.html', shop=shop, week=week)


@blue_print.route('/submit_order', methods=["POST"])
@login_required
def submit_order():
    luck = random.randint(0, 100)
    list = request.form.get('list')
    user_id = utils.get_currentt_user_id()
    shop_id = int(request.form.get('shop_id'))
    time = utils.get_now()

    #检查小组是否已经添加这个店铺
    group = Group.query.filter(Group.id == utils.get_currentt_user_group_id(), Shop.id == shop_id).first()

    if group:
        #计算总价
        order_list = json.loads(list)
        total = 0.0
        for order in order_list:
            total += float(order['price']) * int(order['num'])

        order = Order(user_id, shop_id, utils.get_currentt_user_group_id(), total, time, list, luck)

        db.session.add(order)
        db.session.commit()

        return jsonify(result="success", luck=luck)
    else:
        return redirect("/")