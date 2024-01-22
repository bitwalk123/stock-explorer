def sql_create_tbl_order() -> str:
    sql = '''
        CREATE TABLE IF NOT EXISTS order
        (
            id_order serial,
            "注文番号" integer,
            "アルゴ注文番号" integer,
            "繰越区分" character varying(255),
            "状況" character varying(255),
            "状況(逆指値)" character varying(255),
            "セット注文" character varying(255),
            "注文日時" character varying(255),
            "執行条件" character varying(255),
            "注文期限" character varying(255),
            "銘柄" character varying(255),
            "銘柄コード・市場" character varying(255),
            "取引" character varying(255),
            "売買" character varying(255),
            "口座" character varying(255),
            "注文方法" character varying(255),
            "アルゴ注文情報" character varying(255),
            "逆指値条件" character varying(255),
            "セット注文条件" character varying(255),
            "信用区分(弁済期限)" character varying(255),
            "注文数量[株/口]" integer,
            "約定数量[株/口]" integer,
            "注文単価[円]" numeric,
            "約定単価[円]" numeric,
            "現在値[円]" numeric,
            "約定代金[円]" numeric,
            "手数料[円]" numeric
            PRIMARY KEY (id_order)
        )
    '''
    return sql
