from flask_wtf import FlaskForm
from wtforms.fields import (BooleanField, DateField, StringField,SubmitField,TextAreaField,TimeField)
from wtforms.widgets import DateInput, TimeInput
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime, timedelta


def next_block(delta=0):
    def time():
        now = datetime.now()
        return now - timedelta(minutes=now.minute % 15 - delta - 15,
                               seconds=now.second)
    return time


di = {'default': datetime.now, 'widget': DateInput()}
sti = {'default': next_block(), 'widget': TimeInput()}
eti = {'default': next_block(60), 'widget': TimeInput()}


class AppointmentForm(FlaskForm):
    name = StringField("Name", [ DataRequired()])
    start_date = DateField("Start Date", [ DataRequired()], **di)
    start_time = DateField("Start Time", [ DataRequired()], **sti)
    end_date = DateField("End Date", [ DataRequired()], **di)
    end_time = DateField("End Time", [ DataRequired()], **sti)
    description = TextAreaField("description", [ DataRequired()])
    private = BooleanField("Private?", [ DataRequired()])
    submit = SubmitField("Create an appointment")

    def validate_end_date(form, field):
        start = datetime.combine(form.start_date.data, form.start_time.data)
        end = datetime.combine(field.data, form.end_time.data)
        if start >= end:
            msg = "End date/time must come after start date/time"
            raise ValidationError(msg)
        if form.start_date.data != form.end_date.data:
            msg = "End date must be the same as start date"
            raise ValidationError(msg)
