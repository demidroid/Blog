

def pg_sql(sql: str, values: list):
    str_sql = sql % tuple(values)
    return str_sql
