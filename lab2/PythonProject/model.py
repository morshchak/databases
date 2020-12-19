import psycopg2


class Model:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(host="localhost", port="5432",
                                               database='university', user='postgres', password='72307247')
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error:
            print("Помилка при з'єднанні з PostgreSQL", error)

    def get_col_names(self):
        return [d[0] for d in self.cursor.description]

    def create_db(self):
        f = open("create_db.txt", "r")

        self.cursor.execute(f.read())
        self.connection.commit()

    def get(self, tname, parameter):
        try:
            query = f'SELECT * FROM {tname}'

            if parameter:
                query += ' WHERE ' + parameter

            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def insert(self, tname, columns, values):
        try:
            query = f'INSERT INTO {tname} ({columns}) VALUES ({values});'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def delete(self, tname, parameter):
        try:
            query = f'DELETE FROM {tname} WHERE {parameter};'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def update(self, tname, parameter, statement):
        try:
            query = f'UPDATE {tname} SET {statement} WHERE {parameter}'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def search_task_by_student_group(self, groups):
        try:
            query = f'''
            SELECT * from task
            WHERE id in(
                SELECT task_id FROM student_task
                JOIN student on student_task.student_id=student.id
                WHERE LOWER(student_group) in ({groups.lower()})
            );'''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def search_student_by_task_is_passed(self, is_passed):
        try:
            query = f'''
            SELECT * from student
            WHERE id in(
                SELECT student_id FROM student_task
                JOIN task on task.id=student_task.task_id
                WHERE is_passed={is_passed});'''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def fillFacultyByRandomData(self, number):
        sql = f"""
        CREATE OR REPLACE FUNCTION randomFaculties()
            RETURNS void AS $$
        DECLARE
            step integer  := 0;
        BEGIN
            LOOP EXIT WHEN step >= {number};
                INSERT INTO faculty (name, number_of_students, foundation_date)
                VALUES (
                    substring(md5(random()::text), 1, 30),
                    (random() * (2000 - 1) + 100)::integer,
                    timestamp '1900-01-01 20:00:00' +
                    random() * (timestamp '2015-12-31 20:00:00' -
                    timestamp '1900-01-01 10:00:00')
                );
                step := step + 1;
            END LOOP ;
        END;
        $$ LANGUAGE PLPGSQL;
        SELECT randomFaculties();
        """
        try:
            self.cursor.execute(sql)
        finally:
            self.connection.commit()
