import sqlite3 as sql


class Database:
    def __init__(self, db_name='db.sqlite3'):
        # db.sqlite3 is  a default database
        self.con = sql.connect(db_name)
        print('connected to dbase')

    def close(self):
        self.con.close()
        print('database disconnected')

    def preference_table(self):
        query = "CREATE TABLE preference_table (id INTEGER PRIMARY KEY AUTOINCREMENT, a1 TEXT , a2 TEXT, a3 DOUBLE)"
        self.run_query(query)

    def run_query(self, query):
        try:
            self.con.execute(query)
            self.con.commit()
            print('executed')
            return True
        except Exception as e:
            print(e)
            return False

    def add_preference(self, a1, a2, a3):
        query = f"INSERT INTO preference_table VALUES(null,'{a1}','{a2}', {a3})"
        self.run_query(query)

    def view_preference(self):
        query = "select * from preference_table"
        try:
            result = self.con.execute(query)
            return result.fetchall()
        except Exception as e:
            print(e)

    def delete_preference(self, id):
        query = f"DELETE FROM delete_preference WHERE id={id}"
        return self.con.execute(query)

    def update_preference(self, id, a1=None, a2=None, a3=None):
        query = f"select * from delete_preference where id={id}"
        try:

            result = self.con.execute(query)
            data = result.fetchall()[0]
            if not a1:
                name = data[1]
            if not a2:
                name = data[2]
            if not a3:
                name = data[3]
            query = f"""UPDATE preference_table SET
                    a1='{a1}',
                    a2='{a2}',
                    a3='{a3}'
                    WHERE id={id}
            """
            return self.run_query(query)
        except Exception as e:
            print(e)
            return False

    def user_table(self):
        query = "CREATE TABLE user_table (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT , email TEXT, password TEXT)"
        self.run_query(query)

    def add_user(self, username, email, password):
        query = f"INSERT INTO user_table VALUES(null,'{username}','{email}', '{password}')"
        self.run_query(query)

    def view_user(self):
        query = "select * from user_table"
        try:
            result = self.con.execute(query)
            return result.fetchall()
        except Exception as e:
            print(e)

    def delete_user(self, id):
        query = f"DELETE FROM user_table WHERE id={id}"
        return self.con.execute(query)

    def update_user(self, id, username=None, email=None, password=None):
        query = f"select * from user_table where id={id}"
        try:

            result = self.con.execute(query)
            data = result.fetchall()[0]
            if not username:
                username = data[1]
            if not email:
                email = data[2]
            if not password:
                password = data[3]
            query = f"""UPDATE user_table SET
                    username='{username}',
                    email='{email}',
                    password='{password}'
                    WHERE id={id}
            """
            return self.run_query(query)
        except Exception as e:
            print(e)
            return False
