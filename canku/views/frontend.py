#-*- coding:UTF-8-*-
from flask import render_template, session, Blueprint, request, url_for, redirect, json, current_app
from flask.ext.login import login_required, current_user
from canku import utils
from canku.libs import duoshuo
from canku.extensions import db
from canku.libs.connect_qq import QQAPIClient
from canku.libs.connect_sina import SinaAPIClient
from canku.models import User, Order, Connect, Group, City

blue_print = Blueprint("frontend", __name__)


@blue_print.route('/')
@login_required
def index():
    if utils.get_currentt_user_group_id():
        shops = Group.query.get(utils.get_currentt_user_group_id()).shops
    else:
        shops = None
    return render_template('index.html', shops=shops)


@blue_print.route('/today')
@login_required
def today():
    today_time = utils.get_now().strftime('%Y-%m-%d 00:00:00')
    orders = Order.query.filter(Order.time > today_time, Order.group_id == utils.get_currentt_user_group_id()).all()

    if len(orders) == 0:
        return render_template('today.html', all=None)

    #准备好数组进行处理
    todayOrder = {}

    #进行处理
    for order in orders:
        if str(order.shop.id) in todayOrder:
            item = todayOrder[str(order.shop.id)]
            item["orders"].append(order)
            item["total"] += order.total
            if order.luck <= item["min_luck"]:
                item["min_luck"] = order.luck
                item["min_user"] = order.user
        else:
            todayOrder[str(order.shop.id)] = {
                "min_luck": order.luck,
                "min_user": order.user,
                "total": order.total,
                "shop": order.shop,
                "orders": [order],
                "analytics": {},
                "totalNum": 0
            }
        order_text = json.loads(order.text)
        for ot in order_text:
            if ot["id"] in todayOrder[str(order.shop.id)]["analytics"]:
                todayOrder[str(order.shop.id)]["totalNum"] += ot["num"]
                todayOrder[str(order.shop.id)]["analytics"][str(ot["id"])]["num"] += ot["num"]
                todayOrder[str(order.shop.id)]["analytics"][str(ot["id"])]["total"] += (float(ot["price"]) * ot["num"])
            else:
                todayOrder[str(order.shop.id)]["analytics"][str(ot["id"])] = {
                    "id": ot["id"],
                    "name": ot["name"],
                    "num": ot["num"],
                    "price": float(ot["price"]),
                    "total": float(ot["price"]) * int(ot["num"])
                }
                todayOrder[str(order.shop.id)]["totalNum"] = ot["num"]

    return render_template('today.html', all=todayOrder)


@blue_print.route('/account', methods=["GET", "POST"])
@login_required
def account():
    if request.method == "GET":
        msg = ['',
               u'请填写完整后再提交',
               u'更新成功']
        user = utils.get_current_user()
        if int(request.args.get('msg') or 0) == 2:
            msg_result = 'success'
        else:
            msg_result = 'error'
        msg_text = msg[int(request.args.get('msg') or 0)]
        return render_template('account.html', user=user, msg=msg_text, msg_result=msg_result)
    elif request.method == "POST":
        nickname = request.form.get('nickname')
        name = request.form.get('name')

        #email 未填写
        if nickname and name:
            user = User.query.get(utils.get_currentt_user_id())
            user.name = name
            user.nickname = nickname
            db.session.commit()
            return redirect(url_for('frontend.account', msg=2))
        else:
            return redirect(url_for('frontend.account', msg=1))


@blue_print.route('/signin')
def signin():
    return render_template('signin.html')


@blue_print.route('/signup')
def signup():
    return render_template('signup.html')


@blue_print.route('/signout')
def signout():
    utils.logout()
    return redirect('/signin')


@blue_print.route('/connect/<app>')
def connect_sina(app):
    url = ''
    if app == 'sina':
        sinaClient = SinaAPIClient(
            app_key=current_app.config.get('SINA_APP_KEY'),
            app_secret=current_app.config.get('SINA_APP_SECRET'),
            redirect_uri=current_app.config.get('SINA_CALLBACK_URL')
        )
        url = sinaClient.get_authorize_url()
    elif app == 'qq':
        qqClient = QQAPIClient(
            client_id=current_app.config.get('QQ_APP_KEY'),
            client_secret=current_app.config.get('QQ_APP_SECRET'),
            redirect_uri=current_app.config.get('QQ_CALLBACK_URL')
        )
        url = qqClient.get_auth_url()
    return redirect(url)


@blue_print.route('/connect/<app>/authorized')
def connect_authorized(app):
    code = request.args.get('code')
    open_user = {}
    if app == "sina":
        sinaClient = SinaAPIClient(
            app_key=current_app.config.get('SINA_APP_KEY'),
            app_secret=current_app.config.get('SINA_APP_SECRET'),
            redirect_uri=current_app.config.get('SINA_CALLBACK_URL')
        )
        try:
            r = sinaClient.request_access_token(code)
            access_token = r.get("access_token")
            expires_in = r.get("expires_in")
            sinaClient.set_access_token(access_token, expires_in)
            try:
                sinaUser = sinaClient.users.show.get(uid=r.uid)
                open_user["id"] = sinaUser.id
                open_user["name"] = sinaUser.name
                open_user["access_token"] = access_token
                open_user["figureurl"] = sinaUser.profile_image_url
            except:
                return redirect('/signin')
        except:
            return redirect
    elif app == "qq":
        qqClient = QQAPIClient(
            client_id=current_app.config.get('QQ_APP_KEY'),
            client_secret=current_app.config.get('QQ_APP_SECRET'),
            redirect_uri=current_app.config.get('QQ_CALLBACK_URL')
        )
        r = qqClient.request_access_token(code)
        access_token = r.get("access_token")
        expires_in = r.get("expires_in")
        qqClient.set_access_token(access_token, expires_in)
        openid = qqClient.request_openid()
        qqClient.set_openid(openid)
        qqUser = qqClient.request_api('user/get_user_info')
        open_user["id"] = openid
        open_user["name"] = qqUser.nickname
        open_user["access_token"] = access_token
        open_user["figureurl"] = qqUser.figureurl_1

    connect = Connect.query.filter(Connect.openid == open_user["id"], Connect.app == app).first()

    if connect:
        connect.access_token = open_user["access_token"]
        db.session.commit()
        user = User.query.get(connect.user_id)
        utils.login(user)
        return redirect(url_for("frontend.index"))
    else:
        session['user'] = User(
            nickname=open_user["name"],
            name=open_user["name"],
            join=utils.get_now(),
            figureurl=open_user["figureurl"]
        )
        session['connect'] = Connect(open_user["id"], open_user["access_token"], app)
        return redirect(url_for("frontend.connect_callback", app=app))


@blue_print.route('/connect/callback', methods=["GET", "POST"])
def connect_callback():
    """完善资料"""
    if request.method == "GET":
        siteName = u"新浪微博" if session.get('connect').app != "qq" else u"腾讯QQ"
        return render_template("callback.html", user=session.get('user'), app=session.get('connect').app,
            siteName=siteName)
    elif request.method == "POST":
        nickname = request.form["nickname"]
        name = request.form["name"]
        user = session.get('user')
        if name:
            user.name = name
        if nickname:
            user.nickname = nickname
        user.connects = [session.get('connect')]
        db.session.add(user)
        db.session.commit()
        utils.login(user)
        return redirect(url_for("frontend.index", action="signup_success"))


@blue_print.route('/city/add', methods=["GET", "POST"])
def city_add():
    if request.method == "GET":
        return render_template('city/add.html')
    elif request.method == "POST":
        city = City(request.form['name'])
        db.session.add(city)
        db.session.commit()
        return render_template('city/add.html')


@blue_print.route('/about')
def about():
    return render_template("/info/about.html")


@blue_print.route('/suggestions')
def suggestions():
    code = None
    if current_user.is_authenticated():
        user = utils.get_current_user()
        code = duoshuo.remote_auth(user.id, user.nickname, '', '', user.figureurl)
    return render_template("/info/suggestions.html", code=code)


@blue_print.route('/help')
def help():
    return render_template("/info/help.html")


@blue_print.route('/license')
def license():
    return render_template("/info/license.html")


@blue_print.route('/ie')
def ie():
    return render_template("/info/ie.html")





