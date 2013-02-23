#-*- coding:UTF-8-*
from flask import request, render_template, Blueprint, redirect
from flask.ext.login import login_required
from canku import utils
from canku.extensions import db
from canku.models import Group, User, City

blue_print = Blueprint("group", __name__)


@blue_print.route('/explore')
@login_required
def explore():
    city_id = request.args.get('city')
    cities = City.query.all()
    if city_id and city_id != "0":
        city_id = int(city_id)
        groups = Group.query.filter(Group.city_id == city_id).all()
    else:
        city_id = 0
        groups = Group.query.all()
    return render_template("/group/explore.html", groups=groups, cities=cities, city_id=city_id)


@blue_print.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == "GET":
        cities = City.query.all()
        return render_template("/group/new.html", cities=cities)
    elif request.method == "POST":
        #已经加入小组的不能再创建小组
        if utils.get_currentt_user_group_id() > 0:
            return redirect('/')

        name = request.form["name"]
        descrip = request.form["descrip"]
        address = request.form["address"]

        if not name or not descrip or not address:
            return redirect('/?action=create_group_fail')

        group = Group(name, descrip, address, request.form['city'], utils.get_currentt_user_id())
        group.users = [utils.get_current_user()]

        db.session.add(group)
        db.session.commit()

        return redirect('/?action=create_group_success')


@blue_print.route('/join/<id>', methods=['POST'])
@login_required
def join(id):
    #已经加入小组的不能加入另外的小组
    if utils.get_currentt_user_group_id() > 0:
        return redirect('/')

    group = Group.query.filter(Group.id == id).first()

    if group:
        user = User.query.get(utils.get_currentt_user_id())
        user.group_id = id
        #新增用户数
        group.user_num += 1
        db.session.commit()
        return redirect('/?action=join_group_success')
    else:
        return redirect('/')