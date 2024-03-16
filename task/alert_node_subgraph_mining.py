import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from task.model_repo.subgraph_mining.subgraph_mining import subgraph_mining
from task.taskBasic import taskBasic 


class alert_node_subgraph_mining(taskBasic):
    def __init__(self, **input):
        super().__init__(**input)
        self.input = input
        self.table = input.get("table", "neo4j")
        self.node_type = input.get("node_type", "alert_info")
        self.node_id = input.get("node_id", 0)
        self.edge_type = input.get("edge_type", "alert_edge")
        self.directed = input.get("directed", "undirected")
        self.if_all = input.get("if_all", False)

    @taskBasic.udf
    def run(self):
        # run函数包含error检测
        # @taskBasic.udf主要用于没有包含错误检测的其他方法
        try:
            result = subgraph_mining(**input)
        except ValueError as e:
            self.logger.error(f"VularError occurred in run: {e}")
            return False, e
        except Exception as e:
            self.logger.error(f"Error occurred in run: {e}")
            return False, e
        else:
            return True, result