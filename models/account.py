from sqlalchemy import Column, Integer, String, DateTime

from .db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    # create_time = Column(DateTime, default=datetime.now())
    # _locked = Column(Boolean, default=0, nullable=False)

    def __repr__(self):
        return "<User(#{}:{})".format(self.id, self.username)
