from flask import Blueprint, render_template
import os
import sqlite3
from .forms import AppointmentForm

bp = Blueprint('main', __name__, url_prefix="/hola")
DB_FILE = os.environ.get("DB_FILE")

@bp.route("/aa", methods=["GET", "POST"])
def main():
    form = AppointmentForm()
    if form.validate_on_submit():
        name = str(form.name.data)
        start_datetime = str(form.start_date.data) + ' ' + str(form.start_time.data)
        end_datetime = str(form.end_date.data) + ' ' + str(form.end_time.data)
        description = str(form.description.data)
        private = str(form.private.data)
        with sqlite3.connect(DB_FILE) as conn:
            curs = conn.cursor()
            # curs.execute(f'''INSERT INTO appointments (name, start_datetime, end_datetime, description, private) VALUES ({name}, {start_datetime}, {end_datetime}, {description}, {private});''')
            curs.execute("""INSERT INTO appointments (name, start_datetime, end_datetime, description, private) \
                VALUES (:name, :start_datetime, :end_datetime, :description, :private);""",
                {'name': name, 'start_datetime':start_datetime, 'end_datetime':end_datetime, 'description':description, 'private':private})

    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute('SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime;')
        appointments = curs.fetchall()

    # print('\n\n\n\n',appointments,'\n\n\n\n\n')
    return render_template('main.html', rows=appointments, form=form)
