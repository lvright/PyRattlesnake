# -*- coding: utf-8 -*-

from utils.logger import logger
from backend.db import engine
from .data import (
    accountData, routerData, menuRelationData,
    roleData, roleRelationData, settingData,
    configData, extendData, deptData, postData,
    deptRelationData, postRelationData, dictTypeData,
    dictData
)
from backend.models import (
    Base, Admin, Api, App, ApiGroup,
    AppGroup, Attachment, Config, UserDept,
    Dict, DictType, Extend, LoginLog,
    UserMenu, MenuRelation, Message, Notification,
    OperLog, Post, Role, Setting, RoleRelation,
    DeptRelation, PostRelation
)


async def init_db():
    """ 创建 models/__init__ 下的所有表 """
    try:
        await drop_db()  # 删除所有的表
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("创建表成功!!!")
    except Exception as e:
        logger.error(f"创建表失败!!! -- 错误信息如下:\n{e}")
    finally:
        await engine.dispose()


async def drop_db():
    """ 删除 models/__init__ 下的所有表 """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.info("删除表成功!!!")
    except Exception as e:
        logger.error(f"删除表失败!!! -- 错误信息如下:\n{e}")
    finally:
        await engine.dispose()


async def init_data():
    """ 初始化表数据 """
    try:
        async with engine.begin() as conn:
            await conn.execute(Admin.__table__.insert(), [account for account in accountData])
            await conn.execute(UserMenu.__table__.insert(), [router for router in routerData])
            await conn.execute(MenuRelation.__table__.insert(), [relation for relation in menuRelationData])
            await conn.execute(Role.__table__.insert(), [role for role in roleData])
            await conn.execute(Post.__table__.insert(), [post for post in postData])
            await conn.execute(RoleRelation.__table__.insert(), [relation for relation in roleRelationData])
            await conn.execute(Setting.__table__.insert(), [setting for setting in settingData])
            await conn.execute(Config.__table__.insert(), [config for config in configData])
            await conn.execute(Extend.__table__.insert(), [extend for extend in extendData])
            await conn.execute(UserDept.__table__.insert(), [dept for dept in deptData])
            await conn.execute(DeptRelation.__table__.insert(), [relation for relation in deptRelationData])
            await conn.execute(PostRelation.__table__.insert(), [relation for relation in postRelationData])
            await conn.execute(DictType.__table__.insert(), [type for type in dictTypeData])
            await conn.execute(Dict.__table__.insert(), [dict for dict in dictData])
            logger.info(f"成功初始化表数据!!!")
    except Exception as e:
        logger.error(f"初始化表数据失败!!! -- 错误信息如下:\n{e}")
    finally:
        await engine.dispose()
