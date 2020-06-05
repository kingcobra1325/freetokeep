# CREATED BY JOHN EARL COBAR

# lib imports
from flask import Flask, render_template, url_for, request, jsonify
import os,re,logging

# custom imports
from Main.database.database import list_game_db, register_email, delete_email, cleaner_desc
from Main.forms import FormRegister, FormDelete

################## INIT ##########################

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(128)

#################################################
###############  GET VIEWS ######################
#################################################

@app.route('/')
def index():
    return render_template('base.html',formR = FormRegister(),formD = FormDelete())

#################################################
##############  POST METHODS ####################
#################################################

# refresh game list
@app.route('/_refresh',methods=['POST'])
def _refresh():
    Games = cleaner_desc(list_game_db())
    return jsonify({'refresh':render_template('refresh.html',Games=Games)})

# register email
@app.route('/_register',methods=['POST'])
def _register():
    new_email = request.form.get('email')
    if new_email and re.match(r'[^@]+@[^@]+\.[^@]+',new_email):
        result = register_email(new_email)
        if result:
            print(f'{new_email} successfully registered')
            return jsonify({'message':f'{new_email} has been added to the mailing list. You will be receiving notifications about new free to keep games in the future!','alert':'alert alert-primary'})
        else:
            print(f'{new_email} is already registered')
            return jsonify({'message':f'Unable to add the email as of this time','alert':'alert alert-warning'})
    else:
        return jsonify({'message':f'Invalid input. Please try again','alert':'alert alert-warning'})

# delete email
@app.route('/_delete',methods=['POST'])
def _delete():
    demail = request.form.get('email')
    if demail and re.match(r'[^@]+@[^@]+\.[^@]+',demail):
        result = delete_email(demail)
        if result:
            print(f'{demail} successfully deleted')
            return jsonify({'message':f'{demail} has been deleted from the mailing list. You will stop receiving emails in the future!','alert':'alert alert-danger'})
        else:
            print(f'{demail} cannot be found')
            return jsonify({'message':f'Unable to delete the email as of this time','alert':'alert alert-warning'})
    else:
        return jsonify({'message':f'Invalid input. Please try again','alert':'alert alert-warning'})
