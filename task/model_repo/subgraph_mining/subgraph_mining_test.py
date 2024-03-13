from neo4j import GraphDatabase

# Neo4j数据库的连接信息
URL = "neo4j://120.55.15.198:7687"
USERNAME = "neo4j"
PASSWORD = "Zju302Ch"


# 创建Neo4j数据库连接驱动程序
def main():
    
    # 创建Neo4j数据库连接驱动程序
    with GraphDatabase.driver(URL, auth=(USERNAME, PASSWORD)) as driver:
        with driver.session(database="neo4j") as session:

            test_preparation(session)

            result = process_graph(session)


def process_graph(session):
    # 遍历每个节点，获取节点ID 并处理3跳子图
    nodes = session.execute_read(query_name_get_nodes_tx, node_name="TestNodes")

    delete_nodes(session)

    for record in nodes:
        node_id = record["id"]
        print(f"node id: {node_id}")
        result = session.execute_write(mining_3_hop_subgraph_tx, node_id, edge_name="before")
        print(f"node: {node_id}, linked with {result} \n")

def delete_nodes(session):
    delete_edge = ("""
            MATCH ()-[r:alert_service_Edge]-()
            DELETE r;
    """)
    session.run(delete_edge)

    delete_node = ("""
        MATCH (alertnodes:AlertNodes)
        DETACH DELETE alertnodes
        """
    )
    # delete_node = ("""
    #     MATCH (node)
    #     WHERE NOT ()--(node) AND NOT (node)--()
    #     DELETE node;
    #     """
    # )
    session.run(delete_node)


def query_name_get_nodes_tx(tx, node_name):
    target_id = tx.run(f"""
    MATCH (node:{node_name}) 
    RETURN node.id AS id
    """
    )
    return list(target_id)

def mining_3_hop_subgraph_tx(tx, node_id, edge_name):
    # 获取指定节点的3跳子图节点ID
    # MATCH path = (start)-[*1..3]-(end) 表示从start出发3跳之内与end相连
    # MATCH path = (start)-[*1..3]->(end) 表示从start出发3跳之内到end节点（有向关系）
    neighbor = tx.run("""
        MERGE (alertnodes:AlertNodes {alert_id: $node_id})
        WITH alertnodes
        MATCH path = (start)-[*1..3]->(end)
        WHERE start.id = $node_id AND all(r IN relationships(path) WHERE TYPE(r) = $edge_name)
        WITH collect(end) AS neighbor_list, end, alertnodes
        FOREACH (n IN neighbor_list | 
                MERGE (alertnodes)-[r:alert_service_Edge]->(n))
        RETURN collect(end.id) AS neighbor
        """, node_id = node_id,  edge_name = edge_name
    )
    return list(neighbor)
            

def test_preparation(session):
    num = 10
    node_name = "TestNodes"
    edge_name = "before"
    # 创建10个 Test Nodes
    for i in range(num):
        node_id = i
        result = session.execute_write(add_testnode_tx, node_id)

    # 按顺序连接这10个 Test Nodes 1 -> 2 -> 3 -> 4 -> ...
    session.execute_write(add_edge_tx, num)


def add_testnode_tx(tx, node_id):
    # Create new test node with given id, if not exists already
    result = tx.run("""
        MERGE (p:TestNodes {id: $id})
        RETURN p.id AS id
        """, id=node_id
    )

    return result

def add_edge_tx(tx, num):
    # Create new test edge with given id, if not exists already
    result = tx.run("""
        MATCH (node1:TestNodes), (node2:TestNodes)
        WHERE  node1.id < $num AND node2.id < $num AND node1.id + 1 = node2.id
        MERGE (node1)-[r:before]->(node2)
        """, num=num
        )

main()