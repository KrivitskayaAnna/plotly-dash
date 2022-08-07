import sqlite3
import numpy as np
import pandas as pd


def get_conn(database='test.db'):
    """create conn"""
    return sqlite3.connect(database)


def create_test_table(conn):
    """initialize test_table"""

    cursor = conn.cursor()

    sql_drop_table = "DROP TABLE IF EXISTS test_table"
    cursor.execute(sql_drop_table)

    sql_create_table = """CREATE TABLE test_table 
                          (id BIGSERIAL PRIMARY KEY,
                          is_reviewed BOOLEAN,
                          fio_reviewed_by TEXT,
                          date_reviewed TIMESTAMP,
                          source_text TEXT, 
                          tag_1 TEXT, tag_2 TEXT, tag_3 TEXT,
                          tag_1_relevance BOOLEAN, tag_2_relevance BOOLEAN, tag_3_relevance BOOLEAN)"""
    cursor.execute(sql_create_table)

    with open("dialog.txt", "r") as file:
        sample_dialog = file.readlines()
    dialog1 = "first <BR>" + "<BR>".join(sample_dialog)
    dialog2 = "second <BR>" + "<BR>".join(sample_dialog)
    dialog3 = "third <BR>" + "<BR>".join(sample_dialog)

    rows = [(False, np.nan, np.nan, dialog1, "dialog1_tag_1", "dialog1_tag_2", "dialog1_tag_3", np.nan, np.nan, np.nan),
            (False, np.nan, np.nan, dialog2, "dialog2_tag_1", "dialog2_tag_2", "dialog2_tag_3", np.nan, np.nan, np.nan),
            (False, np.nan, np.nan, dialog3, "dialog3_tag_1", "dialog3_tag_2", "dialog3_tag_3", np.nan, np.nan, np.nan)]

    sql_fill_table = """INSERT INTO test_table
                        VALUES (?,?,?,?,?,?,?,?,?,?)"""
    cursor.executemany(sql_fill_table, rows)

    return 0


def get_table(conn):
    """get one row from table"""
    sql_get_table = "SELECT * FROM test_table WHERE is_reviewed = False LIMIT 1"
    return pd.read_sql(sql_get_table, conn)
