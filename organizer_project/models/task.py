import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from organizer_project import db


class Task(db.Model):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.datetime.now()
    )
    update_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    change_done_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    delete_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    @classmethod
    def add_task(cls, description: str):
        db.session.add(cls(description=description, is_done=False))
        db.session.commit()

    @classmethod
    def delete_task(cls, task_id: int):
        task = db.get_or_404(cls, task_id)
        task.delete_at = func.now()
        db.session.commit()

    @classmethod
    def get_task_list(cls):
        return db.session.execute(
            db.select(cls).where(cls.delete_at.is_(None)).order_by(cls.id)
        ).scalars()

    @classmethod
    def get_task(cls, task_id: int):
        return db.session.execute(
            db.select(cls).where(cls.delete_at.is_(None), cls.id == task_id)
        ).scalar()

    @classmethod
    def update_task(cls, description: str, task_id: int):
        task = db.get_or_404(cls, task_id)
        task.description = description
        task.update_at = func.now()
        db.session.commit()

    @classmethod
    def change_done(cls, task_id: int):
        task = db.get_or_404(cls, task_id)
        is_done = task.is_done
        task.is_done = False if is_done else True
        task.change_done_at = func.now()
        db.session.commit()

    @classmethod
    def call_date_delete(cls, task_id: int):
        return db.get_or_404(cls, task_id).delete_at
