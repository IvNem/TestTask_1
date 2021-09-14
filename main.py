import psycopg2
import sys
import random
import string
import time
from datetime import date, timedelta


def buildblock(size):
    return ''.join(random.choice(string.ascii_letters) for _ in range(size))


def generateFio():
    return str.upper(buildblock(10)) + ' ' + str.upper(buildblock(10)) + ' ' + str.upper(buildblock(10))


def generateBirthday():
    lower = date(1990, 1, 1)
    return lower + timedelta(random.randint(4000, 8000))


def buildPeople(specialVariant=False):
    fio = generateFio()
    if(specialVariant == True):
        fio = 'F' + fio
        return fio, generateBirthday(), True
    else:
        fio = fio if fio[0] != 'F' else random.choice(
            'ABCDEGHIJKLMNOPQRSTUVWXYZ') + fio
        return fio, generateBirthday(), random.choice([True, False])


if __name__ == "__main__":
    conn = psycopg2.connect(dbname='ptmk', user='ptmk',
                            password='ptmk', host='192.168.56.105', port='5432')

    print("Database opened successfully")
    cursor = conn.cursor()
    if sys.argv[1] == '1':
        cursor.execute('''CREATE TABLE PEOPLE  
        (ID SERIAL PRIMARY KEY NOT NULL,
        FIO TEXT NOT NULL,
        BIRTHDAY DATE NOT NULL,
        SEX BOOLEAN NOT NULL);''')
        print("Table created successfully")
        conn.commit()
        conn.close()

    elif sys.argv[1] == '2':
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO PEOPLE (FIO,BIRTHDAY,SEX) VALUES ('{sys.argv[2]}', '{sys.argv[3]}', {sys.argv[4]})"
        )

        conn.commit()
        print("Record inserted successfully")

        conn.close()
    elif sys.argv[1] == '3':
        cursor = conn.cursor()
        cursor.execute(
            '''select p1.fio, p1.birthday, p1.sex,date_part('year', age(p1.birthday)) as number_of_years 
            from people p1 where not exists(select * from people p2 where p1.fio = p2.fio and p1.birthday = p2.birthday and p1.id <> p2.id);'''
        )
        rows = cursor.fetchall()
        for row in rows:
            print("FIO =", row[0])
            print("BIRTHDAY =", row[1])
            print("SEX =", row[2])
            print("NUMBER_OF_YEARS =", row[3], "\n")

        print("Operation done successfully")
        conn.close()
    elif sys.argv[1] == '4':
        cursor = conn.cursor()
        for i in range(0, 100):
            people = buildPeople(True)
            sql = (
                f"INSERT INTO PEOPLE (FIO,BIRTHDAY,SEX) VALUES ('{people[0]}', '{people[1]}', {people[2]})")
            cursor.execute(sql)
        conn.commit()
        for i in range(0, 999900):
            people = buildPeople()
            sql = (
                f"INSERT INTO PEOPLE (FIO,BIRTHDAY,SEX) VALUES ('{people[0]}', '{people[1]}', {people[2]})")
            cursor.execute(sql)
            if(i % 100 == 0):
                conn.commit()
        conn.commit()
    elif sys.argv[1] == '5':
        cursor = conn.cursor()
        t0 = time.time()
        cursor.execute(
            "select * from people where fio like 'F%' and sex=true;"
        )
        rows = cursor.fetchall()
        print(time.time() - t0)
    elif sys.argv[1] == '6':
        cursor = conn.cursor()
        cursor.execute(
            "CREATE INDEX ind_people ON people using btree (FIO);"
        )
        conn.commit()
