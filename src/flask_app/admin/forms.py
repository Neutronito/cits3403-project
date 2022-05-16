from flask_wtf import FlaskForm
from wtforms import TextAreaField, DateField, SubmitField, IntegerField
from wtforms import validators

class newMapForm(FlaskForm):
    map = TextAreaField('Map', validators=[validators.DataRequired()])
    width = IntegerField('Width', validators=[validators.DataRequired()])
    height = IntegerField('Height', validators=[validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()])
    submit = SubmitField('Insert New Map')

    def validate_date(self, date):
        from flask_app.game.models import Map

        if Map.get_map(date.data) is not None:
            raise validators.ValidationError("There is already a map at this date.")
