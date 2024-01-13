def sql_create_tbl_iticker() -> str:
    sql = '''
        CREATE TABLE IF NOT EXISTS iticker
        (
            id_index serial,
            "指数" character varying(6) UNIQUE,
            "名称" character varying(255),
            PRIMARY KEY (id_index)
        )
    '''
    return sql


def sql_ins_into_iticker_vals(row: list) -> str:
    sql = """
        INSERT INTO iticker VALUES(default, '%s', '%s');
    """ % (row[0], row[1])
    return sql


def sql_sel_id_index_from_iticker_with_iticker(iticker: str) -> str:
    sql = """
        SELECT id_index FROM iticker
        WHERE "指数"='%s';
    """ % iticker
    return sql


def sql_upd_iticker_vals(id_index: int, row: list) -> str:
    sql = """
        UPDATE iticker
        SET "指数"='%s',
            "名称"='%s'
        WHERE id_index=%d;
    """ % (row[0], row[1], id_index)
    return sql
