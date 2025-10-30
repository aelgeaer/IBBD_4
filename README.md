make new server

mkdir "C:\PostgreSQL\server2_data"
initdb -D "C:\PostgreSQL\server2_data" -U postgres -W
pg_ctl -D "C:\PostgreSQL\server2_data" -o "-p 5433" start
psql -U postgres -d postgres -p 5433
add to psAdmin 4

make new database
CREATE DATABASE dbs24;
create tables

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python main.py

Go to: http://localhost:5000
