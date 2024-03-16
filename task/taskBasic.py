from neo4j import GraphDatabase
from functools import reduce, wraps
from task.utils import mkdir
import time
import datetime
import torch
import logging
import os

# Neo4j数据库的连接信息
URL = "neo4j://120.55.15.198:7687"
USERNAME = "neo4j"
PASSWORD = "Zju302Ch"
# tablename = "neo4j" # 数据库名


class taskBasic(object):
    def __init__(self, task, **input) -> None:
        """
        维护一些基础设置,包括：数据库的连接信息,资源占用情况(CPU,GPU)
        """

        # 登录信息
        self.loginInfo = {"URL": URL, "USERNAME": USERNAME, "PASSWORD":PASSWORD}

        self.task = task
        self.logger = self.logging_init(self.task)

        # 资源配置
        self.gpu = torch.cuda.is_available()
        self.device = torch.device("cuda")

        # 返回状态
        self.status = True

    def logging_init(self, task):
        path = mkdir("log/" + task)[0]
        logging.basicConfig(
            filename='log.txt',
            level=logging.DEBUG, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        log_handler = logging.FileHandler(path + "/" + task + "_log.txt")
        log_handler.setLevel(logging.INFO)

        logger = logging.getLogger(__name__)
        logger.addHandler(log_handler)
        logger.setLevel('DEBUG')

        return logger


    def udf(func):
        """global decorator for every method

        Before execute the method, check status and do some logging
        After execute the method, update status and do some logging
        Args:
            func ([type]): [description]

        Returns:
            [type]: [description]
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                start = time.time()
                self.logger.info(f"Start:{func.__name__}")
                self.logger.info(f"[{datetime.datetime.now()}][{self.task}]: {func.__name__}\n")
                func(self, *args, **kwargs)
            except Exception as e:
                self.logger.error(f"Failed:{e}")
                # self.error_info += f"{e}"
                return False
            else:
                end = time.time()
                self.logger.info(f"End:{func.__name__}. Time cost:{end-start}")
                return False

        return wrapper