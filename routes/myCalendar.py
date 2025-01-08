from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import calendar
from models import EventCalendar


# Blueprintの作成
myCalendar_bp = Blueprint('myCalendar', __name__, url_prefix='')

@myCalendar_bp.route('/')
def list():
    return render_template('myCalendar.html')

@myCalendar_bp.route("/create_calendar", methods=['GET'])
def createCalendar():
    # 現在の年月を取得
    # 日付のデータ取得
    month = int(request.args.get("month"))
    year = int(request.args.get("year"))
    move = int(request.args.get("move"))

    # 月の変更
    month += move

    # 年月の調整
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    # カレンダー生成
    cal = calendar.Calendar()
    my_calendar = cal.monthdayscalendar(year, month)

    # データの取得
    events = EventCalendar.select().where(
        EventCalendar.add_month == month
        ).order_by(EventCalendar.add_day.asc())
    
    # 結果を辞書に変換
    schedules = []
    for event in events:
        schedule = event.__data__  # モデルのインスタンスを辞書に変換
        schedules.append(schedule)


    # JSONでデータを返す
    return jsonify({"year": year, "month": month, "calendar": my_calendar, "schedules": schedules})

@myCalendar_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':

        month = int(request.form['add_month'])
        day = int(request.form['add_day'])
        title = request.form['add_title']
        todo = request.form['add_todo']
        EventCalendar(add_month=month, add_day=day, add_title=title, add_todo=todo).save()

        return redirect(url_for('myCalendar.list'))
    
    return render_template('myCalendar_add.html')
