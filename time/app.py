from flask import Flask, jsonify, request
import datetime
import psycopg2

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'database': 'citus',
    'user': 'time_service',
    'port': 9700
}


def get_db_connection():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database:", error)
        return None


def store_query_details(ip_address, query_time):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database")
        return

    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO query_details (ip_address, query_time) VALUES (%s, %s);', (ip_address, query_time))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error executing SQL query:", error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/current_time', methods=['GET'])
def get_current_time():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = request.remote_addr

    store_query_details(ip_address, current_time)

    response = {
        'current_time': current_time,
        'ip_address': ip_address
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(port=5001)
