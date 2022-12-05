from sqlalchemy import (Date, DECIMAL, Column,
                        Text, VARCHAR, Integer,
                        CheckConstraint, ForeignKeyConstraint,
                        )
from db import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)


class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True)
    short_name = Column(VARCHAR, nullable=False, unique=True)
    full_name = Column(Text, nullable=False)
    currency_value = Column(DECIMAL, nullable=False)
    date = Column(Date)


class UserCurrencies(Base):
    __tablename__ = 'user_currencies'
    user_currencies_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    first_currency_short_name = Column(VARCHAR, nullable=False)
    second_currency_short_name = Column(
        VARCHAR,
        CheckConstraint(
            'first_currency_short_name!=second_currency_short_name'
            ),
        nullable=False
        )
    ForeignKeyConstraint(['user_currencies.user_id'], ['users.id'])
    ForeignKeyConstraint(['user_currencies.first_currency_short_name'],
                         ['currency.id'])
    ForeignKeyConstraint(['user_currencies.second_currency_short_name'],
                         ['currency.id'])
