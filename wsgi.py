import db.db_manager as db
import db.code_search as search
import api.netto_client as netto
from helper.constants import *
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'

client = netto.Client()

if __name__ == '__main__':
    app.run()

with app.app_context():
    db.init()
    search.CodeSearch().start()


@app.route('/', methods=('GET', 'POST'))
def index():
    codes = db.get_codes(COUPON_TYPE_NCP)
    if request.method == 'POST':
        if request.form['email'] is None:
            call_flash(EMAIL_MISSING)
        elif request.form['code'] is None or not db.exists_code(request.form['code']):
            call_flash(CODE_NOT_FOUND)
        elif db.is_activated(request.form['email'], request.form['code']):
            call_flash(CODE_ALREADY_USED)
        else:
            message = activate_code(request.form['code'], request.form['email'])
            db.save_history(request.form['email'], request.form['code'], message)
            call_flash(message)
    return render_template('index.html', codes=codes)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def activate_code(code: str, email: str) -> str:
    return client.activate_code(code, email)['message']


def call_flash(message: str):
    flash(message, 'message' if message == CODE_SUCCESS else 'error')
