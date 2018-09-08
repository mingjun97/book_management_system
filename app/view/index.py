from . import view
from flask import render_template, request, redirect, url_for, current_app, session
from flask_login import  login_required, login_user, logout_user, current_user
from io import BytesIO
from app.models import Admin, Reader, Record, Book
from app import db
from datetime import datetime
from random import sample
from hashlib import md5
import re
import chardet


@view.route("/")
def index():
    try:
        book_kinds = db.session.execute("select count(*) from books").first()[0]
    except Exception:
        book_kinds = 0
    try:
        book_amount = db.session.execute("select sum(amount) from books").first()[0]
        book_store = db.session.execute("select sum(store) from books").first()[0]
        book_lent = book_amount - book_store
    except Exception:
        book_store = 0
        book_lent = 0
    return render_template("index.html", book_kinds=book_kinds, book_stored=book_store, book_lent=book_lent)


@view.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@view.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        if "name" not in request.form and "password" not in request.form:  # 检查用户提交的表单是否正确
            return render_template("login.html", message="输入错误！")
        user = Admin.query.filter_by(name=request.form["name"]).first() # 从数据库中查找出该用户名对应的数据
        if user is None:  # 用户名不存在
            session['message'] = "用户名/密码错误"
        else:
            if md5((user.password + session['token']).encode('utf-8')).hexdigest() == request.form['password']: # 对用户提交的password字段进行运算验证
                login_user(user) # 登陆成功
                return redirect(request.args.get('next', default=url_for('app.view.manage')))
            else:
                session['message'] = "用户名/密码错误" # 登陆失败，返回提示信息
                return redirect(url_for("app.view.login"))
    session['token'] = ''.join(sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 10))
    return render_template("login.html", token=session['token'], message=session.pop('message', default=None))


@view.route("/advance_search")
def advance():
    return render_template("advance.html")


@view.route("/result")
@view.route("/result/")
@view.route("/result/<int:page>")
def advance_result(page=1):
    book = Book.query
    try:
        if 'name' in request.args:
            for i in request.args['name'].split(' '):
                book = book.filter(Book.name.ilike('%%%s%%' % i))
        if 'type' in request.args:
            book = book.filter(Book.name.ilike('%%%s%%' % request.args['type']))
        if 'author' in request.args:
            book = book.filter(Book.name.ilike('%%%s%%' % request.args['author']))
        if 'publisher' in request.args:
            book = book.filter(Book.name.ilike('%%%s%%' % request.args['publisher']))
        if 'year' in request.args and request.args['year'] != '':
            years = re.findall(r'(\d{4})', request.args['year'])
            if len(years) == 1:
                book = book.filter_by(year=int(years[0]))
            else:
                if int(years[0]) > int(years[1]):
                    book = book.filter(Book.year.between(int(years[1]), int(years[0])))
                else:
                    book = book.filter(Book.year.between(int(years[0]), int(years[1])))
            if len(re.findall(r'[a-zA-Z]', request.args['year'])) != 0:
                return "<script> alert('输入中不能有英文字符！'); window.location='/advance_search';</script>"
        if 'price' in request.args and request.args['price'] != '':
            prices = re.findall(r'(\d+\.?\d*)', request.args['price'])
            if len(prices) == 1:
                book = book.filter_by(prices=float(prices[0]))
            else:
                if float(prices[0]) > float(prices[1]):
                    book = book.filter(Book.price.between(float(prices[1]), float(prices[0])))
                else:
                    book = book.filter(Book.price.between(float(prices[0]), float(prices[1])))
            if len(re.findall(r'[a-zA-Z]', request.args['price'])) != 0:
                return "<script> alert('输入中不能有英文字符！'); window.location='/advance_search';</script>"
    except Exception:
        return "<script> alert('查询错误！'); window.location='/advance_search';</script>"
    order = 1 if 'order' not in request.args else int(request.args['order'])
    book = book.order_by([Book.name.asc(), Book.type.asc(), Book.author.asc(),
                          Book.publisher.asc(), Book.year.asc(), Book.price.asc()][order - 1])
    result_set = list()
    pagination = book.paginate(page, per_page=current_app.config["PER_PAGE"])
    book = pagination.items
    for i in book:
        result_set.append(i.to_dict())
    return render_template("result.html", result_set=result_set,
                           name='' if 'name' not in request.args else request.args['name'], pagination=pagination)


@view.route("/add", methods=['GET', "POST"])
@login_required
def add():
    if request.method == 'POST':
        try:
            form = request.form.to_dict(flat=True)
            book = Book(id=int(form['id']), type=form['type'], name=form['name'], publisher=form['publisher'],
                        year=int(form['year']), author=form['author'], price=float(form['price']),
                        amount=int(form['amount']))
            db.session.add(book)
            db.session.commit()
            return render_template("add.html", message="添加成功!")
        except Exception:
            return render_template('add.html', message="未知错误！")
    return render_template("add.html")


@view.route("/batch_add", methods=["GET", "POST"], strict_slashes=False)
@login_required
def batch_add():
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file and file.filename[-4:] == '.csv':
            count = 0
            datas = BytesIO(file.read()).read()
            encode = chardet.detect(datas)['encoding']
            datas = datas.decode(encode).replace('\r\n', '\n')
            for l in datas.split('\n'):
                data = l.split(',')
                try:
                    book = Book(id=int(data[0]), type=data[1], name=data[2], publisher=data[3], year=data[4],
                                author=data[5], price=data[6], amount=data[7])
                except Exception:
                    return '<script>alert("处理行\\n'+ l + '\\n时发生问题，请检查文件！，确保以英文逗号分割。该行之前部分记录已经添加成功！"); window.location="/add";</script>'
                try:
                    db.session.add(book)
                    db.session.commit()
                except Exception:
                    return '<script>alert("处理行\\n'+ l + '\\n时发生问题，添加入数据库失败，请检查数据book_id是否有重复。部分记录添加成功"); window.location="/add";</script>'
                count += 1
            return render_template("add.html", message="添加%d套书籍成功成功！" % count)
        else:
            return render_template('add.html', message="文件不合法！")
    return redirect(url_for('app.view.add'))


@view.route("/delete_reader", methods=["POST"])
@login_required
def delete_reader():
    r = Reader.query.filter_by(id=request.form.get('id', default=0, type=int)).first()
    record = db.session.execute("SELECT count(*) from records WHERE `reader_id`=:rid AND `receive_date` IS NULL;", {'rid': r.id}).first()[0]
    if record != 0:
        session['message'] = "该读者有未还书目！无法删除！"
        return redirect(url_for('app.view.reader'))
    if r is None:
        session['message'] = "未找到该读者"
        return redirect(request.form['next'])
    db.session.execute("DELETE FROM records WHERE `reader_id`=:rid", {"rid": r.id})
    db.session.delete(r)
    db.session.commit()
    session['message'] = "删除成功"
    return redirect(request.form['next'])


@view.route("/reader", methods=["POST", "GET"])
@view.route("/reader/<int:page>", methods=["POST", "GET"])
@login_required
def reader(page=1):
    # TODO: manage the reader information
    if 'message' in session:
        message = session.pop('message')
    else:
        message = None
    if request.method == "POST":
        try:
            if request.form['name'] == '' or request.form['department'] == '':
                session['message'] = "必填字段不能为空！"
                return redirect(request.url)
            r = Reader(name=request.form['name'], department=request.form['department'], type=["学生", "教师"][request.form.get('type', type=int, default=1)-1])
            db.session.add(r)
            db.session.commit()
            message = "添加成功"
        except Exception:
            message = "添加失败"
        session['message'] = message
        return redirect(request.url)
    pagination = Reader.query.paginate(page, per_page=current_app.config["PER_PAGE"], error_out=False)
    datas = pagination.items

    while len(datas) == 0 and page != 1:
        page -= 1
        pagination = Reader.query.paginate(page, per_page=current_app.config["PER_PAGE"], error_out=False)
        datas = pagination.items
    pagination.iter_pages(left_current=1, left_edge=1, right_current=1, right_edge=1)
    result_set = []
    for i in datas:
        result_set.append(i.to_dict())
    return render_template('reader.html', result_set=result_set, pagination=pagination, message=message)


@view.route("/borrow", methods=["GET"])
@login_required
def borrow():
    # TODO: get check reader info and return the book list
    if 'message' in session:
        message = session.pop('message')
    else:
        message = None
    if 'reader_id' in request.args:
        reader_id = request.args['reader_id']
        r = Reader.query.filter_by(id=reader_id).first()
        if r is None:
            session['message'] = "未找到该读者"
            return redirect(url_for("app.view.borrow"))
        books = db.session.execute("SELECT books.id,books.type,books.name,books.publisher,books.year,"
                                   "books.author,books.price,books.amount,"
                                   "records.borrow_date, records.admin_id, books.store "
                                   "FROM records INNER JOIN books ON records.book_id = books.id "
                                   "WHERE records.reader_id=:rid AND records.receive_date is NULL", {'rid': r.id})
        result_set = []
        for i in books:
            result_set.append(
                {
                    'id': i[0],
                    'type': i[1],
                    'name': i[2],
                    'publisher': i[3],
                    'year': i[4],
                    'author': i[5],
                    'price': i[6],
                    'amount': i[7],
                    'borrow': i[8],
                    'admin': Admin.query.filter_by(id=int(i[9])).first().name,
                    'store': i[10],
                    'return': False,
                }
            )
        books = db.session.execute("SELECT books.id,books.type,books.name,books.publisher,books.year,"
                                   "books.author,books.price,books.amount,"
                                   "records.borrow_date, records.admin_id, books.store, records.receive_date "
                                   "FROM records INNER JOIN books ON records.book_id = books.id "
                                   "WHERE records.reader_id=:rid AND records.receive_date is NOT NULL", {'rid': r.id})
        for i in books:
            result_set.append(
                {
                    'id': i[0],
                    'type': i[1],
                    'name': i[2],
                    'publisher': i[3],
                    'year': i[4],
                    'author': i[5],
                    'price': i[6],
                    'amount': i[7],
                    'borrow': i[8],
                    'admin': Admin.query.filter_by(id=int(i[9])).first().name,
                    'store': i[10],
                    'date': i[11],
                    'return': True,
                }
            )
        return render_template("borrow.html", reader=r.to_dict(), message=message, result_set=result_set)
    return render_template("borrow.html", message=message)


@view.route("/exec", methods=["POST"])
@login_required
def exec_borrow():
    reader_id = request.form['user']
    if int(request.form['exec']) == 1:
        # 检查该读者是否借过该书且未还
        result = int(db.session.execute("SELECT count(*) from records INNER JOIN readers ON records.reader_id = readers.id "
                          "WHERE records.book_id=:id AND records.receive_date IS NULL AND records.reader_id=:rid",
                                        {"id": request.form['book_id'], 'rid': reader_id }).first()[0])
        if result != 0:
            session['message'] = '该读者已借阅过该书！'
            return redirect(url_for("app.view.borrow", reader_id=reader_id))

        # 检查是否有书可借
        book = Book.query.filter_by(id=request.form['book_id']).first()
        if book is None:
            session['message'] = '馆内查无此书！'
            return redirect(url_for("app.view.borrow", reader_id=reader_id))
        if book.store <= 0:
            record = Record.query.filter_by(book_id=book.id).order_by(Record.receive_date.desc()).first().receive_date
            if record is None:
                record = "无记录"
            session['message'] = '库存不足！ 最后还书时间:%s' % record
            return redirect(url_for("app.view.borrow", reader_id=reader_id))
        record = Record(reader_id=reader_id, book_id=request.form['book_id'], admin_id=current_user.id)
        book.store -= 1
        db.session.add(record)
        db.session.add(book)
        db.session.commit()
        session['message'] = '借阅成功！'
    if int(request.form['exec']) == 2:
        record = Record.query.filter_by(reader_id=reader_id, book_id=request.form['book_id'], receive_date=None).first()
        if record is None:
            session['message'] = "未找到借阅未还记录！"
            return redirect(url_for("app.view.borrow", reader_id=reader_id))
        book = Book.query.filter_by(id=request.form['book_id']).first()
        if book is None:
            session['message'] = "查无此书！"
            return redirect(url_for("app.view.borrow", reader_id=reader_id))
        book.store += 1
        record.receive_date = datetime.now()
        db.session.add(record)
        db.session.add(book)
        db.session.commit()
        session['message'] = "还书成功！"
    return redirect(url_for("app.view.borrow", reader_id=reader_id))


@view.route("/manage")
@login_required
def manage():
    return render_template("manage.html")