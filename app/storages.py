from sqlalchemy import func, DateTime
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from statistics import mean, median, stdev
from scipy import stats


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True)
    user_email = db.Column(db.String(64), unique=True)
    user_password = db.Column(db.String(128))

    def set_password(self, password):
        self.user_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.user_password, password)


class PatientData(db.Model):
    __tablename__ = 'patient_data'

    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(DateTime, default=datetime.utcnow, info={'label': 'Дата создания'})
    doctor = db.Column(db.String(255), info={'label': 'Пользователь'})
    full_name = db.Column(db.String(255), info={'label': 'ФИО'})
    gender = db.Column(db.Integer, info={'label': 'Пол'})
    birth_date = db.Column(db.Date, info={'label': 'Дата рождения'})
    age = db.Column(db.Integer, info={'label': 'Возраст'})
    height = db.Column(db.Float, info={'label': 'Рост'})
    weight = db.Column(db.Float, info={'label': 'Вес'})
    bmi = db.Column(db.Float, info={'label': 'BMI (индекс массы тела)'})
    diagnosis_mkb = db.Column(db.String(255), info={'label': 'Диагноз по МКБ'})
    operation_date = db.Column(db.Date, info={'label': 'Дата операции'})
    operation_name = db.Column(db.String(255), info={'label': 'Название операции'})
    intervention_level = db.Column(db.String(255), info={'label': 'Уровень вмешательства'})
    time_between_primary_and_revision_operation = db.Column(db.Float, info={'label': 'Время между первичной и ревизионной операцией'})
    neurological_deficit = db.Column(db.Integer, info={'label': 'Неврологический дефицит'})
    charlson_index = db.Column(db.Float, info={'label': 'Индекс коморбидности Чарлсона'})
    vash_before_operation = db.Column(db.Float, info={'label': 'ВАШ (визуально-аналоговая спина) до операции'})
    vash_1_month_after_operation = db.Column(db.Float, info={'label': 'ВАШ через 1 месяц после операции'})
    vash_3_months_after_operation = db.Column(db.Float, info={'label': 'ВАШ через 3 месяца после операции'})
    vash_6_months_after_operation = db.Column(db.Float, info={'label': 'ВАШ через 6 месяцев после операции'})
    vash_12_months_after_operation = db.Column(db.Float, info={'label': 'ВАШ через 12 месяцев после операции'})
    odi_before_operation = db.Column(db.Float, info={'label': 'ODI до операции'})
    odi_1_month_after_operation = db.Column(db.Float, info={'label': 'ODI через 1 месяц после операции'})
    odi_3_months_after_operation = db.Column(db.Float, info={'label': 'ODI через 3 месяца после операции'})
    odi_6_months_after_operation = db.Column(db.Float, info={'label': 'ODI через 6 месяцев после операции'})
    odi_12_months_after_operation = db.Column(db.Float, info={'label': 'ODI через 12 месяцев после операции'})
    sf_before_operation = db.Column(db.Float, info={'label': 'SF-36 до операции'})
    sf_1_month_after_operation = db.Column(db.Float, info={'label': 'SF-36 через 1 месяц после операции'})
    sf_3_months_after_operation = db.Column(db.Float, info={'label': 'SF-36 через 3 месяца после операции'})
    sf_6_months_after_operation = db.Column(db.Float, info={'label': 'SF-36 через 6 месяцев после операции'})
    sf_12_months_after_operation = db.Column(db.Float, info={'label': 'SF-36 через 12 месяцев после операции'})
    ct_before_operation = db.Column(db.String(255), info={'label': 'КТ (компьютерная томография) до операции'})
    ct_1_month_after_operation = db.Column(db.String(255), info={'label': 'КТ через 1 месяц после операции'})
    ct_3_months_after_operation = db.Column(db.String(255), info={'label': 'КТ через 3 месяца после операции'})
    ct_6_months_after_operation = db.Column(db.String(255), info={'label': 'КТ через 6 месяцев после операции'})
    ct_12_months_after_operation = db.Column(db.String(255), info={'label': 'КТ через 12 месяцев после операции'})
    crb = db.Column(db.Float, info={'label': 'СРБ (с-реактивный белок) до операции'})
    osteoporosis = db.Column(db.Float, info={'label': 'Остеопороз (HU)'})
    intraoperative_culture_result = db.Column(db.Integer, info={'label': 'Интраоперационный посев'})
    pathogen = db.Column(db.String(255), info={'label': 'Интраоперационный посев (возбудитель)'})
    asa_risk = db.Column(db.Integer, info={'label': 'Риск по ASA'})
    blood_group = db.Column(db.Integer, info={'label': 'Группа крови'})
    rh_factor = db.Column(db.Integer, info={'label': 'Резус-фактор'})
    complications = db.Column(db.String(255), info={'label': 'Осложнения'})
    mcnab_scale = db.Column(db.Integer, info={'label': 'Шкала Макнаб'})
    initial_platelet_level = db.Column(db.Float, info={'label': 'Исходный уровень тромбоцитов, *109/л'})
    final_platelet_level = db.Column(db.Float, info={'label': 'Конечный уровень тромбоцитов, *109/л'})
    final_thrombogel_volume = db.Column(db.Float, info={'label': 'Конечный объем тромбогеля, мл'})
    alloimmunity = db.Column(db.Integer, info={'label': 'Аллокость'})

    def calculate_bmi(self):
        if self.height and self.weight:
            height_meters = float(self.height) / 100  # Переводим рост из см в метры
            self.bmi = round(float(self.weight) / (height_meters ** 2), 2)
        else:
            self.bmi = None

    def get_patient_number(self):
        try:
            session = db.session
            row_number = (
                session.query(func.count(PatientData.id))
                .filter(PatientData.id <= self.id)
                .scalar()
            )
            return row_number
        except Exception as e:
            print(f"Ошибка при получении номера пациента: {str(e)}")
            return None


class StatisticsData(db.Model):
    __tablename__ = 'statistics_data'

    id = db.Column(db.Integer, primary_key=True)
    column_name = db.Column(db.String(255))
    mean = db.Column(db.Float)
    median = db.Column(db.Float)
    confidence_interval_min = db.Column(db.Float)
    confidence_interval_max = db.Column(db.Float)
    standard_deviation = db.Column(db.Float)


def statistics():
    numeric_columns = ["gender", "age", "height", "weight", "bmi", "time_between_primary_and_revision_operation", "neurological_deficit",
                       "charlson_index", "vash_before_operation", "vash_1_month_after_operation", "vash_3_months_after_operation",
                       "vash_6_months_after_operation", "vash_12_months_after_operation", "odi_before_operation",
                       "odi_1_month_after_operation", "odi_3_months_after_operation", "odi_6_months_after_operation",
                       "odi_12_months_after_operation", "sf_before_operation", "sf_1_month_after_operation",
                       "sf_3_months_after_operation", "sf_6_months_after_operation", "sf_12_months_after_operation",
                       "crb", "osteoporosis", "asa_risk", "blood_group", "rh_factor", "mcnab_scale",
                       "initial_platelet_level", "final_platelet_level", "final_thrombogel_volume", "alloimmunity"]

    if PatientData.query.count() < 2:
        return

    for column in numeric_columns:
        column_info = PatientData.__table__.columns[column].info
        column_label = column_info.get('label', column)

        values = [getattr(patient, column) for patient in PatientData.query.all() if
                  getattr(patient, column) is not None]

        if not values:
            continue

        values = [float(value) for value in values]

        avg_value = mean(values)
        median_value = median(values)

        if len(set(values)) == 1:
            std_deviation = 0
            confidence_interval = (avg_value, avg_value)
        else:
            std_deviation = stdev(values)
            confidence_interval = stats.t.interval(0.95, len(values) - 1, loc=avg_value, scale=std_deviation)

        statistics_data = StatisticsData.query.filter_by(column_name=column_label).first()
        if statistics_data:
            statistics_data.mean = avg_value
            statistics_data.median = median_value
            statistics_data.confidence_interval_min = '{:.2f}'.format(confidence_interval[0])
            statistics_data.confidence_interval_max = '{:.2f}'.format(confidence_interval[1])
            statistics_data.standard_deviation = std_deviation
        else:
            statistics_data = StatisticsData(
                column_name=column_label,
                mean=avg_value,
                median=median_value,
                confidence_interval_min='{:.2f}'.format(confidence_interval[0]),
                confidence_interval_max='{:.2f}'.format(confidence_interval[1]),
                standard_deviation=std_deviation
            )

        db.session.add(statistics_data)
        db.session.commit()
