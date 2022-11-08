from contextlib import contextmanager
from dataclasses import dataclass
import dbt.exceptions # noqa
from dbt.adapters.base import Credentials
import mysql.connector

from dbt.adapters.sql import SQLConnectionManager as connection_cls
from dbt.events import AdapterLogger
from typing import Optional
from databend_py import Client
from clickhouse_sqlalchemy import make_session


logger = AdapterLogger("databend")
@dataclass
class DatabendCredentials(Credentials):
    """
    Defines database specific credentials that get added to
    profiles.yml to connect to new adapter
    """
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    schema: str = "default"

    # Add credentials members here, like:
    # host: str
    # port: int
    # username: str
    # password: str

    _ALIASES = {
        "dbname":"database",
        "pass":"password",
        "user":"username"
    }
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            self.database = None

    def __post_init__(self):
        # mysql classifies database and schema as the same thing
        if (
            self.database is not None and
            self.database != self.schema
        ):
            raise dbt.exceptions.RuntimeException(
                f"    schema: {self.schema} \n"
                f"    database: {self.database} \n"
                f"On Databend, database must be omitted or have the same value as"
                f" schema."
            )
    @property
    def type(self):
        """Return name of adapter."""
        return "databend"

    @property
    def unique_field(self):
        """
        Hashed and included in anonymous telemetry to track adapter adoption.
        Pick a field that can uniquely identify one team/organization building with this adapter
        """
        return self.schema

    def _connection_keys(self):
        """
        List of keys to display in the `dbt debug` output.
        """
        return ("host","port","database", "schema", "user")

class DatabendConnectionManager(connection_cls):
    TYPE = "databend"


    @contextmanager
    def exception_handler(self, sql: str):
        """
        Returns a context manager, that will handle exceptions raised
        from queries, catch, log, and raise dbt exceptions it knows how to handle.
        """
        try:
            yield

        except Exception as e:
            logger.debug("Error running SQL: {}".format(sql))
            logger.debug("Rolling back transaction.")
            self.rollback_if_open()
            raise dbt.exceptions.RuntimeException(str(e))

    def begin(self):
        pass

    def commit(self):
        pass

    @classmethod
    def open(cls, connection):
        """
        Receives a connection object and a Credentials object
        and moves it to the "open" state.
        """
        if connection.state == "open":
            logger.debug("Connection is already open, skipping open.")
            return connection

        credentials = connection.credentials

        try:
            handle = mysql.connector.connect(
                host=credentials.host,
                port=credentials.port,
                user=credentials.username,
                password=credentials.password,
            )
        except Exception as e:
            logger.debug("Error opening connection: {}".format(e))
            connection.handle = None
            connection.state = "fail"
            raise dbt.exceptions.FailedToConnectException(str(e))
        connection.state = "open"
        connection.handle = handle
        return connection

    @classmethod
    def get_response(cls,cursor):
        """
        Gets a cursor object and returns adapter-specific information
        about the last executed command generally a AdapterResponse ojbect
        that has items such as code, rows_affected,etc. can also just be a string ex. "OK"
        if your cursor does not offer rich metadata.
        """
        # ## Example ##
        return "OK"
    
    @classmethod
    def get_status(cls, _):
        """
        Returns connection status
        """
        return "OK"
    
    @classmethod
    def get_credentials(cls, credentials):
        """
        Returns Databend credentials
        """
        return credentials

    def cancel(self, connection):
        """
        Gets a connection object and attempts to cancel any ongoing queries.
        """
        connection_name = connection.name
        logger.debug("Cancelling query '{}'", connection_name)
        connection.handle.close()
        logger.debug("Cancel query '{}'", connection_name)