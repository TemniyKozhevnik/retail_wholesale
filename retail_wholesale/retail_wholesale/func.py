import psycopg2


def dbconnector():
    con = psycopg2.connect(
        dbname='App',
        user='postgres',
        password='admin12345',
        host='localhost',
        port='5433'
    )
    return con


def take_id_from_customer(first_name, second_name, phone_number):
    con = dbconnector()
    cur = con.cursor()
    cur.execute(
        f'''select
	           id
            from retail_customer
            where
                first_name = \'{first_name}\'
            and
                second_name = \'{second_name}\'
            and
                phone_number = \'{phone_number}\''''
    )
    dbconnector().close()
    return cur.fetchone()[0]


def take_id_from_product(category, sub_category, title):
    con = dbconnector()
    cur = con.cursor()
    cur.execute(
        f'''select
	           id
            from retail_product
            where
                category = \'{category}\'
            and
                sub_category = \'{sub_category}\'
            and
                title = \'{title}\''''
    )
    dbconnector().close()
    return cur.fetchone()[0]