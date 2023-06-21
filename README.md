# Citus Example: Microservices

Three microservices used to demonstrte setting up Citus as scalable storage backend for microservices.

# Citus setup

```sql
    SET citus.enable_schema_based_sharding TO ON;

    CREATE SCHEMA AUTHORIZATION user_service;
    CREATE SCHEMA AUTHORIZATION time_service;
    CREATE SCHEMA AUTHORIZATION ping_service;
```

Execute the corresponding SQL file as every service.

```bash
psql -U user_service -f user_service/user.sql
psql -U time_service -f time_service/time.sql
psql -U ping_service -f ping_service/ping.sql
```

# Connection configuration

Modify the `db_config` variable for every service in their `app.py`.

```python
db_config = {
    'host': 'localhost',
    'database': 'citus',
    'user': 'time_service',
    'port': 9700
}
```

# Running the apps

Change into every app directory and run them in their own python env.

```bash
cd user
pipenv install
pipenv shell
python app.py
```

Repeat the above for `time` and `ping` service.

# Execute some commands against the API

```bash

    # Create 10 users
    curl -X POST -H "Content-Type: application/json" -d '[
      {"name": "John Doe", "email": "john@example.com"},
      {"name": "Jane Smith", "email": "jane@example.com"},
      {"name": "Mike Johnson", "email": "mike@example.com"},
      {"name": "Emily Davis", "email": "emily@example.com"},
      {"name": "David Wilson", "email": "david@example.com"},
      {"name": "Sarah Thompson", "email": "sarah@example.com"},
      {"name": "Alex Miller", "email": "alex@example.com"},
      {"name": "Olivia Anderson", "email": "olivia@example.com"},
      {"name": "Daniel Martin", "email": "daniel@example.com"},
      {"name": "Sophia White", "email": "sophia@example.com"}
    ]' http://localhost:5000/users

    # List users
    curl http://localhost:5000/users

    # Get current time
    curl http://localhost:5001/current_time

    # Ping example.com
    curl -X POST -H "Content-Type: application/json" -d '{"host": "example.com"}' http://localhost:5002/ping

```

# LICENSE

Copyright (c) 2023, Microsoft

Licensed under the MIT license - feel free to incorporate the code in your own projects!