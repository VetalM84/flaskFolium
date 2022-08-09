"""Models for the maps' app."""

from maps import db
from dataclasses import dataclass


@dataclass
class Report(db.Model):
    """Report model. With ability to export to JSON."""

    __tablename__ = "Reports"

    id: int
    latitude: float
    longitude: float
    color: str
    comment: str
    created_at: str
    ip: str

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now())
    ip = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return f"<Отчет №{self.id} от {self.created_at}>"
