import sqlite3 as sql


class Database:
    def __init__(self):
        conn = sql.connect('PCP_Database')
        cur = conn.cursor()
        cur.execute("create table if not exists Pumps (ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                    " SERIAL varchar (50) NOT NULL UNIQUE,"
                    " CAPACITY varchar(50) NOT NULL, BRAND varchar (20) NOT NULL, ELASTOMER varchar (20) NOT NULL,"
                    "  COMMENT text)")
        cur.execute("create table if not exists Records (ID INTEGER PRIMARY KEY AUTOINCREMENT ,"
                    "SERIAL_NO varchar(50) not null ,DATE date  not null"
                    ", EVENT varchar(50) not null , LOCATION varchar(50) not null,"
                    " CONDITION varchar(50) not null, CUM_RUN_LIFE integer not null"
                    ", COMMENTS text, FOREIGN KEY (SERIAL_NO) REFERENCES Pumps(SERIAL)"
                    "ON DELETE CASCADE) ")
        cur.execute("create table if not exists brand_lib (brand varchar (50) primary key NOT NULL)")
        cur.execute("create table if not exists capacity_lib (brand text NOT NULL ,pump_capacity varchar (50) )")
        cur.execute("create table if not exists elastomer_lib (brand text NOT NULL ,elastomer varchar (50) )")
        cur.execute("create table if not exists Admins (USERNAME varchar (50) NOT NULL ,"
                    " PASSWORD varchar (50) NOT NULL)")
        cur.execute("create table if not exists Users (USERNAME varchar (50) NOT NULL ,"
                    " PASSWORD varchar (50) NOT NULL)")
        cur.execute("create table if not exists BenchTest (SERIAL_NO varchar (50) NOT NULL ,"
                    " PUMP_MODEL varchar (50) NOT NULL,"
                    "PO_FROM varchar (50) NOT NULL, TEST_DATE date NOT NULL, TEST_TYPE varchar (50) NOT NULL, "
                    "EFF_MAX_LIFT INTEGER not null, SUMMARY text, RTR_INSP text, STR_INSP text,"
                    " TAGBAR_INSP text,COMMENT text, "
                    "TEST_FILE_LINK text)")
        cur.execute("create table if not exists Fields (Field varchar (50) primary key NOT NULL)")
        cur.execute("create table if not exists Fields_and_Wells (Fields varchar (50) NOT NULL ,Wells varchar (50) NOT NULL)")
        
        cur.execute ('select * from brand_lib where brand = "Select brand"')
        check1 = cur.fetchall()
        if len(check1) == 0 :
            cur.execute ('insert into brand_lib (brand) values ("Select brand")')
            conn.commit()
        else:
            pass

        cur.execute ('select * from elastomer_lib where brand = "Select brand" and elastomer = "Select elastomer type"')
        check2 = cur.fetchall()
        if len(check2) == 0 :
            cur.execute ('insert into elastomer_lib (brand,elastomer) values ("Select brand","Select elastomer type")')
            conn.commit()
        else:
            pass

        cur.execute ('select * from capacity_lib where brand = "Select brand" and pump_capacity = "Select pump model"')
        check3 = cur.fetchall()
        if len(check3) == 0 :
            cur.execute ('insert into capacity_lib (brand,pump_capacity) values ("Select brand","Select pump model")')
            conn.commit()
        else:
            pass

        cur.execute ('select * from Fields where Field = "Select field"')
        check4 = cur.fetchall()
        if len(check4) == 0 :
            cur.execute ('insert into Fields (Field) values ("Select field")')
            conn.commit()
        else:
            pass

        cur.execute ('select * from Fields_and_Wells where Fields = "Select field" and Wells = "Well No."')
        check5 = cur.fetchall()
        if len(check5) == 0 :
            cur.execute ('insert into Fields_and_Wells (Fields,Wells) values ("Select field","Well No.")')
            conn.commit()
        else:
            pass

