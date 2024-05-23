from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """ 
    This class gots settings form os variables
    """
    # Base
    debug: bool = False
    project_name: str = "osiris"
    
    # Database
    # ToDo after docker with postgres:
    # db_async_connection_str = "postgresql+asyncpg://postgres:postgres@localhost/asyncalchemy"
    db_async_connection_str: str = "sqlite+aiosqlite:///data.db"
    db_async_test_connection_str: str = ""

    # Logger
    logger_cfg: str = "osiris/conf/logger_cfg.yaml"