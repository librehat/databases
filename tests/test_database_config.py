from databases import DatabaseConfig


def test_database_config_repr():
    u = DatabaseConfig.from_url("postgresql://localhost/name")
    assert repr(u) == "DatabaseConfig('postgresql://localhost/name')"

    u = DatabaseConfig.from_url("postgresql://username@localhost/name")
    assert repr(u) == "DatabaseConfig('postgresql://username@localhost/name')"

    u = DatabaseConfig.from_url("postgresql://username:password@localhost/name")
    assert repr(u) == "DatabaseConfig('postgresql://username:********@localhost/name')"


def test_database_config_properties():
    u = DatabaseConfig.from_url("postgresql+asyncpg://username:password@localhost:123/mydatabase")
    assert u.dialect == "postgresql"
    assert u.driver == "asyncpg"
    assert u.username == "username"
    assert u.password == "password"
    assert u.hostname == "localhost"
    assert u.port == 123
    assert u.database == "mydatabase"


def test_database_config_options():
    url = "postgresql://localhost/mydatabase?pool_size=20&ssl=true"
    u = DatabaseConfig.from_url(url)
    assert u.options == {"pool_size": "20", "ssl": "true"}
    assert u.to_url() == url


def test_replace_database_config_components():
    u = DatabaseConfig.from_url("postgresql://localhost/mydatabase")

    assert u.database == "mydatabase"
    new = u.replace(database="test_" + u.database)
    assert new.database == "test_mydatabase"
    assert str(new) == "postgresql://localhost/test_mydatabase"

    assert u.driver == ""
    new = u.replace(driver="asyncpg")
    assert new.driver == "asyncpg"
    assert str(new) == "postgresql+asyncpg://localhost/mydatabase"

    assert u.port is None
    new = u.replace(port=123)
    assert new.port == 123
    assert str(new) == "postgresql://localhost:123/mydatabase"

    u = DatabaseConfig.from_url("sqlite:///mydatabase")
    assert u.database == "mydatabase"
    new = u.replace(database="test_" + u.database)
    assert new.database == "test_mydatabase"
    assert str(new) == "sqlite:///test_mydatabase"

    u = DatabaseConfig.from_url("sqlite:////absolute/path")
    assert u.database == "/absolute/path"
    new = u.replace(database=u.database + "_test")
    assert new.database == "/absolute/path_test"
    assert str(new) == "sqlite:////absolute/path_test"
