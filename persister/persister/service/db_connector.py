from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import drop_database

from persister.service.db_engine import DbEngine


class DbConnector(object):
    def __init__(self, db_access_data, db_name):
        """
        :type db_access_data: persister.model.db_access_data.DbAccessData
        :type db_name: str
        """
        self.db_access_data = db_access_data
        self.db_name = db_name
        self._cached_session = None

    def initialize_db(self):
        engine = self._get_engine()
        if not database_exists(engine.url):
            create_database(engine.url)
            self._register_entities()
            try:
                base_entity_class_meta = self._get_entity_class_metadata()
                base_entity_class_meta.create_all(engine)
            except Exception as e:
                print("Could not initialize DB. Details: {}".format(e))
        else:
            print("No need to initialize DB: {} is already initialized.".format(engine.url))

    def drop_db(self):
        engine = self._get_engine()
        if database_exists(engine.url):
            self._register_entities()
            try:
                base_entity_class_meta = self._get_entity_class_metadata()
                base_entity_class_meta.drop_all(self._get_engine())
                drop_database(engine.url)
            except Exception as e:
                print("Could not drop DB. Details: {}".format(e))
        else:
            print("Could not drop DB: the db: {} was already dropped.".format(engine.url))

    def get_db_session(self):
        """
        :rtype: sqlalchemy.orm.session.Session
        """
        if not self._cached_session or not self._cached_session.is_active:
            self._cached_session = self._init_new_session()
        return self._cached_session

    def _get_entity_class_metadata(self):
        base_entity_class = DbEngine.get_base_entity_class()
        return base_entity_class.metadata

    def _init_new_session(self):
        print("Creating new DB session...")
        session_constructor = sessionmaker(bind=self._get_engine())
        return session_constructor()

    def _get_engine(self):
        return DbEngine.get_engine(self.db_access_data, self.db_name)

    def _register_entities(self):
        """
        Imports all classes deriving from sqlalchemy Base class.
        Important to do before initializing / dropping DB schemas
        By the imports, SQL Alchemy acknowledges to have mapped classes under its control
        So it can drop / create schemas
        """
        print("Registering DB entities...")
        from persister.entity.feature import Feature
        from persister.entity.raw_feature import RawFeature, RawFeatureValue
        from persister.entity.plugin import Plugin
        from persister.entity.track import Track
        from persister.entity.track_source import TrackSource
        from persister.entity.segment import Segment
