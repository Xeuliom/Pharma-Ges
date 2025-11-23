# core/inventory_manager.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.db_setup import Medicine

engine = create_engine('sqlite:///pharmacy.db')
Session = sessionmaker(bind=engine)
session = Session()

def get_all_medicines():
    return session.query(Medicine).all()

def add_medicine(name, category, price, quantity, expiry_date):
    medicine = Medicine(
        name=name,
        category=category,
        price=price,
        quantity=quantity,
        expiry_date=expiry_date
    )
    session.add(medicine)
    session.commit()

def update_medicine(med_id, name, category, price, quantity, expiry_date):
    medicine = session.query(Medicine).get(med_id)
    if medicine:
        medicine.name = name
        medicine.category = category
        medicine.price = price
        medicine.quantity = quantity
        medicine.expiry_date = expiry_date
        session.commit()

def delete_medicine(med_id):
    medicine = session.query(Medicine).get(med_id)
    if medicine:
        session.delete(medicine)
        session.commit()
