from sqlalchemy import create_engine, MetaData
import DBsettings

engine = create_engine(
	DBsettings.db.string, echo=False, client_encoding="UTF-8"
)

metadata_obj = MetaData(bind=engine)
connection = engine.connect()