from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func
from paytrack.database import Base

# ORM classes
class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(30), nullable=False, unique=True)
    enabled = Column(Boolean, default=True, nullable=False)
    paygate_form = Column(String(20), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return '<Account %r>' % (self.id)

class Credit(Base):
    __tablename__ = 'credit'
    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(Enum('requested', 'approved', 'rejected'), nullable=False)
    amount = Column(Float, nullable=False)
    credit_type = Column(Enum('discount', 'barter'), nullable=False)
    payer_id = Column(Integer, ForeignKey('payer.id'), nullable=False)
    payer = relationship('Payer')
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    account = relationship('Account')
    expires_at = Column(DateTime, nullable=True)
    reviewer_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    reviewer = relationship('User')
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return '<Credit %r>' % (self.id)

class Invoice(Base):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(Enum('draft', 'sent', 'canceled'), nullable=False)
    paid = Column(Boolean, default=False, nullable=False)
    amount = Column(Float, nullable=False)
    payer_id = Column(Integer, ForeignKey('payer.id'), nullable=False)
    payer = relationship('Payer')
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    account = relationship('Account')
    expires_at = Column(DateTime, nullable=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return '<Invoice %r>' % (self.id)

class Payer(Base):
    __tablename__ = 'payer'
    id = Column(Integer, primary_key=True, nullable=False)
    fname = Column(String(30), nullable=False)
    lname = Column(String(30), nullable=False)
    email = Column(String(100), nullable=False)
    credits = relationship('Credit')
    invoices = relationship('Invoice')
    payments = relationship('Payment')
    refunds = relationship('Refund')
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return '<Payer %r>' % (self.email)

class Payment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(Enum('paid', 'error'), nullable=False)
    amount = Column(Float, nullable=False, default=0)
    payer_id = Column(Integer, ForeignKey('payer.id'), nullable=False)
    payer = relationship('Payer')
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    account = relationship('Account')
    invoice_id = Column(Integer, ForeignKey('invoice.id'), nullable=False)
    invoice = relationship('Invoice')
    payment_type = Column(Enum('paygate', 'creditcard', 'check', 'cash'), nullable=False)
    reviewer_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    reviewer = relationship('User')
    trans_decision = Column(String(25), nullable=True)
    trans_reference = Column(String(25), nullable=True)
    trans_id = Column(String(25), nullable=True)
    trans_time = Column(String(25), nullable=True)
    trans_sig = Column(String(50), nullable=True)
    refunds = relationship('Refund')
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return '<Payment %r>' % (self.id)

class Refund(Base):
    __tablename__ = 'refund'
    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(Enum('requested', 'approved', 'rejected'), nullable=False)
    amount = Column(Float, nullable=False)
    payer_id = Column(Integer, ForeignKey('payer.id'), nullable=False)
    payer = relationship('Payer')
    payment_id = Column(Integer, ForeignKey('payment.id'), nullable=False)
    payment = relationship('Payment')
    reviewer_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    reviewer = relationship('User')
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return '<Refund %r>' % (self.id)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    netid = Column(String(25), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return '<User %r>' % (self.netid)
