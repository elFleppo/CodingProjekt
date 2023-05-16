import re
from lxml import etree
import sqlite3 as sqlite3
import psycopg as psycopg
import html

dblp_record_types_for_publications = ('article', 'inproceedings', 'proceedings', 'book', 'incollection',
    'phdthesis', 'masterthesis', 'www', 'author')
parser = etree.XMLParser(dtd_validation=True)

dtd = etree.DTD("dblp.dtd")
context = etree.iterparse("dblp.xml", events=('start', 'end'), load_dtd=True, #pylint: disable=E1101
    resolve_entities=True, encoding="ISO-8859-1", remove_blank_text=True, huge_tree=True)
context = iter(context)
event, root = next(context)
n_records_parsed = 0

#conn = sqlite3.connect("dblp.db")
#conn.execute("CREATE TABLE IF NOT EXISTS publications (title VARCHAR(200), year INTEGER)")
#conn.execute("CREATE TABLE IF NOT EXISTS authors (name VARCHAR(100))")
#conn.execute("CREATE TABLE IF NOT EXISTS authored (name VARCHAR(100), title VARCHAR(200))")
conn = psycopg.connect(host="localhost", dbname="dblp", user="postgres", password="cds2023")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS publications (key VARCHAR(120) PRIMARY KEY NOT NULL, title VARCHAR(2500), pubyear VARCHAR(100), mdate varchar(50), publtype VARCHAR(50))")
cursor.execute("CREATE TABLE IF NOT EXISTS authors (orcid VARCHAR (100) NOT NULL PRIMARY KEY, name VARCHAR(100))")
cursor.execute("CREATE TABLE IF NOT EXISTS authored (orcid VARCHAR (100), key VARCHAR(120), name VARCHAR(100), title VARCHAR(2500))")
conn.commit()

try:
    for event, elem in context:
        if event == 'end' and elem.tag in dblp_record_types_for_publications:
            try:
                pub_year = None
                for year in elem.findall('year'):
                    pub_year = year.text
                    #print(pub_year)

                #if pub_year is None:
                 #   continue

                pub_title = None
                pub_key = None
                pub_mdate = None
                pub_publtype = None
                pub_title_sql_str = None
                for title in elem.findall('title'):
                    pub_title = title.text
                    pub_mdate = elem.attrib["mdate"]
                    pub_publtype = elem.attrib["publtype"]
                    pub_key = str(elem.attrib["key"])
                    print("TITLE ATTRIB:", pub_mdate, pub_key, pub_publtype)
                    cursor.execute(
                        "INSERT INTO publications VALUES ('{key}','{title}','{pubyear}','{mdate}','{publtype}')  ON CONFLICT DO NOTHING;".format(
                            key=pub_key, title=pub_title_sql_str, pubyear=pub_year, mdate=pub_mdate,
                            publtype=pub_publtype))
                    conn.commit()
                #if pub_title is None:
                 #   continue

                pub_authors = []
               # for author in elem.findall('author'):
               #     if author.text is not None:
               #         pub_authors.append(author.text)
               #         print(author.attrib["orcid"])
               #         print(author.attrib)
               #         orcid = author.attrib["orcid"]
                if elem.tag == "author":
                    pub_authors.append(elem.text)
                    print(elem.attrib["orcid"])
                    orcid = elem.attrib["orcid"]
            except KeyError as error:
               pass

            if pub_title_sql_str != None:
                pub_title_sql_str = pub_title.replace("'", "''")

            pub_author_sql_strs = []
            if pub_authors != None:
                for author in pub_authors:
                    pub_author_sql_strs.append(author.replace("'", "''"))

                #cursor.execute("INSERT INTO publications VALUES ('{key}','{title}','{pubyear}','{mdate}','{publtype}')  ON CONFLICT DO NOTHING;".format(key=pub_key, title=pub_title_sql_str, pubyear=pub_year,mdate=pub_mdate, publtype=pub_publtype))
                #conn.commit()
                for author in pub_author_sql_strs:
                    cursor.execute("INSERT INTO authors VALUES ('{orcid}','{name}')  ON CONFLICT DO NOTHING;".format(orcid=orcid, name=author))
                    cursor.execute("INSERT INTO authored VALUES ('{orcid}','{key}','{name}','{title}')  ON CONFLICT DO NOTHING;".format(orcid=orcid, key=pub_key, name=author, title=pub_title_sql_str))
                    conn.commit()
            elem.clear()
            root.clear()

            n_records_parsed += 1
            #print(n_records_parsed)

except etree.ParseError as error:
    error = str(error)
    match = re.search(r"\'([a-z]+)\'", error)
    new_string = match.group(1)
    new_string = "&" + new_string
    new_char = html.unescape(new_string)
    print(new_char)
    for match in error:
        error.replace(error, new_char)


cursor.close()
conn.close()