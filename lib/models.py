import sqlite3

# Setup

def mkdir_p(directory):
    try:
        os.mkdir(directory)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise e
        pass

mkdir_p("./sql")

conn = sqlite3.connect("")

# Utility functions

def _convert_elem(elem):
    t = type(elem)
    if t == str:
        return "'" + elem + "'"
    elif t == int:
        return str(elem)
    else:
        return "'" + str(elem) + "'"

def query_from_file(name):
    f = open(os.path.join(".", "sql", name))
    return f.read().strip()

def create_tables():
    cursor = conn.cursor()
    res1 = cursor.execute(query_from_file("create-tumblr-oauth.sql"))
    res2 = cursor.execute(query_from_file("create-tumblr-posts.sql"))
    res3 = cursor.execute(query_from_file("create-medium-posts.sql"))
    return res1 | res2 | res3

def insert(tablename, rows=[]):
    values = []
    for row in rows:
        elems_as_str = [_convert_elem(elem) for elem in row]
        row_as_str = "(" + ",".join(elems_as_str)  + ")"
        values.append(row_as_str)
    values_as_str = ",\n".join(values)
    sql = "insert into %s values %s" % (tablename, values_as_str)
    return cursor.execute(sql)

def find(query, is_file=False):
    if is_file:
        filename = query
        return cursor.execute(query_from_file(filename))
    else:
        return cursor.execute(query)

def unwrap(result):
    return result[0]

def unwrap_one(result):
    return result[0][0]
