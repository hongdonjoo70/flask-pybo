from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField, StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo,Email


class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired("필수 입력입니다.")])
    content= TextAreaField("내용",validators=[DataRequired("내용이 필요합니다.")])
    submit=SubmitField("저장하기")

class AnswerForm(FlaskForm):
    content=TextAreaField("내용",validators=[DataRequired("내용은 필수입니다.")])
    submit=SubmitField("답변등록")

class UserCreateForm(FlaskForm):
    username=StringField("사용자이름",validators=[DataRequired(),Length(3,25)])
    password1=PasswordField("비밀번호",validators=[DataRequired(),EqualTo("password2",message="비밀번호가 일치하지 않습니다.")])
    password2 = PasswordField("비밀번호확인", validators=[DataRequired()])
    email=EmailField("이메일",validators=[DataRequired(),Email()])
    submit=SubmitField("저장하기")

class UserLoginForm(FlaskForm):
    username=StringField("사용자 이름",validators=[DataRequired(),Length(3,25)])
    password = PasswordField("비밀번호", validators=[DataRequired()])
    submit = SubmitField("저장하기")