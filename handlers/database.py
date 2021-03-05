from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

mysql_engine = create_engine('mysql+mysqldb://root:Admin10!@localhost:3306/nt_desktop_app')


def get_session():
    session_class = sessionmaker(bind=mysql_engine)  # session_class is a real class :)
    return session_class()  # return an instance of session_class class.
