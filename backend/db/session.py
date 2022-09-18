# -*- coding: utf-8 -*-

from asyncio import current_task
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from backend.core.conf import setting


# 创建表引擎
engine = create_async_engine(
    url=setting.DATABASE_URI,  # 数据库uri
    echo=setting.DATABASE_ECHO,  # 是否打印日志
    future=True,
    isolation_level='READ_UNCOMMITTED'
    # pool_size=10,  # 队列池个数
    # max_overflow=20,  # 队列池最大溢出个数
)

metadata = MetaData(engine)

# 操作表会话
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False  # 防止提交后属性过期
)

async_session = async_scoped_session(async_session_factory, scopefunc=current_task)