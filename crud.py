from db import session
from models import Currency, Users, UserCurrencies
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


class DataBaseSession:
    def __init__(self) -> None:
        self.session = session


class DatabaseWrite(DataBaseSession):

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def check_user_in_users_db(cls, user_id):
        try:
            query = session.query(Users
                                  ).filter_by(user_id=user_id
                                              ).one()
        except NoResultFound as empty:
            print(empty, 'and was added')
            return True
        else:
            if query.user_id == user_id:
                return False

    def insert_user_to_db(self, user_id):
        try:
            if self.check_user_in_users_db(user_id):
                return add_to_db(Users(user_id=user_id))
        except Exception as ex:
            print('\n', ex)

    @classmethod
    def check_user_in_user_currency_db(
        cls,
        user: int
    ):
        try:
            query = session.query(UserCurrencies).filter_by(user_id=user).one()
            if query.user_id == user:
                return False
        except Exception as ex:
            print(ex)
            return True

    def insert_currency_to_db(self,
                              user: int,
                              first_currency: str,
                              second_currency: str):
        try:
            if self.check_user_in_user_currency_db(user=user):
                currency_to_db = UserCurrencies(
                        user_id=user,
                        first_currency_short_name=first_currency,
                        second_currency_short_name=second_currency)
                return add_to_db(currency_to_db)
        except TypeError as type_error:
            print(type_error, 'raise in insert_currency ')

    def add_to_db(self, object):
        try:
            session.add(object)
        except Exception as ex:
            session.rollback()
            print(ex)
        else:
            session.commit()
            session.close()


class DatabaseRead(DataBaseSession):

    def __init__(self) -> None:
        super().__init__()

    def get_user_currency(self, user, tumbler=True):
        try:
            query = session.query(
                    UserCurrencies).filter_by(user_id=user).one()
            if tumbler:
                return query.first_currency_short_name
            return query.second_currency_short_name

        except Exception as ex:
            print(ex)

    @classmethod
    def currency_values(cls, user):
        values = []
        first_currency = query_currency(user=user)
        second_currency = query_currency(user=user, tumbler=False)
        name_currency = [first_currency, second_currency]
        for name in name_currency:
            query = session.query(Currency).filter_by(
                short_name=name).one()
            values.append(query.currency_value)
        return values


class DatabaseUpdate(DataBaseSession):
    def __init__(self) -> None:
        super().__init__()

    def update_currency(self, user, currency, tumbler=True):
        try:
            user_user_currency = select(UserCurrencies
                                        ).where(UserCurrencies.user_id == user)
            user_currency = session.scalars(user_user_currency).one()

            if tumbler:
                user_currency.first_currency_short_name = currency
                return self.update_commit_or_rollback()
            else:
                user_currency.second_currency_short_name = currency
                return self.update_commit_or_rollback()

        except Exception as ex:
            print(ex)

    def update_currency_value(self, short_name, value):
        try:
 
            currency = select(Currency).where(
                Currency.short_name == short_name)
            new_currency = session.scalar(currency)
            new_currency.currency_value = value

            return self.update_commit_or_rollback()

        except Exception as ex:
            print(ex)

    def switch_user_currencies(self, user, currency):
        try:

            user_user_currency = select(UserCurrencies
                                        ).where(UserCurrencies.user_id == user)
            user_currency = session.scalars(user_user_currency).one()

            user_currency.first_currency_short_name = currency[1]
            user_currency.second_currency_short_name = currency[0]

            return self.update_commit_or_rollback()

        except Exception as ex:
            print(ex)

    @classmethod
    def update_commit_or_rollback(cls):
        try:
            session.commit()
        except Exception:
            session.rollback()


def query_currency(user, tumbler=True):
    """arg tumbler if True give main currency if False second"""
    currency = DatabaseRead()
    if tumbler:
        return currency.get_user_currency(user)
    return currency.get_user_currency(user, False)


def user_currency_update(user, currency, tumbler=True):
    update = DatabaseUpdate()
    try:
        if tumbler:
            return update.update_currency(user, currency)
        return update.update_currency(user, currency, False)
    except Exception as ex:
        print(ex)


def take_data_from_currency_db():
    try:
        query = session.query(Currency).all()
    except NoResultFound as empty:
        print(empty)
    else:
        return query


def check_user(user):
    try:
        query = session.query(Users
                              ).filter_by(user_id=user
                                          ).one()
    except NoResultFound as empty:
        print(empty)
        return True
    else:
        if query.user_id == user:
            return False


def add_to_db(to_db):
    try:
        session.add(to_db)
    except Exception as ex:
        session.rollback()
        print(ex)
    else:
        session.commit()
