from flask import Blueprint, render_template, request, redirect, url_for
import datetime
import calendar
from models import EventCalendar

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
    
    return render_template('myCalendar.html',
                            originalName = originalName,
                            days = days,
                            month = month,
                            today = date,
                            my_calendar = my_calendar
                            )

@myCalendar_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':

        month = int(request.form['add_month'])
        day = int(request.form['add_day'])
        title = request.form['add_title']
        todo = request.form['add_todo']
        EventCalendar.create(add_month=month, add_day=day, add_title=title, add_todo=todo)
        return redirect(url_for('myCalendar.list'))
    
    return render_template('myCalendar_add.html')