import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class DataBase:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
        )

    def get_items(self):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""select item_id, name, price from items""")
                return cursor.fetchall()

    def get_discounters(self):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""select item_id, name from discounted_users""")
                return cursor.fetchall()

    def get_master_data(self, duty_id):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """with ts as (select opened_at, coalesce(closed_at, timezone('utc', now()::timestamp)) as closed_at from duties where id = %s),
                    tea as (
                        select coalesce(sum(50), 0) as sum, count(*) 
                    from items_purchased T 
                        left join items 
                               on items.item_id = T.item_id 
                    where T.item_id = 7 
                               and created_at < (select closed_at from ts) 
                               and created_at >= (select opened_at from ts)
                    ) 
            select sum(100), count(*), (select sum from tea), (select count from tea)
                    from items_purchased T 
                        left join items 
                               on items.item_id = T.item_id 
                    where T.item_id < 5 
                               and created_at < (select closed_at from ts) 
                               and created_at >= (select opened_at from ts)""",
                    (
                        duty_id,
                    ),
                )
                return cursor.fetchone()

    # """SELECT SUM(salary) FROM duties
    # WHERE opened_at >= DATE_TRUNC('month', CURRENT_DATE)
    # AND closed_at < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
    # """

    def insert_buy(self, item_id, master_tg_id, payment, comment, discount_id = None):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """insert into items_purchased (item_id, tg_id, amount, comment, payment, discount_id) values(%s, %s, 1, %s, %s, %s)""",
                    (
                        item_id,
                        master_tg_id,
                        comment,
                        payment,
                        discount_id
                    ),
                )

    def insert_expense(self, tg_id, expense, amount, comment):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """insert into expences (tg_id, expense, amount, comment) values(%s, %s, %s, %s)""",
                    (
                        tg_id,
                        expense,
                        amount,
                        comment,
                    ),
                )

    def get_hookah_master(self, tg_id):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """select 1 from masters where tg_id = %s""", (tg_id,)
                )
                rows = cursor.fetchone()
                if rows is not None:
                    return True
                else:
                    return False

    def open_duty(self, master_tg_id):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """insert into duties (tg_id) values (%s)""", (master_tg_id,)
                )

    def get_active_duty(self):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """select id, tg_id from duties
                         where closed_at is null
                        """
                )
                return cursor.fetchone()

    def close_duty(self):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """update duties set closed_at = now()::timestamp where closed_at is null;""",
                )

    def insert_reserve(self, tg_id, amount, date, comment):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO reservations (tg_id, amount, datetime, comment)
                               VALUES (%s, %s, %s, %s)""",
                    (tg_id, amount, date, comment),
                )

    def get_month_salary(self):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT name, SUM(salary) FROM duties
                    LEFT JOIN masters On duties.tg_id = masters.tg_id
                    WHERE opened_at >= DATE_TRUNC('month', CURRENT_DATE)
                    AND closed_at < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
                    GROUP BY name""",
                )
                return cursor.fetchall()

    def get_earn(self):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT sum(price) from items_purchased left join items on items.item_id = items_purchased.item_id where created_at < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month' and created_at >= DATE_TRUNC('month', CURRENT_DATE)""",
                )
                return cursor.fetchone()

    def get_expences(self):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT sum(amount) from expences where datetime < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month' and datetime >= DATE_TRUNC('month', CURRENT_DATE)""",
                )
                return cursor.fetchone()

    def get_last_month_salary(self):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT name, SUM(salary) FROM duties
                    LEFT JOIN masters On duties.tg_id = masters.tg_id
                    WHERE opened_at >= DATE_TRUNC('month', CURRENT_DATE - interval '1 month')
                    AND closed_at < DATE_TRUNC('month', CURRENT_DATE)
                    GROUP BY name""",
                )
                return cursor.fetchall()

    def get_items_today(self, duty_id):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """ with ts as (select opened_at, coalesce(closed_at, timezone('utc', now()::timestamp)) as closed_at from duties where id = %s)
                    SELECT name, price, comment, discount_id FROM items_purchased
                    LEFT JOIN items on items_purchased.item_id = items.item_id
                    WHERE created_at >= (select opened_at from ts)
                    AND created_at < (select closed_at from ts) order by created_at asc""",
                    (duty_id,),
                )
                return cursor.fetchall()

    def insert_user(self, user_tg_id, name, phone):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO users (tg_id, name, phone) VALUES (%s, %s, %s)""",
                    (user_tg_id, name, phone),
                )

    def get_user_tg_id(self, user_tg_id):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT name, phone from users where tg_id=%s""", (user_tg_id,))
                rows = cursor.fetchone()
                if rows is not None:
                    return rows
                else:
                    return None


# SELECT  name, salary, duties.id, opened_at, closed_at FROM duties
#                     LEFT JOIN masters On duties.master = masters.user_id
#                     WHERE opened_at >= DATE_TRUNC('month', CURRENT_DATE - interval '1 month')
#                     AND closed_at < DATE_TRUNC('month', CURRENT_DATE)
