import datetime

from api import db


class GeolocationModel(db.Model):
    __tablename__ = "geolocation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String, nullable=False)
    hostname = db.Column(db.String, nullable=False)
    country_code = db.Column(db.String, nullable=False)  # should be a foreign key to a country table
    city = db.Column(db.String, nullable=False)  # same here
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "ip": self.ip,
            "country": self.country_code,
            "hostname": self.hostname,
            "city": self.city,
            "timestamp": self.timestamp,
        }
