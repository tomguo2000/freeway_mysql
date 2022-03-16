import time
from datetime import datetime
from app.database.db_types.JsonCustomType import JsonCustomType
from app.database.sqlalchemy_extension import db

class SettingModel(db.Model):
    """Defines attributes for the setting item, use it in Database table.

    Attributes:
        ...
    """

    # Specifying database table used for UserModel
    __tablename__ = "settings"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)

    # setting data
    key = db.Column(db.String(256), unique=True)
    # value = db.Column(db.String(512), nullable=False)
    value = db.Column(JsonCustomType)

    # other info
    # creation_date = db.Column(db.DECIMAL(20,7))   # mysql正常，sqlite会丢失精度
    # creation_date = db.Column(db.DATETIME())      # mysql手工改表的小数位正常，sqlite正常
    creation_date = db.Column(db.FLOAT(32))
    modification_date = db.Column(db.FLOAT(32))
    last_modification_username = db.Column(db.String(80))

    def __init__(self, key, value):
        """Initialises settingModel class with key, value."""
        # required fields

        self.key = key
        self.value = value

        # default fields
        self.creation_date = time.time()


    def json(self):
        """Returns Settingmodel object in json format."""
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "creation_date": self.creation_date,
            "modification_date": self.modification_date,
            "last_modification_username": self.last_modification_username,
        }

    def __repr__(self):
        """Returns the setting's key and value."""
        return f"Setting key {self.key}. Value is {self.value} ."

    @classmethod
    def find_by_key(cls, key: str) -> "SettingModel":
        """Returns the setting that has the key we searched for."""
        return cls.query.filter_by(key=key).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "SettingModel":
        """Returns the setting that has the id we searched for."""
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all_settings(cls):
        """Returns all the settings."""
        return cls.query.all()

    @classmethod
    def is_empty(cls) -> bool:
        """Returns a boolean if the Settingmodel is empty or not."""
        return cls.query.first() is None

    def save_to_db(self) -> None:
        """Adds a setting to the database."""
        db.session.add(self)
        db.session.commit()
        return self.id

    def delete_from_db(self) -> None:
        """Deletes a setting from the database."""
        db.session.delete(self)
        db.session.commit()
