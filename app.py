from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Подключение к базе данных PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        dbname="medical_center",  # Укажите имя вашей базы данных
        user="postgres",  # Укажите ваше имя пользователя
        password="korol",  # Укажите ваш пароль
        host="localhost",  # Адрес сервера (обычно localhost)
        port="5432"  # Порт по умолчанию для PostgreSQL
    )
    return conn

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Добавить пациента
@app.route('/add-patient', methods=['POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        date_of_birth = request.form['date_of_birth']
        diagnosis = request.form['diagnosis']

        # Получаем текущую дату для admission_date
        admission_date = datetime.now().strftime('%Y-%m-%d')  # Текущая дата в формате ГГГГ-ММ-ДД

        # Вставляем данные пациента в таблицу
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patients (name, date_of_birth, diagnosis, admission_date) VALUES (%s, %s, %s, %s)",
            (name, date_of_birth, diagnosis, admission_date)  # Добавлен admission_date
        )
        conn.commit()  # Сохраняем изменения в базе данных
        cursor.close()
        conn.close()

        return redirect(url_for('index'))  # После добавления перенаправляем на главную страницу

# Выполнение произвольного SQL запроса
@app.route('/execute-sql', methods=['POST'])
def execute_sql():
    if request.method == 'POST':
        sql_query = request.form['sql_query']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('index.html', message='Query executed successfully!', result=result)
        except Exception as e:
            return render_template('index.html', message=f'Error executing query: {str(e)}')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)







