import psycopg2

con = psycopg2.connect(
    dbname='App',
    user='postgres',
    password='admin12345',
    host='localhost',
    port='5433'
)
cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS retail_product(
    id SERIAL PRIMARY KEY,
    title varchar(50) NOT NULL,
    category varchar(50) NOT NULL,
    sub_category varchar(50),
    text text default 'Дополнительная информация отсутствует.'
);
            
CREATE TABLE IF NOT EXISTS retail_wholesale(
    id SERIAL PRIMARY KEY,
    order_date TIMESTAMP NOT NULL,
    region varchar(50) NOT NULL,
    sales INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES retail_customer(id),
    FOREIGN KEY(product_id) REFERENCES retail_product(id)
);

drop procedure insert_retail_wholesale;
CREATE PROCEDURE insert_retail_wholesale(
        p_order_date timestamp,
        p_region varchar(50),
        p_sales integer,
        p_customer_id integer,
        p_product_id integer
    ) as $$
    begin 
        insert into retail_wholesale(
            order_date,
            region,
            sales,
            customer_id,
            product_id
        )
        values(
            p_order_date,
            p_region,
            p_sales,
            p_customer_id,
            p_product_id
        );
    end;
    $$ language plpgsql;

drop procedure update_retail_wholesale;   
CREATE PROCEDURE update_retail_wholesale(
        p_id integer,
        p_order_date timestamp,
        p_region varchar(50),
        p_sales integer,
        p_customer_id integer,
        p_product_id integer
    ) as $$
    begin 
        update retail_wholesale
        set 
        order_date = p_order_date,
        region = p_region,
        sales = p_sales,
        customer_id = p_customer_id,
        product_id = p_product_id
        where id = p_id;
    end;
    $$ language plpgsql; 

drop procedure delete_retail_wholesale; 
CREATE PROCEDURE delete_retail_wholesale(
        p_id integer
    ) as $$
    begin 
        delete from retail_wholesale
        where id = p_id;
    end;
    $$ language plpgsql; 
''')

con.commit()
con.close()