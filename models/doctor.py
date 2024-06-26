#!/usr/bin/python3
"""Defines the Doctor class."""
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app import Base
from sqlalchemy.orm import relationship
import bcrypt


class Doctor(Base):
    """Represents the Doctor."""

    __tablename__ = 'Doctor'
    DoctorID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    FullName = Column(String(100), nullable=True)
    SpecialtyID = Column(Integer, ForeignKey('Specialty.SpecialtyID'),
                         nullable=True)
    LocationID = Column(Integer, ForeignKey('Location.LocationID'),
                        nullable=True)
    AppointmentDateTime = Column(DateTime, nullable=True)

    Email = Column(String(75), nullable=True)
    Password = Column(String(128), nullable=False)

    specialty = relationship("Specialty", back_populates="doctors")
    location = relationship("Location", back_populates="doctors")
    appointments = relationship("Appointment", back_populates="doctor")
    reviews = relationship("Review", back_populates="doctor")
    availabilities = relationship("Availability", back_populates="doctor")


    def serialize(self):
        """Serialize Doctor object to a dictionary."""
        return {
                'DoctorID': self.DoctorID,
                'FullName': self.FullName,
                'SpecialtyID': self.SpecialtyID,
                'LocationID': self.LocationID,
                'AppointmentDateTime': self.AppointmentDateTime.
                strftime("%Y-%m-%d %H:%M:%S")
                if self.AppointmentDateTime else None
        }

    def set_password(self, password):
        """Hashes and sets the doctor's password."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.Password = hashed_password.decode('utf-8')


    def check_password(self, password):
        """Verifies the provided password against the hashed password."""
        return bcrypt.checkpw(password.encode('utf-8'), self.Password.encode('utf-8'))
