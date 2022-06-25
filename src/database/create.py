from sqlalchemy import create_engine, MetaData
import DBsettings
import sqlalchemy

engine = create_engine(
	DBsettings.db.string, echo=False, client_encoding="UTF-8"
)


connection = engine.connect()


def create():
	metadata_obj = MetaData(bind=engine)
	res = metadata_obj.tables.keys()

	if "ctf_table" not in res:
		ctf_table = sqlalchemy.Table(
			"ctf_table",
			metadata_obj,
			sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
			sqlalchemy.Column("name", sqlalchemy.String),
			sqlalchemy.Column("date", sqlalchemy.String, nullable=False),
			sqlalchemy.Column("active", sqlalchemy.Boolean, nullable=False)
		)
	else:
		ctf_table = sqlalchemy.Table(
			"ctf_table", metadata_obj, autoload_with=engine
		)

	if "ctf_teams" not in res:
		ctf_teams = sqlalchemy.Table(
			"ctf_teams",
			metadata_obj,
			sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
			sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
			sqlalchemy.Column("leader", sqlalchemy.String, nullable=False),
			sqlalchemy.Column("members", sqlalchemy.types.ARRAY(sqlalchemy.String), nullable = True),
			sqlalchemy.Column("points", sqlalchemy.Integer, nullable=True),
			sqlalchemy.Column("ctf_id", None, sqlalchemy.ForeignKey("ctf_table.id"))
	)
	else:
		ctf_teams = sqlalchemy.Table(
			"ctf_teams", metadata_obj, autoload_with=engine
		)

	metadata_obj.create_all()

	return ctf_table, ctf_teams


ctf_table, ctf_teams = create()