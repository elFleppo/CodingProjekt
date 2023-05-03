from lxml import etree
import sqlite3 as sqlite3
dblp_record_types_for_publications = ('article', 'inproceedings', 'proceedings', 'book', 'incollection',
    'phdthesis', 'masterthesis', 'www', 'author')
parser = etree.XMLParser(dtd_validation=True)
dtd = etree.DTD("dblp.dtd")
context = etree.iterparse("dblp.xml", events=('start', 'end'), load_dtd=True, #pylint: disable=E1101
    resolve_entities=True)
context = iter(context)
event, root = next(context)
n_records_parsed = 0

conn = sqlite3.connect("dblp.db")
conn.execute("CREATE TABLE IF NOT EXISTS publications (title VARCHAR(200), year INTEGER)")
conn.execute("CREATE TABLE IF NOT EXISTS authors (name VARCHAR(100))")
conn.execute("CREATE TABLE IF NOT EXISTS authored (name VARCHAR(100), title VARCHAR(200))")
for event, elem in context:
    if event == 'end' and elem.tag in dblp_record_types_for_publications:
        pub_year = None
        for year in elem.findall('year'):
            pub_year = year.text
        if pub_year is None:
            continue

        pub_title = None
        for title in elem.findall('title'):
            pub_title = title.text
        if pub_title is None:
            continue

        pub_authors = []
        for author in elem.findall('author'):
            if author.text is not None:
                pub_authors.append(author.text)

        #print(pub_year)
        #print(pub_title)
        #print(pub_authors)
        # insert the publication, authors in sql tables
        pub_title_sql_str = pub_title.replace("'", "''")
        pub_author_sql_strs = []
        for author in pub_authors:
            pub_author_sql_strs.append(author.replace("'", "''"))

        conn.execute("INSERT OR IGNORE INTO publications VALUES ('{title}','{year}')".format(
            title=pub_title_sql_str,
            year=pub_year))
        for author in pub_author_sql_strs:
            conn.execute("INSERT OR IGNORE INTO authors VALUES ('{name}')".format(name=author))
            conn.execute("INSERT INTO authored VALUES ('{author}','{publication}')".format(author=author,
                                                                                           publication=pub_title_sql_str))
        elem.clear()
        root.clear()

        n_records_parsed += 1
        print("No. of records parsed: {}".format(n_records_parsed))

