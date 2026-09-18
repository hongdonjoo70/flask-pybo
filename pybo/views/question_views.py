from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, g,flash

from pybo import db
from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question,Answer,User
from pybo.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list')
def _list():
    page = request.args.get('page', default=1, type=int) # 페이지
    kw = request.args.get('kw', default='', type=str)  # 검색키워드 추가
    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username)\
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list.join(User)\
            .outerjoin(sub_query, sub_query.c.question_id == Question.id)\
            .filter(Question.subject.ilike(search) |    # 질문제목
                    Question.content.ilike(search) |    # 질문내용
                    User.username.ilike(search) |       # 질문작성자
                    sub_query.c.content.ilike(search) | # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    )\
            .distinct()
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html',question_list=question_list, page=page, kw=kw)

@bp.route('/detail/<int:question_id>')
def detail(question_id):
    form=AnswerForm()
    question = Question.query.get_or_404(question_id)
    # return render_template('question/question_detail.html', question=question,form=form)
    return render_template('question/question_detail.html', question=question,form=form)

@bp.route('/create',methods=['GET','POST'])
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question=Question(subject=form.subject.data,content=form.content.data,create_date=datetime.now(),user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for ('main.index'))
    return render_template("question/question_form.html",form=form)

@bp.route('/modify/<int:question_id>', methods=['GET','POST'])
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash ("수정권한이 없습니다.")
        return redirect(url_for("question.detail", question_id=question.id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for("question.detail", question_id=question.id))
    else:
        form = QuestionForm(obj=question)
        return render_template("question/question_form.html",form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash ("삭제권한이 없습니다.")
        return redirect(url_for("question.detail", question_id=question.id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("question._list"))
