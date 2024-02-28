from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# データベースの接続URLを設定
# 例: SQLiteの場合
DATABASE_URL = "postgresql://miyaharaiam:1234@localhost/react_fastapi_portfolio"

# 例: PostgreSQLの場合
# DATABASE_URL = "postgresql://user:password@localhost/dbname"

# SQLAlchemyエンジンを作成
engine = create_engine(DATABASE_URL)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラスの生成
Base = declarative_base()
