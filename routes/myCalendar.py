from flask import Blueprint, render_template, request, redirect, url_for
import datetime
import calendar
from models.eventCalendar import EventCalendar
from models.make import Make

# Blueprintの作成
myCalendar_bp = Blueprint('myCalendar', __name__, url_prefix='')


@myCalendar_bp.route('/')
def list():

    # カレンダー名
    originalName = "\"好きな名前\""

    # 曜日のデータ準備
    days = ['月', '火', '水', '木', '金', '土', '日']

    # 日付のデータ取得
    today = datetime.date.today()
    year = today.year
    month = today.month
    date = today.day

    # カレンダーのデータ取得
    cal = calendar.Calendar(firstweekday=0)
    my_calendar = cal.monthdayscalendar(year, month)
    
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
    
    return render_template('myCalendar.html',
                            originalName = originalName,
                            days = days,
                            month = month,
                            today = date,
                            my_calendar = my_calendar,
                            upcoming_tasks = upcoming_tasks
                            )

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

@myCalendar_bp.route('/make', methods=['GET','POST'])
def make():
    
    if request.method == 'POST':
        title = request.form['title']
        Make.create(title = title)
        return redirect(url_for('myCalender.list'))
    
    return render_template('calender_make.html')
