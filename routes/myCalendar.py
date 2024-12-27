from flask import Blueprint, render_template, request, redirect, url_for
import datetime
import calendar
from models.myCalendar import MyCalendar

# Blueprintの作成
myCalendar_bp = Blueprint('myCalendar', __name__, url_prefix='')

@myCalendar_bp.route('/')
def list():
    calendars=MyCalendar.select()

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
                            my_calendar = my_calendar,
                            title='calendar',
                            items=calendars)

@myCalendar_bp.route('/add')
def add():
    if request.method=='POST':
        name=request.form['name']
        date=request.form['date']
        MyCalendar.create(name=name,date=date)
        redirect(url_for('myCalendar'))
    return render_template('myCalendar.add')
