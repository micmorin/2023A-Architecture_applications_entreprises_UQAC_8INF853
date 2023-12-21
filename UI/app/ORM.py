from sqlalchemy import Integer, String
import db_mod
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

class User(db_mod.db.Model):
    __tablename__ = "User"

    ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    Password: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.Username

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.ID)    
    
    def to_json(self):
        return {'username':self.Username}