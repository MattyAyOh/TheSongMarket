import sqlite3
import os

def create_database():
    print 'Creating Database...'
    db = sqlite3.connect('records.sqlite')
    db.execute('CREATE TABLE IF NOT EXISTS `ytviewcount` ( \
    `trackid`   INTEGER NOT NULL, \
    `artistid`  INTEGER NOT NULL, \
    `spotifyuri`    TEXT NOT NULL, \
    `youtubeuri`    TEXT NOT NULL, \
    `viewcount` INTEGER NOT NULL, \
    PRIMARY KEY(trackid))')
    db.execute('CREATE TABLE IF NOT EXISTS `artistaverages` ( \
    `artistid`  INTEGER NOT NULL, \
    `average` INTEGER NOT NULL, \
    PRIMARY KEY(artistid))')
    db.commit()
    db.close()

def check_database():
    # if not os.path.exists('records.sqlite'):
    create_database()
