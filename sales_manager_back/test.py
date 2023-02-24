if __name__ == '__main__':
    from admin.models import User
    from config import DevelopmentConfig
    from sqlalchemy.orm import sessionmaker, scoped_session
    from sqlalchemy import create_engine

    sett = DevelopmentConfig()
    engine = create_engine(sett.DATABASE_URI, echo=True, pool_pre_ping=True)
    select_db = sessionmaker(engine)
    db_session = scoped_session(select_db)
    newObj = User({"name": "Emily Li", "password": "123456", "status": 1})
    db_session.add(newObj)
    db_session.commit()
