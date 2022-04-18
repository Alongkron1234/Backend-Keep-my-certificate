from database import Base
from sqlalchemy import Column, Integer, String

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    name = Column(String, nullable=False)
    content = Column(String, nullable=False)


