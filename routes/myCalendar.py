from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import calendar
from datetime import datetime
from models.eventCalendar import EventCalendar


# Blueprintの作成
myCalendar_bp = Blueprint('myCalendar', __name__, url_prefix='')

@myCalendar_bp.route('/')
def list():
    today = datetime.today()
    month = today.month
    date = today.day

    # データベースから全てのタスクを取得し、日付でソート
    tasks = EventCalendar.select().order_by(EventCalendar.add_month, EventCalendar.add_day)
    
    # 今日以降の期限のタスクをフィルタリング
    upcoming_tasks = [
        task for task in tasks 
        if (task.add_month > month) or 
           (task.add_month == month and task.add_day >= date)
    ]
    
    # 最初の3つのタスクのみを取得
    upcoming_tasks = upcoming_tasks[:3]
    
    return render_template('myCalendar.html', upcoming_tasks = upcoming_tasks)

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


@myCalendar_bp.route('/add/<int:month_day>', methods=['GET', 'POST'])
def add(month_day):
    
    if request.method == 'POST':

        if len(str(month_day)) == 3:
            month = int(str(month_day)[-3])
            day = month_day - int(str(month_day)[-3]) * 100
        else:
            month = int(month_day / 100)
            day = month_day - int(month_day / 100) * 100
        
        title = request.form['add_title']
        todo = request.form['add_todo']
        
        # 予定を保存
        event = EventCalendar(
            add_month=month,
            add_day=day,
            add_title=title,
            add_todo=todo
        )
        event.save()

        return redirect(url_for('myCalendar.list'))
    
    return render_template('myCalendar_add.html', month_day = month_day)
