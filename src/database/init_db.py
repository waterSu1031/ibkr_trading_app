# from .session import Base, engine
from src.database.session import Base, engine


def init():
    Base.metadata.create_all(bind=engine)
    print("✅ DB 테이블이 성공적으로 생성되었습니다.")


if __name__ == "__main__":
    init()
