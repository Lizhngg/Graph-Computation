from neo4j import GraphDatabase

# Neo4j数据库的连接信息
URL = "neo4j://120.55.15.198:7687"
USERNAME = "neo4j"
PASSWORD = "Zju302Ch"
# tablename = "neo4j" # 数据库名


# 创建Neo4j数据库连接驱动程序
def subgraph_mining(table="neo4j", 
                    mining_task="service", 
                    node_type="alert_info", 
                    source_node_id=0,
                    target_node_id=1,
                    edge_type="alert_edge", 
                    directed = "undirected", 
                    if_all=False):
    
    # 创建Neo4j数据库连接驱动程序
    with GraphDatabase.driver(URL, auth=(USERNAME, PASSWORD)) as driver:
        with driver.session(database=table) as session:

            if mining_task == "service":

                if if_all == False:
                    nodes = session.execute_read(query_name_get_nodes_tx, node_type=node_type)
                    nodes_ids = [record["id"] for record in nodes]
                    if source_node_id in nodes_ids:
                        result = session.execute_write(mining_3_hop_subgraph_service_tx, 
                                                       node_type=node_type, 
                                                       node_id=source_node_id, 
                                                       edge_type=edge_type, 
                                                       directed=directed)
                        response = f"node: {source_node_id}, linked with {result}"
                    else:
                        raise ValueError(f"node not exist(node id: {source_node_id})!")
                        # result = f"node not exist(node id: {source_node_id})! \n"
                else:
                    # 获取所需节点
                    nodes = session.execute_read(query_name_get_nodes_tx, node_type=node_type)

                    for record in nodes:
                        node_id = record["id"]
                        # print(f"node id : {node_id}")
                        result = session.execute_write(mining_3_hop_subgraph_service_tx, 
                                                       node_type=node_type, 
                                                       node_id= node_id, 
                                                       edge_type=edge_type, 
                                                       directed=directed)
                    response = "Success!"
            
            elif mining_task == "event":
                if source_node_id == target_node_id:
                    raise ValueError(f"event not exist between nodes with same id!")
                nodes = session.execute_read(query_name_get_nodes_tx, node_type=node_type)
                nodes_ids = [record["id"] for record in nodes]
                if source_node_id in nodes_ids and target_node_id in nodes_ids:
                    result = session.execute_write(mining_3_hop_subgraph_event_tx, 
                                                   node_type=node_type, 
                                                   source_node_id=source_node_id, 
                                                   target_node_id=target_node_id,
                                                   edge_type=edge_type, 
                                                   directed=directed)
                    response = f"event: {source_node_id}-{target_node_id}, subgraph: {result}"
                else:
                    raise ValueError(f"event not exist(node id: {source_node_id}-{target_node_id})!")
                    # response = f"event not exist(node id: {source_node_id}-{target_node_id})! \n"

    return response

def query_name_get_nodes_tx(tx, node_type):
    target_id = tx.run(f"""
    MATCH (node:{node_type}) 
    RETURN node.id AS id
    """
    )
    return list(target_id)

def mining_3_hop_subgraph_service_tx(tx, node_type, node_id, edge_type, directed):
    # 获取指定节点的3跳子图节点ID
    # MATCH path = (start)-[*1..3]-(end) 表示从start出发3跳之内与end相连
    # MATCH path = (start)-[*1..3]->(end) 表示从start出发3跳之内到end节点（有向关系）

    edge_dir_mapping = {"in": "<-", "out": "->", "undirected": "-"}
    edge_dir = edge_dir_mapping.get(directed)
    if edge_dir is None:
        # 抛出异常
        raise ValueError("Invalid value for directed: {}".format(directed))

    neighbor = tx.run(f"""
        MERGE (alertnodes:AlertNodes {{ alert_id: {node_id} }})
        WITH alertnodes
        MATCH path = (start:{node_type} {{ id: {node_id} }})-[*1..3]{edge_dir}(end:{node_type})
        WHERE all(r IN relationships(path) WHERE TYPE(r) = '{edge_type}')
        WITH collect(end) AS neighbor_list, start, end, alertnodes
        FOREACH (n IN neighbor_list | 
                MERGE (alertnodes)-[r:alert_service_Edge]->(n))
        WITH start, end, alertnodes
        MERGE (alertnodes)-[r:alert_service_Edge]->(start)
        RETURN start.id AS core, collect(end.id) AS neighbor
        """)
    return list(neighbor)


def mining_3_hop_subgraph_event_tx(tx, node_type, source_node_id, target_node_id, edge_type, directed):
    # 获取指定节点的3跳子图节点ID
    # MATCH path = (start)-[*1..3]-(end) 表示从start出发3跳之内与end相连
    # MATCH path = (start)-[*1..3]->(end) 表示从start出发3跳之内到end节点（有向关系）

    edge_dir_mapping = {"in": "<-", "out": "->", "undirected": "-"}
    edge_dir = edge_dir_mapping.get(directed)
    if edge_dir is None:
        # 抛出异常
        raise ValueError("Invalid value for directed: {}".format(directed))

    neighbor = tx.run(f"""
        MERGE (alertnodes:AlertNodes {{ alert_id: {source_node_id} }})
        WITH alertnodes
        MATCH path = (start:{node_type})-[*1..3]{edge_dir}(end:{node_type})
        WHERE start.id in [{source_node_id},{target_node_id}]
        AND all(r IN relationships(path) WHERE TYPE(r) = '{edge_type}')
        WITH collect(end) AS neighbor_list, start, end, alertnodes
        FOREACH (n IN neighbor_list | 
                MERGE (alertnodes)-[r:alert_service_Edge]->(n))
        WITH start, end, alertnodes
        MERGE (alertnodes)-[r:alert_service_Edge]->(start)
        RETURN start.id AS core, collect(end.id) AS neighbor
        """)
    return list(neighbor)