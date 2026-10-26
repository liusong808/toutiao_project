from datetime import datetime
from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy import DateTime, func, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

# 连接数据库URL地址
ASYNC_DATABASE_URL = "mysql+aiomysql://root:liusong123@localhost:3306/news_app?charset=utf8"


# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # 可选, 输出SQL日志
    pool_size = 10,  # 设置连接池活跃的连接数
    max_overflow = 20  # 允许额外的连接数
)


# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, # 绑定数据库引擎
    class_=AsyncSession, # 指定会话类
    expire_on_commit=False, # 提交后会话不过期, 不会重新查询数据
)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session # 返回数据库会话给路由处理函数
            await session.commit() # 提交事务
        except Exception:
            await session.rollback() # 有异常, 回滚
            raise
        finally:
            await session.close() # 关闭会话
















