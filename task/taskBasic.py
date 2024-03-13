from neo4j import GraphDatabase
import torch

# Neo4j数据库的连接信息
URL = "neo4j://120.55.15.198:7687"
USERNAME = "neo4j"
PASSWORD = "Zju302Ch"
# tablename = "neo4j" # 数据库名


class taskBasic(object):
    def __init__(self, **input) -> None:
        """
        维护一些基础设置,包括：数据库的连接信息,资源占用情况(CPU,GPU)
        """

        # 登录信息
        self.loginInfo = {"URL": URL, "USERNAME": USERNAME, "PASSWORD":PASSWORD}

        # 参数设置
        self.task = input.get("task", "new task")
        self.model = input.get("model", "graph model")
        self.path = input.get("path", "")
        self.params = input.get("params", {})
        self.response = input.get("response", "default")

        # 资源配置
        self.gpu = torch.cuda.is_available()
        self.device = torch.device("cuda")