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
        query = "CREATE TABLE preference_table (id INTEGER PRIMARY KEY AUTOINCREMENT, preference TEXT , review TEXT, rating DOUBLE,user_id INTEGER)"
        self.run_query(query)

    def run_query(self, query):
        try:
            self.con.execute(query)
            self.con.commit()
            print(query,'executed')
            return True
        except Exception as e:
            print(e)
            return False

    def add_preference(self, preference, review, rating,userid):
        query = f"INSERT INTO preference_table VALUES(null,'{preference}','{review}', {rating},{userid})"
        self.run_query(query)

    def view_preference(self,userid):
        query = f"select * from preference_table where user_id={userid}"
        try:
            result = self.con.execute(query)
            return result.fetchall()
        except Exception as e:
            print(e)

    def delete_preference(self, userid):
        query = f"DELETE FROM delete_preference WHERE id={userid}"
        return self.con.execute(query)

    def update_preference(self, userid, preference=None, review=None, rating=None):
        query = f"select * from delete_preference where id={userid}"
        try:

            result = self.con.execute(query)
            data = result.fetchall()[0]
            if not preference:
                preference = data[1]
            if not review:
                review = data[2]
            if not rating:
                rating = data[3]
            query = f"""UPDATE preference_table SET
                    preference='{preference}',
                    review='{review}',
                    rating='{rating}'
                    WHERE id={userid}
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
        return self.run_query(query)

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


if __name__ == "__main__":
    db= Database()
    db.run_query('drop table preference_table')