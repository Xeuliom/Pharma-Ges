# database/db_setup.py
from sqlalchemy import create_engine, Column, Integer, ForeignKey, DateTime, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="admin")

class Medicine(Base):
    __tablename__ = 'medicines'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    expiry_date = Column(Date)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String, unique=True)

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    medicine_id = Column(Integer, ForeignKey('medicines.id'))
    quantity = Column(Integer)
    total_price = Column(Float)
    timestamp = Column(DateTime)

# Initialize DB
def get_engine():
    return create_engine('sqlite:///pharmacy.db')

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)

# Create a new user
def create_user(username, password, role="admin"):
    session = get_session()
    user = User(username=username, password=password, role=role)
    session.add(user)
    try:
        session.commit()
        print(f"User '{username}' created successfully.")
    except Exception as e:
        session.rollback()
        print(f"Failed to create user: {e}")
    finally:
        session.close()

# Create a new medicine
def create_medicine(name, category, price, quantity, expiry_date):
    session = get_session()
    medicine = Medicine(
        name=name,
        category=category,
        price=price,
        quantity=quantity,
        expiry_date=expiry_date if isinstance(expiry_date, date) else date.fromisoformat(expiry_date)
    )
    session.add(medicine)
    try:
        session.commit()
        print(f"Medicine '{name}' added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Failed to add medicine: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
    create_user("admin", "admin123")
    create_medicine("Paracetamol", "Painkiller", 1.5, 100, "2025-12-31")
