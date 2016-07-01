from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from stock_tracer.common import Configuration

db_base_url = Configuration.get("db_base_url")

db_name_ut = Configuration.get("db_name_ut")
db_ut_url = db_base_url + "/" + db_name_ut
engine_ut = create_engine(db_ut_url)

db_name_prod = Configuration.get("db_name_prod")
db_prod_url = db_base_url + "/" + db_name_prod
engine_prod = create_engine(db_prod_url)

Session = scoped_session(sessionmaker(expire_on_commit=False))

@contextmanager
def transaction(tx=None):
    if tx:
        yield tx
    else:
        is_unit_test = Configuration.get("__unit_test__")
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
            Session.remove()
