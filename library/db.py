from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stock_tracer.library import get_configuration

config = get_configuration("global")
db_base_url = config["db_base_url"]

db_name_ut = config["db_name_ut"]
db_ut_url = db_base_url + "/" + db_name_ut
engine_ut = create_engine(db_ut_url)

db_name_prod = config["db_name_prod"]
db_prod_url = db_base_url + "/" + db_name_prod
engine_prod = create_engine(db_prod_url)

Session = sessionmaker(expire_on_commit=False)

@contextmanager
def transaction(env="Prod"):
    engine = engine_prod if env == "Prod" else engine_ut
    session = Session(bind=engine)

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
