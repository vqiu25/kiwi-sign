import sqlite3

def connectDB():
    connection = sqlite3.connect('kiwisl.db')
    cursor = connection.cursor()
    return {connection, cursor}

def closeDB(connection):
    connection.close()

def setUpWordsTable(connection, cursor, words):
    cursor.execute(
        '''
        DROP TABLE IF EXISTS words
        '''
    )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS words (
            word TEXT PRIMARY KEY,
            seen INTEGER NOT NULL DEFAULT 0
        )
        '''
    )
    for category in words:
        for word in words.get(category):
            cursor.execute(
                '''
                INSERT INTO words (word) VALUES (?)
                ''', 
                (word,)
            )
    connection.commit()

def printTable(cursor, table):
    cursor.execute(
        '''
        SELECT * FROM {}
        '''.format(table)
    )
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def checkWord(cursor, word):
    cursor.execute(
        '''
        SELECT seen FROM words WHERE word = ?
        ''',
        (word,)
    )
    return cursor.fetchone()[0] == 1

def seenWord(connection, cursor, word):
    cursor.execute(
        '''
        UPDATE words SET seen = 1 WHERE word = ?
        ''',
        (word,)
    )
    connection.commit()