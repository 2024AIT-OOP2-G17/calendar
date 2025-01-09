from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import calendar
from datetime import datetime
from models.eventCalendar import EventCalendar


# Blueprintの作成
myCalendar_bp = Blueprint('myCalendar', __name__, url_prefix='')

@myCalendar_bp.route('/')
def list():
    #test出力
    print(f"今日の日付: {datetime.today().strftime('%Y-%m-%d')}")
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    current_date = today.day

    # データベースから全てのタスクを取得
    tasks = EventCalendar.select()
    
    # 今日以降の期限のタスクをフィルタリングしたいけどできてない気がする
    upcoming_tasks = []
    for task in tasks:
        # 月と日から日付オブジェクトを作成
        task_date = datetime(current_year, task.add_month, task.add_day)
        today_date = datetime(current_year, current_month, current_date)
        
        # 過去の日付の場合は来年の日付として扱う
        if task_date < today_date:
            task_date = datetime(current_year + 1, task.add_month, task.add_day)
            
        # 更新された task_date を使って比較
        if task_date >= today_date:
            # タスクに並び替え用の日付情報を追加
            task.sort_date = task_date
            upcoming_tasks.append(task)
    
    # 日付でソート（更新された日付情報を使用）
    upcoming_tasks.sort(key=lambda x: x.sort_date)
    
    # 最初の3つのタスクのみを取得
    upcoming_tasks = upcoming_tasks[:3]
    
    return render_template('myCalendar.html', upcoming_tasks=upcoming_tasks)

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
        
        # 予定を保存
        event = EventCalendar(
            add_month=month,
            add_day=day,
            add_title=title,
            add_todo=todo
        )
        event.save()

        return redirect(url_for('myCalendar.list'))
    
    return render_template('myCalendar_add.html')
