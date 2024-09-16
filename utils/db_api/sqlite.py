import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    # Create tables
    def create_table_users(self):
        sql = """
          CREATE TABLE IF NOT EXISTS Users (
              id TEXT PRIMARY KEY,  -- Store UUID as TEXT
              fullname VARCHAR(255),
              telegram_id VARCHAR(20) UNIQUE,
              language VARCHAR(3),
              phone VARCHAR(20),
              phone_number VARCHAR(20) NULL,
              manzil TEXT,
              saja TEXT,
              sj_avia TEXT,
              tuman TEXT,
              is_staff BOOLEAN DEFAULT FALSE,
              exact_address TEXT,
              description TEXT,
              user_id TEXT,
              add_user TEXT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
              updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Remove ON UPDATE clause
          );
          """
        self.execute(sql, commit=True)

    def create_table_address(self):
        sql = """
          CREATE TABLE IF NOT EXISTS Address (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id TEXT,          -- Added this to relate address with user
              region_id TEXT,
              pk TEXT,
              name TEXT,
              region_name TEXT,
              FOREIGN KEY (user_id) REFERENCES Users(telegram_id)
          );
          """
        self.execute(sql, commit=True)

    def create_table_orders(self):
        sql = """
            CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT,
                kg TEXT,
                hajm TEXT,
                qty INT,
                price INT,
                reiz_number INT,
                status BOOLEAN DEFAULT FALSE,
                image TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                order_id TEXT
            )
        """
        self.execute(sql=sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, fullname: str, telegram_id: str = None, language: str = 'uz', phone: str = None,
                 phone_number: str = None, manzil: str = None, saja: str = None, sj_avia: str = None, tuman: str = None,
                 exact_address: str = None, description: str = None,  user_id: str =None):
        sql = """
        INSERT INTO Users(id, fullname, telegram_id, language, phone, phone_number, manzil,
        saja, sj_avia, tuman, exact_address, description, user_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, fullname, telegram_id, language, phone, phone_number, manzil, saja, sj_avia, tuman, exact_address, description, user_id
                                      ), commit=True)

    def add_address(self, user_id: str, region_id: str, name: str, pk: str, region_name: str):
        sql = """
        INSERT INTO Address(user_id, region_id, pk, name, region_name) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, region_id, pk, name, region_name), commit=True)

    def add_order(self, client_id: str, kg: str, hajm: str, qty: int, price: int, reiz_number: int, status: bool,
                  image: str, created_at: str, updated_at: str, order_id : str):
        sql = """
        INSERT INTO Orders (client_id, kg, hajm, qty, price, reiz_number, status, image, created_at, updated_at, order_id)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(client_id, kg, hajm, qty, price, reiz_number, status, image, created_at,
                                      updated_at, order_id), commit=True)

    def select_all_address(self):
        sql = """
           SELECT * FROM Address
           """
        return self.execute(sql, fetchall=True)

    def select_all_orders(self):
        sql = """
        SELECT * FROM Orders
        """
        return self.execute(sql, fetchall=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        """
        Select a user from the Users table based on provided filters.

        :param kwargs: Filtering criteria, e.g., telegram_id=123456
        :return: Fetched user data
        """
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def select_order(self, **kwargs):
        sql = "SELECT * FROM Orders WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def select_address(self, **kwargs):
        """
        Select address information based on provided filters.

        :param kwargs: Filtering criteria, e.g., region_name='Toshkent'
        :return: Fetched address data
        """
        sql = "SELECT * FROM Address WHERE "
        conditions = []
        parameters = []

        for key, value in kwargs.items():
            conditions.append(f"{key} = ?")
            parameters.append(value)

        sql += " AND ".join(conditions)
        return self.execute(sql, parameters, fetchone=True)

    def select_district_names_by_region_id(self, region_id):
        """
        Select all district names for a given region ID.

        :param region_id: ID of the region to filter by
        :return: List of district names
        """
        sql = "SELECT DISTINCT name FROM Address WHERE region_id = ?"
        parameters = [region_id]
        result = self.execute(sql, parameters, fetchall=True)
        return [row[0] for row in result]

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_field(self, telegram_id, field, value):
        # Ensure that only valid fields are updated to prevent SQL injection
        valid_fields = {"fullname", "phone_number", "manzil", "kargo", "tuman", "sj_avia", "saja", "is_staff",
                        "exact_address", "add_user", "updated_at", "description"}  # Add other valid fields as needed
        if field not in valid_fields:
            raise ValueError(f"Invalid field: {field}")

        sql = f"""
        UPDATE Users SET {field}=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(value, telegram_id), commit=True)

    def update_order_field(self, order_id, field, value):
        # Ensure that only valid fields are updated to prevent SQL injection
        valid_fields = {"status"}  # Add other valid fields as needed
        if field not in valid_fields:
            raise ValueError(f"Invalid field: {field}")

        sql = f"""
        UPDATE Orders SET {field}=? WHERE order_id=?
        """
        return self.execute(sql, parameters=(value, order_id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


    def select_user_by_saja_value(self, saja_value: str):
        """
        Select a user from the Users table based on the provided 'saja' value.

        :param saja_value: The 'saja' value to filter by.
        :return: Fetched user data if found, otherwise None.
        """
        sql = "SELECT * FROM Users WHERE saja = ?"
        parameters = (saja_value,)
        return self.execute(sql, parameters, fetchone=True)

    # You may also want a method for sj_avia:
    def select_user_by_sj_avia_value(self, sj_avia_value: str):
        """
        Select a user from the Users table based on the provided 'sj_avia' value.

        :param sj_avia_value: The 'sj_avia' value to filter by.
        :return: Fetched user data if found, otherwise None.
        """
        sql = "SELECT * FROM Users WHERE sj_avia = ?"
        parameters = (sj_avia_value,)
        return self.execute(sql, parameters, fetchone=True)

    def get_users_by_activation_status(self, is_staff: bool):
        sql = "SELECT * FROM Users WHERE is_staff = ?"
        return self.execute(sql, (is_staff,), fetchall=True)

    def select_orders_by_date(self, year: str, month: str):
        # Oyni raqam formatiga o'zgartiramiz
        month_mapping = {
            "Yanvar": "01", "Fevral": "02", "Mart": "03", "Aprel": "04",
            "May": "05", "Iyun": "06", "Iyul": "07", "Avgust": "08",
            "Sentabr": "09", "Oktabr": "10", "Noyabr": "11", "Dekabr": "12"
        }
        month = month_mapping.get(month, "01")  # Agar moslik bo'lmasa yanvarni olamiz
        sql = """
        SELECT * FROM Orders
        WHERE strftime('%Y', created_at) = ? AND strftime('%m', created_at) = ?
        """
        parameters = (year, month)
        return self.execute(sql, parameters, fetchall=True)

    def select_orders_by_date_and_status(self, year: str, month: str, status: bool):
        month_mapping = {
            "Yanvar": "01", "Fevral": "02", "Mart": "03", "Aprel": "04",
            "May": "05", "Iyun": "06", "Iyul": "07", "Avgust": "08",
            "Sentabr": "09", "Oktabr": "10", "Noyabr": "11", "Dekabr": "12"
        }
        month = month_mapping.get(month, "01")

        status_condition = 1 if status else 0

        sql = """
        SELECT * FROM Orders
        WHERE strftime('%Y', created_at) = ? AND strftime('%m', created_at) = ? AND status = ?
        """
        parameters = (year, month, status_condition)
        return self.execute(sql, parameters, fetchall=True)

    def get_user_by_phone(self, phone: str):
        sql = """
        SELECT * FROM Users
        WHERE phone = ?
        """
        parameters = (phone,)
        return self.execute(sql, parameters, fetchone=True)

    def select_orders_by_saja_id(self, saja_id: str):
        sql = """
        SELECT * FROM Orders
        WHERE client_id = ?
        """
        parameters = (saja_id,)
        return self.execute(sql, parameters, fetchall=True)
