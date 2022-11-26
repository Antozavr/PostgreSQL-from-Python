import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE customer_phone;
        DROP TABLE customer;
        """)
        cur.execute('CREATE TABLE IF NOT EXISTS customer ('
                    'id SERIAL PRIMARY KEY, '
                    'name VARCHAR (40) NOT NULL ,'
                    'surname VARCHAR (40) NOT NULL,'
                    'email VARCHAR (40) NOT NULL,'
                    'phone VARCHAR(40));')
        cur.execute('CREATE TABLE IF NOT EXISTS customer_phone('
                    'id SERIAL PRIMARY KEY,'
                    'customer_id integer references customer(id),'
                    'phone_number VARCHAR(220));')
        conn.commit()


def add_client(conn, first_name, last_name, email, phones):
    with conn.cursor() as cur:
        cur.execute(f"""
                   INSERT INTO customer(name, surname, email) VALUES('{first_name}', '{last_name}', '{email}')
                   RETURNING id, name, surname, email;""")
        print(cur.fetchone())
        cur.execute(f"""
                    INSERT INTO customer_phone(customer_id,phone_number) VALUES(1,'{phones}')
                    RETURNING id, customer_id, phone_number;""")
        print(cur.fetchone())


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO customer_phone(phone_number, customer_id) VALUES(%s, %s);
        """, (phone, client_id))
        conn.commit()
        cur.execute("""
              SELECT * FROM customer_phone;
              """)
        print(cur.fetchall())


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute(f"""
               UPDATE customer SET name=%s WHERE id=%s;
               """, (f'{first_name}', client_id))
        cur.execute(f"""
               UPDATE customer SET surname=%s WHERE id=%s;
               """, (f'{last_name}', client_id))
        cur.execute(f"""
               UPDATE customer SET email=%s WHERE id=%s;
               """, (f'{email}', client_id))
        cur.execute("""
               SELECT * FROM customer;
               """)
        print(cur.fetchall())
        cur.execute(f"""
               UPDATE customer_phone SET phone_number=%s WHERE id=%s;
               """, (f'{phone}', client_id))
        cur.execute("""
               SELECT * FROM customer_phone;
               """)
        print(cur.fetchall())


def delete_phone(conn, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM customer_phone WHERE phone_number=%s;
        """, (phone,))
        cur.execute("""
        SELECT * FROM customer_phone;
        """)
        print(cur.fetchall())


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM customer_phone WHERE customer_id=%s;
        """, (client_id,))
        cur.execute("""
        SELECT * FROM customer_phone;
        """)
        print(cur.fetchall())
        cur.execute("""
        DELETE FROM customer WHERE id=%s;
        """, (client_id,))
        cur.execute("""
        SELECT * FROM customer;
        """)
        print(cur.fetchall())


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM customer WHERE name=%s and surname=%s and email=%s;
            """, (first_name, last_name, email,))
        print(cur.fetchall())
        cur.execute("""
                    SELECT customer_id FROM customer_phone WHERE phone_number=%s;
                    """, (phone,))
        print(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database="netology_db", user="postgres", password="USHxv246") as conn:
        create_db(conn)
        add_client(conn, 'Anton', 'Potapov', 'antozavr@gmail.com', '+7-222-333-44-55')
        add_phone(conn, 1, '+72382365517')
        change_client(conn, 1, 'Pavel', 'Mamonov', 'mamonov@mail.ru', '+72222222')
        # delete_phone(conn, '+72382365517')
        # delete_client(conn, 1)
        find_client(conn, 'Pavel', 'Mamonov', 'mamonov@mail.ru', '+72222222')
