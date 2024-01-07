def sql_create_tbl_currency() -> str:
    sql = '''
        CREATE TABLE IF NOT EXISTS currency
        (
            id_currency serial,
            "Currency" character varying(6) UNIQUE,
            "Denomination" character varying(255),
            "Flag" boolean,
            PRIMARY KEY (id_currency)
        )
    '''
    return sql


def sql_drop_tbl_currency() -> str:
    """Drop table ticker if exists
    """
    sql = 'DROP TABLE IF EXISTS currency;'
    return sql


def sql_ins_into_currency_vals(row: list) -> str:
    sql = """
        INSERT INTO currency VALUES(default, '%s', '%s', %s);
    """ % (row[0], row[1], row[2])
    return sql


def sql_sel_id_currency_currency_from_currency() -> str:
    sql = """
        SELECT id_currency, "Currency" FROM currency
        WHERE "Flag" IS TRUE;
    """
    return sql


def sql_sel_id_currency_from_currency_with_currency(currency: str) -> str:
    sql = """
        SELECT id_currency FROM currency
        WHERE "Currency"='%s';
    """ % currency
    return sql


def sql_upd_currency_vals(id_currency: int, row: list) -> str:
    sql = """
        UPDATE currency
        SET "Currency"='%s',
            "Denomination"='%s',
            "Flag"=%s
        WHERE id_currency=%d;
    """ % (row[0], row[1], row[2], id_currency)
    return sql
