from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
"""
sql table using sqlachemy
"""

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    fileId = db.Column(db.Integer)
    receivedDate = db.Column(db.Date)
    topic = db.Column(db.String(150))
    profession = db.Column(db.String(150))
    detailedProfessionCategory = db.Column(db.String(150))
    tenderingList = db.Column(db.String(150))
    winner = db.Column(db.String(150))
    scopeOfWork = db.Column(db.String(150))
    majorTerms = db.Column(db.String(1500))
    totalPrice = db.Column(db.String(150))
    unitPrice = db.Column(db.String(150))
    currency = db.Column(db.String(150))
    exchangeRate = db.Column(db.String(150))
    moblizationTime= db.Column(db.String(150))
    moblizationCost = db.Column(db.String(150))
    tax = db.Column(db.String(150))
    localContent = db.Column(db.String(150))
    handleDate = db.Column(db.String(150))
    personInCharge = db.Column(db.String(150))
    internalApprovedDate = db.Column(db.String(150))
    headOfficeApprovedDate = db.Column(db.String(150))
    responseDateToOperator = db.Column(db.String(150))
    remarks = db.Column(db.String(1500))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
