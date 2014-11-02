import sqlite3

def create_database():
    print 'creating database'
    db = sqlite3.connect('vc.sqlite')
    db.execute('CREATE TABLE IF NOT EXISTS `viewcount` ( \
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

create_database()