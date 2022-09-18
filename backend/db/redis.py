# redis 链接
import json
from typing import Union
from aioredis import Redis
from backend.core.conf import setting

class MyRedis(Redis):
    """ 继承Redis,并添加自己的方法 """
    async def list_loads(self, key: str, num: int = -1) -> list:
        """
        将列表字符串转为对象

        :param key: 列表的key
        :param num: 最大长度(默认值 0-全部)
        :return: 列表对象
        """
        todo_list = await self.lrange(key, 0, (num - 1) if num > -1 else num)
        return [json.loads(todo) for todo in todo_list]

    async def cus_lpush(self, key: str, value: Union[str, list, dict]):
        """
        向列表右侧插入数据

        :param key: 列表的key
        :param value: 插入的值
        """
        text = json.dumps(value)
        await self.lpush(key, text)

    async def get_list_by_index(self, key: str, id: int) -> object:
        """
        根据索引得到列表值

        :param key: 列表的值
        :param id: 索引值
        :return:
        """
        value = await self.lindex(key, id)
        return json.loads(value)


# 参考: https://github.com/grillazz/fastapi-redis/tree/main/app
async def init_redis_pool() -> MyRedis:
    """ 连接redis """
    redis = await MyRedis.from_url(url=setting.REDIS_URI, encoding=setting.GLOBAL_ENCODING, decode_responses=True)
    return redis