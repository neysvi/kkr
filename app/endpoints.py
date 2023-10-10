from flask import jsonify, request, url_for, send_from_directory, current_app, make_response, session
from sqlalchemy import asc
import os
from werkzeug.utils import secure_filename

from app import app, db
from app.storages import PatientData, statistics, StatisticsData, User
from app.utils import login_required


@app.route('/get_data', methods=['GET'])
@login_required
def get_data():
    patient_data = PatientData.query.order_by(asc(PatientData.id)).all()

    return jsonify([{
        'id': patient.id,
        'create_date': patient.create_date,
        'doctor': patient.doctor,
        'number': patient.get_patient_number(),
        'full_name': patient.full_name,
        'gender': patient.gender,
        'birth_date': patient.birth_date,
        'age': patient.age,
        'diagnosis_mkb': patient.diagnosis_mkb,
        'operation_date': patient.operation_date,
        'operation_name': patient.operation_name,
        'intervention_level': patient.intervention_level,
        'time_between_primary_and_revision_operation': patient.time_between_primary_and_revision_operation,
        'neurological_deficit': patient.neurological_deficit,
        'charlson_index': patient.charlson_index,
        'vash_before_operation': patient.vash_before_operation,
        'vash_1_month_after_operation': patient.vash_1_month_after_operation,
        'vash_3_months_after_operation': patient.vash_3_months_after_operation,
        'vash_6_months_after_operation': patient.vash_6_months_after_operation,
        'vash_12_months_after_operation': patient.vash_12_months_after_operation,
        'odi_before_operation': patient.odi_before_operation,
        'odi_1_month_after_operation': patient.odi_1_month_after_operation,
        'odi_3_months_after_operation': patient.odi_3_months_after_operation,
        'odi_6_months_after_operation': patient.odi_6_months_after_operation,
        'odi_12_months_after_operation': patient.odi_12_months_after_operation,
        'sf_before_operation': patient.sf_before_operation,
        'sf_1_month_after_operation': patient.sf_1_month_after_operation,
        'sf_3_months_after_operation': patient.sf_3_months_after_operation,
        'sf_6_months_after_operation': patient.sf_6_months_after_operation,
        'sf_12_months_after_operation': patient.sf_12_months_after_operation,
        'ct_before_operation': patient.ct_before_operation,
        'crb': patient.crb,
        'osteoporosis': patient.osteoporosis,
        'height': patient.height,
        'weight': patient.weight,
        'bmi': patient.bmi,
        'intraoperative_culture_result': patient.intraoperative_culture_result,
        'asa_risk': patient.asa_risk,
        'blood_group': patient.blood_group,
        'rh_factor': patient.rh_factor,
        'complications': patient.complications,
        'mcnab_scale': patient.mcnab_scale,
        'initial_platelet_level': patient.initial_platelet_level,
        'final_platelet_level': patient.final_platelet_level,
        'final_thrombogel_volume': patient.final_thrombogel_volume,
        'alloimmunity': patient.alloimmunity
    } for patient in patient_data])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    uploads = os.path.join(current_app.root_path)
    path = f"{app.config['UPLOAD_FOLDER']}{filename}"
    return send_from_directory(uploads, path)


@app.route('/insert_data', methods=['POST'])
# @login_required
def insert_data():
    data = request.form

    file = request.files['ct_before_operation']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        file_url = url_for('uploaded_file', filename=filename, _external=True)
    else:
        return jsonify({"message": "Недопустимый файл"}), 400

    new_patient = PatientData(
        full_name=data.get('full_name'),
        gender=data.get('gender'),
        birth_date=data.get('birth_date'),
        age=data.get('age'),
        diagnosis_mkb=data.get('diagnosis_mkb'),
        operation_date=data.get('operation_date'),
        operation_name=data.get('operation_name'),
        intervention_level=data.get('intervention_level'),
        time_between_primary_and_revision_operation=data.get('time_between_primary_and_revision_operation'),
        neurological_deficit=bool(data.get('neurological_deficit')),
        charlson_index=data.get('charlson_index'),
        vash_before_operation=data.get('vash_before_operation'),
        vash_1_month_after_operation=data.get('vash_1_month_after_operation'),
        vash_3_months_after_operation=data.get('vash_3_months_after_operation'),
        vash_6_months_after_operation=data.get('vash_6_months_after_operation'),
        vash_12_months_after_operation=data.get('vash_12_months_after_operation'),
        odi_before_operation=data.get('odi_before_operation'),
        odi_1_month_after_operation=data.get('odi_1_month_after_operation'),
        odi_3_months_after_operation=data.get('odi_3_months_after_operation'),
        odi_6_months_after_operation=data.get('odi_6_months_after_operation'),
        odi_12_months_after_operation=data.get('odi_12_months_after_operation'),
        sf_before_operation=data.get('sf_before_operation'),
        sf_1_month_after_operation=data.get('sf_1_month_after_operation'),
        sf_3_months_after_operation=data.get('sf_3_months_after_operation'),
        sf_6_months_after_operation=data.get('sf_6_months_after_operation'),
        sf_12_months_after_operation=data.get('sf_12_months_after_operation'),
        ct_before_operation=file_url,
        crb=data.get('crb'),
        osteoporosis=data.get('osteoporosis'),
        height=data.get('height'),
        weight=data.get('weight'),
        bmi=data.get('bmi'),
        intraoperative_culture_result=bool(data.get('intraoperative_culture_result')),
        asa_risk=data.get('asa_risk'),
        blood_group=data.get('blood_group'),
        rh_factor=bool(data.get('rh_factor')),
        complications=data.get('complications'),
        mcnab_scale=data.get('mcnab_scale'),
        initial_platelet_level=data.get('initial_platelet_level'),
        final_platelet_level=data.get('final_platelet_level'),
        final_thrombogel_volume=data.get('final_thrombogel_volume'),
        alloimmunity=bool(data.get('alloimmunity'))
    )

    db.session.add(new_patient)
    db.session.commit()
    statistics()

    return jsonify({"message": "Данные успешно добавлены в базу данных"}), 201


@app.route('/delete_data/<int:id>', methods=['DELETE'])
# @login_required
def delete_data(id):
    patient = PatientData.query.get(id)

    if patient:
        db.session.delete(patient)
        db.session.commit()
        statistics()
        return jsonify({"message": "Запись успешно удалена"}), 200
    else:
        return jsonify({"error": "Запись не найдена"}), 404


@app.route('/edit_data/<int:id>', methods=['PUT'])
# @login_required
def edit_data(id):
    patient = PatientData.query.get(id)
    data = request.form.to_dict()

    # Удалите лишние кавычки из строковых значений
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.strip('"')

    file = request.files.get('ct_before_operation')

    if file:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            file.save(file_path)

            file_url = url_for('uploaded_file', filename=filename, _external=True)

            patient.ct_before_operation = file_url
        else:
            return jsonify({"message": "Недопустимый файл"}), 400

    if patient:
        patient.full_name = data.get('full_name')
        patient.gender = data.get('gender')
        patient.birth_date = data.get('birth_date')
        patient.age = data.get('age')
        patient.diagnosis_mkb = data.get('diagnosis_mkb')
        patient.operation_date = data.get('operation_date')
        patient.operation_name = data.get('operation_name')
        patient.intervention_level = data.get('intervention_level')
        patient.time_between_primary_and_revision_operation = data.get('time_between_primary_and_revision_operation')
        patient.neurological_deficit = bool(data.get('neurological_deficit'))
        patient.charlson_index = data.get('charlson_index')
        patient.vash_before_operation = data.get('vash_before_operation')
        patient.vash_1_month_after_operation = data.get('vash_1_month_after_operation')
        patient.vash_3_months_after_operation = data.get('vash_3_months_after_operation')
        patient.vash_6_months_after_operation = data.get('vash_6_months_after_operation')
        patient.vash_12_months_after_operation = data.get('vash_12_months_after_operation')
        patient.odi_before_operation = data.get('odi_before_operation')
        patient.odi_1_month_after_operation = data.get('odi_1_month_after_operation')
        patient.odi_3_months_after_operation = data.get('odi_3_months_after_operation')
        patient.odi_6_months_after_operation = data.get('odi_6_months_after_operation')
        patient.odi_12_months_after_operation = data.get('odi_12_months_after_operation')
        patient.sf_before_operation = data.get('sf_before_operation')
        patient.sf_1_month_after_operation = data.get('sf_1_month_after_operation')
        patient.sf_3_months_after_operation = data.get('sf_3_months_after_operation')
        patient.sf_6_months_after_operation = data.get('sf_6_months_after_operation')
        patient.sf_12_months_after_operation = data.get('sf_12_months_after_operation')
        patient.crb = data.get('crb')
        patient.osteoporosis = data.get('osteoporosis')
        patient.height = data.get('height')
        patient.weight = data.get('weight')
        patient.bmi = data.get('bmi')
        patient.intraoperative_culture_result = bool(data.get('intraoperative_culture_result'))
        patient.asa_risk = data.get('asa_risk')
        patient.blood_group = data.get('blood_group')
        patient.rh_factor = bool(data.get('rh_factor'))
        patient.complications = data.get('complications')
        patient.mcnab_scale = data.get('mcnab_scale')
        patient.initial_platelet_level = data.get('initial_platelet_level')
        patient.final_platelet_level = data.get('final_platelet_level')
        patient.final_thrombogel_volume = data.get('final_thrombogel_volume')
        patient.alloimmunity = bool(data.get('alloimmunity'))

        db.session.commit()
        statistics()
        return jsonify({"message": "Запись успешно обновлена"}), 200
    else:
        return jsonify({"error": "Запись не найдена"}), 404


@app.route('/get_stat', methods=['GET'])
# @login_required
def get_stat():
    stat_data = StatisticsData.query.order_by(asc(StatisticsData.id)).all()

    return jsonify([{
        'id': stat.id,
        'column_name': stat.column_name,
        'mean': stat.mean,
        'median': stat.median,
        'confidence_interval_min': stat.confidence_interval_min,
        'confidence_interval_max': stat.confidence_interval_max,
        'standard_deviation': stat.standard_deviation
    } for stat in stat_data])


# Авторизация
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_email = data.get('user_email')
    user_password = data.get('user_password')

    user = User.query.filter_by(user_email=user_email).first()
    if user and user.check_password(user_password):
        session["user_id"] = user.id

        return jsonify({"message": "Успешная аутентификация", 'username': user.user_name}), 200
    else:
        return jsonify({"message": "Неверные данные"}), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_name = data.get('user_name')
    user_email = data.get('user_email')
    user_password = data.get('user_password')

    existing_user = User.query.filter_by(user_email=user_email).first()
    if existing_user:
        return jsonify({"message": "Пользователь с таким email уже существует"}), 400

    new_user = User(user_name=user_name, user_email=user_email)
    new_user.set_password(user_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Пользователь успешно зарегистрирован"}), 201
