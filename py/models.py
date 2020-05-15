import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class LicencePlate(db.Model):
    __tablename__ = "licence_plate"
    __table_args__ = {"schema": "lp"}
    licence_plate_id = db.Column(db.Integer, primary_key=True)
    licence_plate = db.Column(db.String, nullable=False)
    insurance = db.Column(db.DateTime)
    address = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    # image = db.relationship("Image", backref="licenceplate", lazy=True)

    def __repr__(self):
        return self.licence_plate


class Complaint(db.Model):
    __tablename__ = "complaint"
    __table_args__ = {"schema": "lp"}
    complaint_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return self.licence_plate
