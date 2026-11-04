from sqlalchemy.orm import Session
from app import models, schemas


# CREATE
def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(**employee.model_dump())

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee


# READ ALL
def get_employees(db: Session):
    return db.query(models.Employee).all()


# READ BY ID
def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()


# UPDATE
def update_employee(
    db: Session,
    employee_id: int,
    employee: schemas.EmployeeUpdate
):
    db_employee = get_employee(db, employee_id)

    if db_employee is None:
        return None

    update_data = employee.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)

    return db_employee


# DELETE
def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee(db, employee_id)

    if db_employee is None:
        return None

    db.delete(db_employee)
    db.commit()

    return db_employee