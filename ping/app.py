import subprocess
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'database': 'citus',
    'user': 'ping_service',
    'port': 9700
}


def get_db_connection():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database:", error)
        return None


def store_ping_result(host, result):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database")
        return

    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO ping_results (host, result) VALUES (%s, %s);', (host, result))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error executing SQL query:", error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/ping', methods=['POST'])
def ping_host():
    data = request.get_json()
    host = data.get('host')

    if not host:
        return jsonify({'error': 'Missing host parameter'}), 400

    try:
        result = subprocess.run(['ping', '-c', '4', host], capture_output=True, text=True)

        store_ping_result(host, result.stdout)

        response = {
            'host': host,
            'result': result.stdout
        }

        return jsonify(response), 200
    except subprocess.CalledProcessError as error:
        return jsonify({'error': f'Error while pinging the host: {str(error)}'}), 500


if __name__ == '__main__':
    app.run(port=5002)
