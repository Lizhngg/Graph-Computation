import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from task.model_repo.subgraph_mining.subgraph_mining import subgraph_mining
from task.taskBasic import taskBasic 


class alert_node_subgraph_mining(taskBasic):
    def __init__(self, **input):
        super().__init__(**input)
        self.table = input.get("table", "neo4j")
        self.node_type = input.get("node_type", "alert_info")
        self.node_id = input.get("node_id", 0)
        self.edge_type = input.get("edge_type", "alert_edge")
        self.directed = input.get("directed", "undirected")
        self.if_all = input.get("if_all", False)

    def run(self):
        response = subgraph_mining(table=self.table, node_type=self.node_type, edge_type=self.edge_type, 
                                 node_id=self.node_id, directed=self.directed, if_all=self.if_all)
        return response