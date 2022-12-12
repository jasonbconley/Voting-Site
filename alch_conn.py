from sqlalchemy import create_engine, MetaData, update
from matplotlib.figure import Figure

# This function could be optimized to pull from a connection pool
def get_engine():
    return create_engine('sqlite:///times.db', echo=True)

# For all choices, increment their respective number
def increment_data(choices):
    engine = get_engine()
    meta = MetaData(bind=engine)
    MetaData.reflect(meta)
    
    time_table = meta.tables['available_times']
    times = fetch_data()[0]

    # For every time chosen by the user, update that number
    for val in choices:
        u = update(time_table)
        u = u.values(count= time_table.c.count + 1)
        u = u.where(time_table.c.time == times[val])
        engine.execute(u)


# For all choices, decrement thier respective number
def decrement_data(choices):
    engine = get_engine()
    meta = MetaData(bind=engine)
    MetaData.reflect(meta)
    
    time_table = meta.tables['available_times']
    times, counts = fetch_data()

    # For every time chosen by the user, update that number
    for val in choices:
        if counts[val] > 0:
            u = update(time_table)
            u = u.values(count= time_table.c.count - 1)
            u = u.where(time_table.c.time == times[val])
            engine.execute(u)

# Fetching the table values from the sqlite db
def fetch_data():
    engine = get_engine()

    with engine.connect() as conn:
        result = conn.execute("SELECT time, count FROM available_times")
        times = []
        counts = []
        for time, count in result:
            times.append(time)
            counts.append(count)

    return times, counts

def show_graph():
    times, counts = fetch_data()
    fig = Figure()
    ax = fig.add_subplot()
    ax.bar(times, counts)
    return fig