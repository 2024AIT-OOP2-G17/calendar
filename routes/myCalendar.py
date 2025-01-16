from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import calendar
from datetime import datetime
from models.eventCalendar import EventCalendar
from models.make import Make


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

    # 作成したカレンダーのタイトルを取得
    makes = Make.select()
    
    # 最初の3つのタスクのみを取得
    upcoming_tasks = upcoming_tasks[:3]
    
    return render_template('myCalendar.html', upcoming_tasks = upcoming_tasks, items=makes)

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


@myCalendar_bp.route('/add/<int:ymd>', methods=['GET', 'POST'])
def add(ymd):
    
    if request.method == 'POST':

        year = int(ymd / 10000)
        month = int((ymd - year * 10000) / 100)
        day = ymd - (year * 10000) - (month * 100)
        title = request.form['add_title']
        todo = request.form['add_todo']
        
        # 予定を保存
        event = EventCalendar(
            add_year=year,
            add_month=month,
            add_day=day,
            add_title=title,
            add_todo=todo
        )
        event.save()

        return redirect(url_for('myCalendar'))
    
    return render_template('myCalendar_add.html', ymd = ymd)

@myCalendar_bp.route('/edit/<int:eventCalendar_id>',methods=['GET','POST'])
def edit(eventCalendar_id):
    calendar=EventCalendar.get_or_none(EventCalendar.id==eventCalendar_id)
    if not calendar:
        return redirect(url_for('myCalendar'))
    if request.method=='POST':
        calendar.month=request.form['month']
        calendar.day=request.form['day']
        calendar.title=request.form['title']
        calendar.todo=request.form['todo']
        calendar.save()
        return redirect(url_for('myCalendar'))
    return render_template('myCalendar_edit.html',calendar=calendar)

@myCalendar_bp.route('/make', methods=['GET','POST'])
def make():
    
    if request.method == 'POST':
        title = request.form['title']
        Make.create(title = title)
        return redirect(url_for('myCalendar.list'))
    
    return render_template('calender_make.html')

@myCalendar_bp.route('/edit/<int:eventCalendar_id>/achieve', methods=['GET'])
def achieve():
    # クエリパラメータを取得
    month=request.args.get('month')
    day=request.args.get('day')
    title=request.args.get('title')
    todo=request.args.get('todo')
    # 必要に応じて、取得データを処理またはデータベースに保存
    # 例: 完了済みタスクとしてフラグを設定する
    completed_event=EventCalendar.get_or_none(
        (EventCalendar.add_month==int(month))&
        (EventCalendar.add_day==int(day))&
        (EventCalendar.add_title==title)&
        (EventCalendar.add_todo==todo)
    )
    if completed_event:
        completed_event.is_completed=True  # 完了フラグ（仮想フィールド）
        completed_event.save()

    # 達成済みリストにデータを渡して表示
    data = f"{month}月{day}日: {title} - {todo}"
    return render_template('achieve_list.html', data=data)

