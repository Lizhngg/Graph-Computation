import bentoml
import importlib


@bentoml.service(
    traffic={"timeout": 300},
    workers=1,)
class graphComputation:
    def __init__(self) -> None:
        """
        初始化，引入必要的库，定义变量
        """
        from neo4j import GraphDatabase

    @bentoml.api
    def alert_subgraph_mining(
            self,
            task: str = "new_task",
            model: str = "alert_node_subgraph_mining",
            path: str = "alert_node_subgraph_mining",
            input_params: dict = {  
                "table": "neo4j",
                "node_type": "alert_information_id",
                "node_id": 5,
                "edge_type": "alert_service_edge",
                "directed": "undirected"
                },
            response = "default"
    ) -> str:
        """
        在servicer被post访问时会解析请求body中的json文件,
        并将文件中的内容以参数形式输入对应被@bentoml.api修饰的方法.
        see https://docs.bentoml.org/en/latest/reference/sdk.html#service-decorator
        """
        ## 这里也可以直接import，取决于是否需要为不同task创建不同url，不需要则直接把task作为参数输入
        # 输入路径
        task_path = 'task.{:s}'.format(path)
        # 调用类
        mod = importlib.import_module(task_path)
        task_class = getattr(mod, model)
        #实例化
        mining_svc = task_class(**input_params)
        # run
        response = mining_svc.run()

        return response
