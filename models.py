from sqlalchemy import Column, String
from database import Base


class URLMap(Base):
    __tablename__ = "urls"

    code = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
