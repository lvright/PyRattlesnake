# -*- coding: utf-8 -*-

import create
import os
from config import Config


if __name__ == '__main__':

    os.system('figlet -f slant PyRattlesnake')

    import uvicorn

    # TODO 启动 uvicorn FastApi

    uvicorn.run(
        app=create.app,
        host=Config.url,
        port=Config.port,
        workers=Config.workers
    )