from psycopg2 import connect
from psycopg2 import DatabaseError
from config import config
from matplotlib.figure import Figure

def insert_data(time_choice):
    conn = None
    try:
        params = config()
        conn = connect(**params)

        with conn, conn.cursor() as cur:
    
            cur.execute("SELECT * FROM \"timesSchema\".availabletimes")
            sql_list = cur.fetchall()
            times_list = [time[0] for time in sql_list]

            if validate_data(times_list[time_choice], times_list):
                cur.execute("UPDATE \"timesSchema\".usertimes SET number = number + 1 WHERE time = \'{}\'".format(times_list[time_choice]))
                conn.commit()
                print("Data inserted")
            else:
                print("Invalid data")

    except (Exception, DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def delete_data(time_choice : int):
    conn = None
    try:
        params = config()
        conn = connect(**params)

        with conn, conn.cursor() as cur:
    
            cur.execute("SELECT * FROM \"timesSchema\".availabletimes")
            sql_list = cur.fetchall()
            times_list = [time[0] for time in sql_list]

            current_number = 0
            if validate_data(times_list[time_choice], times_list):
                cur.execute("SELECT number FROM \"timesSchema\".usertimes WHERE time = \'{}\'".format(times_list[time_choice]))
                current_number = cur.fetchone()[0]
                print(f'current number is {current_number}')
            else:
                print("Invalid data")

            if int(current_number) >= 1:
                cur.execute("UPDATE \"timesSchema\".usertimes SET number = number - 1 WHERE time = \'{}\'".format(times_list[time_choice]))
                conn.commit()
                print("Data updated")

    except (Exception, DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def show_graph():
    data_list = display_data()
    x = [data[0] for data in data_list]
    y = [data[1] for data in data_list]
    fig = Figure()
    ax = fig.add_subplot()
    ax.bar(x, y)
    return fig
    
def display_data():
    conn = None
    data_list = ['None', 'None', 'None']
    try:
        params = config()
        conn = connect(**params)

        with conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM \"timesSchema\".usertimes")
            sql_list = cur.fetchall()
            data_list = sql_list

    except (Exception, DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            return data_list
    
# Helper functions for this script
def validate_data(data_val, data_list):
    if data_val in data_list:
        return True

    return False