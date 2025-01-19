from flask import Blueprint, render_template, request, flash, jsonify,app
from flask_login import login_required, current_user
from .models import Note
from .models import Record
from .models import MpesaSTKPush
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/add-patient')
@login_required
def add_patient():
    return render_template("add_patient.html", user=current_user)


@views.route('/add-record', methods=['POST'])
@login_required
def add_record():
    record = json.loads(request.data)
    new_record = Record(
        patientName=record['patientName'],
        phoneNumber=record['phoneNumber'],
        note=record['note'],
        paymentMethod=record['paymentMethod'],
        amount=record['amount'],
        user_id=current_user.id
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify({'success': True})

@views.route('/get-records')
@login_required
def get_records():
    records = Record.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': record.id,
        'patientName': record.patientName,
        'phoneNumber': record.phoneNumber,
        'note': record.note,
        'paymentMethod': record.paymentMethod,
        'amount': record.amount,
        'date': record.date.strftime("%Y-%m-%d %H:%M:%S")
    } for record in records])

@views.route('/delete-record', methods=['POST'])
@login_required
def delete_record():
    record_data = json.loads(request.data)
    record_id = record_data['recordId']
    record = Record.query.get(record_id)
    if record and record.user_id == current_user.id:
        db.session.delete(record)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

@views.route('/mpesa-payment')
@login_required
def mpesa_payment():
    return render_template('mpesa_payment.html', user=current_user)
@views.route('/mpesa-callback', methods=['POST'])
def mpesa_callback():
    callback_data = request.json
   
    return jsonify({'status': 'success'})


@views.route('/initiate-mpesa-payment', methods=['POST'])
@login_required
def initiate_mpesa_payment():
    data = request.get_json()
    phone_number = data.get('phone_number')
    amount = data.get('amount')
    
    mpesa = MpesaSTKPush()
    response = mpesa.initiate_stk_push(phone_number=phone_number, amount=amount)
    
    return jsonify({'success': True, 'response': response})

from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash

@views.route('/update-password', methods=['POST'])
@login_required
def update_password():
    data = request.get_json()
    
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')
    
    # Verify current password
    if not check_password_hash(current_user.password, current_password):
        return jsonify({'success': False, 'message': 'Current password is incorrect'})
    
    # Update password
    current_user.password = generate_password_hash(new_password)
    db.session.commit()
    
    return jsonify({'success': True})
