import MySQLdb
import csv


def get_connector(user='protekdb',passwd='protekdb',host='protekdb.cp8grvhux7la.us-west-1.rds.amazonaws.com',db='protekdb'):
    conn = MySQLdb.connect(user=user,passwd=passwd,host=host,db=db)
    return conn


def create_table(query='create table muralitb (fname varchar(50),lname varchar(50), address varchar(100)) '):
    try:
        connector = get_connector()
        mycursor = connector.cursor()
        mycursor.execute()
        connector.close()
    except Exception, e:
        print str(e)


def insert_into_table(query='insert into muralitb values("%s", "%s", "%s")' %('Murali', 'Gogineni', 'Protek Consultancy')):
    try:
        connector = get_connector()
        mycursor = connector.cursor()
        mycursor.execute(query)
        connector.commit()
        connector.close()
        print 'inserted'
    except Exception, e:
        print str(e)


def get_data_from_table(query='select * from muralitb'):
    try:
        connector = get_connector()
        mycursor = connector.cursor()
        mycursor.execute(query)
        return mycursor.fetchall()
    except Exception, e:
        print str(e)


def delete_data_from_table(query='delete from muralitb'):
    try:
        connector = get_connector()
        mycursor = connector.cursor()
        mycursor.execute(query)
        print 'deleted'
    except Exception, e:
        print str(e)


def delete_table(query='drop table muralitb'):
    try:
        connector = get_connector()
        mycursor = connector.cursor()
        mycursor.execute(query)
        print 'deleted'
    except Exception, e:
        print str(e)


def get_row_count(query='select count(*) from muralitb'):
    try:
        connector = get_connector()
        mycursor = connector.cursor()
        mycursor.execute(query)
        return mycursor.fetchall()
    except Exception, e:
        print str(e)


def check_for_special_chars(input):
    import re
    chars = re.findall('[a-zA-Z\s]*', input)
    if ''.join(chars) == input:
        return True


def read_and_insert_csv(location):
    with open(location, 'rb') as csv_file:
        csv_read = csv.DictReader(csv_file, delimiter=',')
        for row in csv_read:
            for item in row.values():
                if not check_for_special_chars(item):
                    print 'Invalid value entered `ease try again: ' + item
                    return
            insert_into_table('insert into muralitb values("%s", "%s", "%s")' %(row['Fname'], row['Lname'], row['Address']))

read_and_insert_csv('/home/rakesh/Desktop/test2.csv')
# print get_row_count()[0][0]
