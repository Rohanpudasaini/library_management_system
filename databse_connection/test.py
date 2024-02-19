from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from connect_db import engine, session


class Base(DeclarativeBase):
    pass


class UserAddress(Base):
    __tablename__ = 'userAddress'
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    address_id = Column('address_id', Integer, ForeignKey('addresses.id'))

    def __repr__(self) -> str:
        return f'{self.__tablename__ = } and {self.name = }'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String())
    addresses = relationship("Address", secondary='userAddress', back_populates='users')

    def __repr__(self) -> str:
        return f'{self.__tablename__ = } and {self.name = }'


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    # user_id = Column(Integer, ForeignKey('users1.id'))
    users = relationship('User', secondary='userAddress', back_populates='addresses')

    def __repr__(self) -> str:
        return f'{self.__tablename__ = } and {self.name = }'


# Base.metadata.create_all(engine)

# gmail = Address(email="gmail")
# yahoo = Address(email="Yahoo")
# proton_mail = Address(email='proton mail')
# rohan =     User(name='Rohan1')
# kaushal = User(name='Kaushal1')
# ganesh =   User(name='Ganesh1')
# address1 = Address(email)

# session.add_all([rohan, kaushal, ganesh])
# new_user = User(name='Rohan Pudasaini')
# new_address = Address(email='test@test.com', user=new_user)
# session.add(new_user)

result = session.query(User).filter(User.name =='Rohan1').first()
new_address= Address(email='Something_new')
result.addresses.append(new_address) 
session.add_all([new_address,result])



session.commit()
