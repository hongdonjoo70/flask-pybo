from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired("필수 입력입니다.")])
    content= TextAreaField("내용",validators=[DataRequired("내용이 필요합니다.")])
    submit=SubmitField("저장하기")
