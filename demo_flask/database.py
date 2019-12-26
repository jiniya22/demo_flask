from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

engine = create_engine('mysql+mysqldb://test:test@localhost:3306/jiniworld_flask?charset=utf8', echo=False, convert_unicode=True, poolclass=NullPool)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
