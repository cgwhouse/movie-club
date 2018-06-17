from sqlite3 import connect, IntegrityError
from csv import DictReader
from sys import argv


def main():
    insert_company_string = 'INSERT INTO Company VALUES (NULL, ?, ?, ?, ?, ?, ?, ?);'
    insert_hq_string = 'INSERT INTO HQ VALUES (?, ?, ?, ?, ?, ?);'
    insert_alias_string = 'INSERT INTO Alias VALUES (?, ?, ?);'
    insert_sector_string = 'INSERT INTO Sector VALUES (NULL, ?);'
    insert_industry_string = 'INSERT INTO Industry VALUES (NULL, ?);'
    insert_ceo_title_string = 'INSERT INTO CeoTitle VALUES (NULL, ?);'
    insert_year_rank_string = 'INSERT INTO YearRank VALUES (?, ?, ?, ?, ?, ?);'

    conn = connect(argv[1])
    c = conn.cursor()

    createTables(c)

    with open('raw_data.csv', encoding="utf8") as mfile:
        reader = DictReader(mfile)
        for row in reader:
            sector_id = doSector(c, insert_sector_string, row)
            industry_id = doIndustry(c, insert_industry_string, row)
            ceo_title_id = doCeoTitle(c, insert_ceo_title_string, row)
            company_id = doCompany(
                c, insert_company_string, row, sector_id, industry_id, ceo_title_id)
            doHQ(c, insert_hq_string, row, company_id)
            doAlias(c, insert_alias_string, row, company_id)
            doYearRank(c, insert_year_rank_string, row, company_id)
    conn.commit()
    conn.close()


def createTables(cursor):
    with open('createTables.sql', encoding='utf8') as createScript:
        script = createScript.read()
        cursor.executescript(script)


def doSector(cursor, insert_string, row):
    try:
        cursor.execute(insert_string, (row['Sector'],))
        sector_id = cursor.lastrowid
    except IntegrityError:
        cursor.execute(
            'SELECT sector_ID FROM Sector WHERE sector = ?;', (row['Sector'],))
        sector_id = cursor.fetchone()[0]
    return sector_id


def doIndustry(cursor, insert_string, row):
    try:
        cursor.execute(insert_string, (row['Industry'],))
        industry_id = cursor.lastrowid
    except IntegrityError:
        cursor.execute(
            'SELECT industry_ID FROM Industry WHERE industry = ?;', (row['Industry'],))
        industry_id = cursor.fetchone()[0]
    return industry_id


def doCeoTitle(cursor, insert_string, row):
    try:
        cursor.execute(insert_string, (row['Ceo-title'],))
        ceo_title_id = cursor.lastrowid
    except IntegrityError:
        cursor.execute(
            'SELECT ceo_title_ID FROM CeoTitle WHERE title = ?;', (row['Ceo-title'],))
        ceo_title_id = cursor.fetchone()[0]
    return ceo_title_id


def doCompany(cursor, insert_string, row, sector_id, industry_id, ceo_title_id):
    try:
        cursor.execute(insert_string, (row['Title'], row['Website'], row['Ceo'],
                                       row['Employees'], sector_id, industry_id, ceo_title_id))
        company_id = cursor.lastrowid
    except IntegrityError:
        cursor.execute(
            'SELECT company_ID FROM Company WHERE title = ?;', (row['Title'],))
        company_id = cursor.fetchone()[0]
    return company_id


def doHQ(cursor, insert_string, row, company_id):
    try:
        cursor.execute(insert_string, (company_id,
                                       row['Hqaddr'], row['Hqcity'], row['Hqstate'], row['Hqzip'], row['Hqtel']))
    except IntegrityError:
        pass


def doAlias(cursor, insert_string, row, company_id):
    try:
        cursor.execute(insert_string, (company_id,
                                       row['Ticker'], row['Fullname']))
    except IntegrityError:
        cursor.execute(
            'SELECT full_name FROM Alias WHERE company_ID = ?;', (company_id,))
        current_full = cursor.fetchone()[0]
        if len(row['Fullname']) > len(current_full):
            cursor.execute(
                'UPDATE Alias SET full_name = ? WHERE company_ID = ?;', (row['Fullname'], company_id))


def doYearRank(cursor, insert_string, row, company_id):
    cursor.execute(insert_string, (company_id,
                                   row['Year'], row['Rank'], row['Revenues'], row['Profits'], row['Assets']))


main()
