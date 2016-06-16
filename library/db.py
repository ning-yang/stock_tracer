from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stock_tracer.library import Configuration


config = Configuration.getInstance()
db_base_url = config.get("db_base_url")

db_name_ut = config.get("db_name_ut")
db_ut_url = db_base_url + "/" + db_name_ut
engine_ut = create_engine(db_ut_url)

db_name_prod = config.get("db_name_prod")
db_prod_url = db_base_url + "/" + db_name_prod
engine_prod = create_engine(db_prod_url)

Session = sessionmaker(expire_on_commit=False)

@contextmanager
def transaction():
    is_unit_test = config.get("__unit_test__")
    engine = engine_ut if is_unit_test else engine_prod
    session = Session(bind=engine)

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
