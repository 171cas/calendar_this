from flask import Blueprint, render_template
import os
import sqlite3
from .forms import AppointmentForm

bp = Blueprint('main', __name__, url_prefix="/")
DB_FILE = os.environ.get("DB_FILE")

@bp.route("/")
def main():
    form = AppointmentForm()
    # if form.validate_on_submit():
    #     print('\n\n\n\n', form, '\n\n\n\n\n')
        # with sqlite3.connect(DB_FILE) as conn:
        #     curs = conn.cursor()
        #     curs.execute('SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime;')
        #     appointments = curs.fetchall()

    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute('SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime;')
        appointments = curs.fetchall()
    # print('\n\n\n\n',appointments,'\n\n\n\n\n')
    return render_template('main.html', rows=appointments, form=form)
