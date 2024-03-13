from model_repo.subgraph_mining.subgraph_mining import subgraph_mining
from taskBasic import taskBasic 


class alert_node_subgraph_mining(taskBasic):
    def __init__(self, **input):
        super().__init__(**input)
        self.table = self.params.get("table", "neo4j")
        self.node_type = self.params.get("node_type", "alert_info")
        self.node_id = self.params.get("node_id", 0)
        self.edge_type = self.params.get("edge_type", "alert_edge")
        self.directed = self.params.get("directed", "undirected")
        self.if_all = self.params.get("if_all", False)

    def run(self):
        result = subgraph_mining(table=self.table, node_type=self.node_type, edge_type=self.edge_type, 
                                 node_id=self.node_id, directed=self.directed, if_all=self.if_all)
        return result