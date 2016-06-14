from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stock_tracer.library import get_configuration

config = get_configuration("global")
db_base_url = config["db_base_url"]

db_name_ut = config["db_name_ut"]
db_ut_url = db_base_url + "/" + db_name_ut

db_name_prod = config["db_name_prod"]
db_prod_url = db_base_url + "/" + db_name_prod

@contextmanager
def transaction(env="Prod"):
    if env == "Prod":
        engine = create_engine(db_prod_url)
    else:
        engine = create_engine(db_ut_url)

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
