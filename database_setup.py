#!/usr/bin/env python
''' Set up database '''
from sqlalchemy import (Column, Integer, String, DateTime, create_engine,
        ForeignKey)
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import logging
import yaml

BASE = declarative_base()

class Database(object):
    ''' Database class for schema and sessions '''
    def __init__(self, host, db_name, user, passwd):
        self.host = host
        self.db_name = db_name
        self.user = user
        self.passwd = passwd

        self.engine = create_engine("postgres://{user}:{passwd}@{host}/{name}".format(
            user=self.user,
            passwd=self.passwd,
            host=self.host,
            name=self.db_name), echo=True)

    def session(self):
        session = sessionmaker(bind=self.engine)
        #session = Session()
        return session()
# Tables
class Media(BASE):
    ''' Media table '''
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_date = Column(DateTime)
    scrubbed_file_name = Column(String)
    #local = relationship("Local", uselist=False, backref="local")
    #remote = relationship("Remote", uselist=False, backref="remote")

    def __repr__(self):
        return '''
<Media(file_name='{file_name}', file_date='{file_date}', \
scrubbed_file_name='{scrubbed_file_name}')>'''.format(
            file_name=self.file_name,
            file_date=self.file_date,
            scrubbed_file_name=self.scrubbed_file_name
            )

class Local(BASE):
    ''' Local table '''
    __tablename__ = 'local'

    id = Column(Integer, primary_key=True)
    media_fk = Column(Integer, ForeignKey('media.id'))
    status = Column(String)
    retrieved_date = Column(DateTime)

    def __repr__(self):
        return "<Local(media_fk='{media_fk}', retrieved_date='{retrieved_date}',\
        status='{status}')>".format(
            media_fk=self.media_fk,
            retrieved_date=self.retrieved_date,
            status=self.status
            )

class Remote(BASE):
    ''' Remote table '''
    __tablename__ = 'remote'

    id = Column(Integer, primary_key=True)
    media_fk = Column(Integer, ForeignKey('media.id'))
    date_found = Column(DateTime)
    local = relationship("Local", uselist=False, backref="remote")

    def __repr__(self):
        return "<Local(media_fk='{media_fk}', date_found='{date_found}')>".format(
            media_fk=self.media_fk,
            date_found=self.date_found
            )

if __name__ == "__main__":
    try:
        stream = file('config.yml', 'r')
        cfg = yaml.load(stream)
    except Exception as error:
        logging.error(error)
        raise SystemExit(1)

    db_hostname = cfg['host']
    db_name = cfg['db_name']
    db_user = cfg['user']
    db_pass = cfg['passwd']

    database = Database(host=db_hostname, db_name=db_name, user=db_user,
        passwd=db_pass)
    engine = database.engine
    BASE.metadata.create_all(engine)
