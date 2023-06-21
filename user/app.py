from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'database': 'citus',
    'user': 'user_service',
    'port': 9700
}


def get_db_connection():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database:", error)
        return None


@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users;')
        rows = cursor.fetchall()

        users = []
        for row in rows:
            user = {
                'id': row[0],
                'name': row[1],
                'email': row[2]
            }
            users.append(user)

        return jsonify(users), 200
    except (Exception, psycopg2.Error) as error:
        print("Error executing SQL query:", error)
        return jsonify({'error': 'Failed to fetch users from the database'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/users', methods=['POST'])
def create_users():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    try:
        data = request.get_json()
        users = data

        if not isinstance(users, list):
            return jsonify({'error': 'Invalid data format. Expected an array of users.'}), 400

        cursor = conn.cursor()

        created_user_ids = []
        for user in users:
            name = user.get('name')
            email = user.get('email')

            cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;', (name, email))
            user_id = cursor.fetchone()[0]
            created_user_ids.append(user_id)

        conn.commit()

        return jsonify({'message': 'Users created successfully', 'user_ids': created_user_ids}), 201
    except (Exception, psycopg2.Error) as error:
        print("Error executing SQL query:", error)
        return jsonify({'error': 'Failed to create users in the database'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run()

