import os
import sys
from database import Base, engine
from parse_cj import main
from zipcode.fetch_zipcode import download_zip_to_memory
from zipcode.fetch_zipcode import extract_zip
from zipcode import path
import asyncio


def init_db():
    try:
        os.remove('db.sqlite')
    except OSError:
        print('Error on deleting database file')

    from models import Address
    Base.metadata.create_all(engine)


def fetch_zipcode():
    zipfile = download_zip_to_memory(path.EPOST_ALL_URL)
    extract_zip(zipfile, path.DATA_PATH)


def parse_cj():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()


if sys.argv[1] == 'init_db':
    init_db()
elif sys.argv[1] == 'fetch_zipcode':
    fetch_zipcode()
elif sys.argv[1] == 'parse_cj':
    parse_cj()
