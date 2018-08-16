def max_sql_variables():
    """See the comment above providing credit to user F. Montesano.
    """
    import sqlite3
    db = sqlite3.connect(':memory:')
    cur = db.cursor()
    cur.execute('CREATE TABLE t (test)')
    low, high = 0, 100000
    while (high - 1) > low: 
        guess = (high + low) // 2
        query = 'INSERT INTO t VALUES ' + ','.join(['(?)' for _ in
                                                    range(guess)])
        args = [str(i) for i in range(guess)]
        try:
            cur.execute(query, args)
        except sqlite3.OperationalError as e:
            if "too many SQL variables" in str(e):
                high = guess
            else:
                raise
        else:
            low = guess
    cur.close()
    db.close()
    return low

