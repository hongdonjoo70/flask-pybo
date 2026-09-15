from datetime import datetime
from pybo import db
from flask import Blueprint, request, redirect, url_for, render_template

from pybo.forms import AnswerForm
from pybo.models import Question, Answer

bp=Blueprint('answer', __name__,url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=['POST'])
def create(question_id):
    question = Question.query.get_or_404(question_id)
    # content = request.form.get('content')
    form = AnswerForm()
    if form.validate_on_submit():
        content = form.content.data
        answer = Answer(content=content,create_date=datetime.now())
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for("question.detail", question_id=question_id))

    return redirect(url_for("question.detail", question=question, form=form))
