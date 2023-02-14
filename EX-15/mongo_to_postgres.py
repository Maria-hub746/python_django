from pymongo import MongoClient
import configparser
import psycopg2
from psycopg2 import sql

l_authors = []
l_quotes = []
l_tags = []

conf = configparser.ConfigParser()
conf.read('settings.ini')

def from_mongo():
    global l_tags
    m_user = conf.get('mongo', 'user')
    m_pass = conf.get('mongo', 'pass')
    m_db = conf.get('mongo', 'db_name')
    m_domain = conf.get('mongo', 'domain')

    url = f'mongodb+srv://{m_user}:{m_pass}@{m_domain}/{m_db}?retryWrites=true&w=majority'
    mongo = MongoClient(url)
    mongodb = mongo[m_db]
    quotes = mongodb.quotes.find()
    authors = mongodb.authors.find()

    for el in authors:
        l_authors.append({
            'fullname': el['fullname'],
            'born_date': el['born_date'],
            'born_location': el['born_location'],
            'description': el['description']
        })

    tags = set()
    for el in quotes:
        [tags.add(tag) for tag in el['tags']]
    l_tags = list(tags)

    index = 1
    quotes = mongodb.quotes.find()
    for el in quotes:
        tags = []
        for tag in el['tags']:
            tags.append((index, l_tags.index(tag) + 1))
        author_name = mongodb.authors.find_one({"_id": el['author']})['fullname']
        id_author = None
        for i in range(len(l_authors)):
            if l_authors[i]['fullname'] == author_name:
                id_author = i + 1
        l_quotes.append({
            'quote': el['quote'],
            'author': id_author,
            'tags': tags
        })
        index += 1

def to_postgress():
    conn = psycopg2.connect(dbname=conf.get('postgres', 'db'), user=conf.get('postgres', 'user'),
                            password=conf.get('postgres', 'password'), host=conf.get('postgres', 'host'),
                            port=conf.get('postgres', 'port'))
    cursor = conn.cursor()

    cursor.execute('DELETE FROM quotesapp_tags')
    cursor.execute('DELETE FROM quotesapp_authors')
    cursor.execute('DELETE FROM quotesapp_quotes')
    cursor.execute('DELETE FROM quotesapp_quotes_tags')
    conn.commit()

    tags = [(l_tags[i]) for i in range(len(l_tags))]
    insert = sql.SQL('INSERT INTO quotesapp_tags (name) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, tags))
    )
    cursor.execute(insert)
    conn.commit()

    authors = [(l_authors[i]['fullname'], l_authors[i]['born_date'], l_authors[i]['born_location'], l_authors[i]['description']) for i in range(len(l_authors))]
    insert = sql.SQL('INSERT INTO quotesapp_authors (fullname, born_date, born_location, description) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, authors))
    )
    cursor.execute(insert)
    conn.commit()

    quotes = [(l_quotes[i]['quote'], l_quotes[i]['author']) for i in range(len(l_quotes))]
    insert = sql.SQL(
        'INSERT INTO quotesapp_quotes (quote, author_id) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, quotes))
    )
    cursor.execute(insert)
    conn.commit()

    quotes_tags = []
    for quote in l_quotes:
        for tag in quote['tags']:
            quotes_tags.append((tag[0], tag[1]))
    insert = sql.SQL(
        'INSERT INTO quotesapp_quotes_tags (quotes_id, tags_id) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, quotes_tags))
    )
    cursor.execute(insert)
    conn.commit()

    cursor.close()
    conn.close()


if __name__ == '__main__':
    print('from mongo.......')
    from_mongo()
    print('to postgres.......')
    to_postgress()
    print('done.')