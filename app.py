from flask import Flask, render_template, request, redirect, flash, session
from surveys import satisfaction_survey as survey
from flask_debugtoolbar import DebugToolbarExtension

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def show_survey_selection():
    """Select Survey"""
    return render_template('select_survey.html', survey=survey)


@app.route('/begin', methods=["POST"])
def start_survey():


    session[RESPONSES_KEY] = []

    return redirect('/questions/0')

@app.route('/answer', methods=["POST"])
def handle_question():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    if (len(responses) != qid):
        """Insert a Message"""
        flash(f"Invalid question: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app.route('/complete')
def complete():
    return render_template("completion.html")


