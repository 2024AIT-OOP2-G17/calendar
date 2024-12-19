from flask import Blueprint, render_template, request, redirect, url_for
import datetime
import calendar

# Blueprintの作成
index_bp = Blueprint('index', __name__, url_prefix='')


@index_bp.route('/')
def list():
    # データ取得
    today = datetime.date.today()
    year = today.year
    month = today.month
    date = today.day

    calender = calendar.Calendar(firstweekday=0)
    thisMonth = calendar.monthdayscalendar(year, month)
    
    return render_template('calender.html',
                            month = thisMonth)
