from model.base import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)


__all__ = ["Announcement", ]


class Announcement(Base):
    __tablename__ = "announcement"

    announcementid = Column(Integer, primary_key=True, autoincrement=True)
    courseid = Column(Integer, ForeignKey("course.courseid"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    # auth
    is_show = Column(Boolean, nullable=False, server_default="true")

    # time information
    announce_date = Column(DateTime, nullable=True)


    def to_dict(self):
        return {
            "announcementid": self.announcementid,
            "courseid": self.courseid,
            "title": self.title,
            "content": self.content,
            "is_show": self.is_show,
            "announce_date": self.announce_date
        }
