from flask_wtf import Form
from wtforms import TextField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired

#New Flask form
class newSuggestionForm(Form):
  sType = SelectField('Suggestion Type', choices=[('Other', 'Other'), ('DC', 'DC'), ('Logos', 'Logos'), ('Home', 'Home')], validate_choice=True)
  title = TextField('Title', validators=[DataRequired()])
  desc = TextAreaField('Description', validators=[DataRequired()])

class newLoginForm(Form):
  username = TextField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
