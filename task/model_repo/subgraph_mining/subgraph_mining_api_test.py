from neo4j import GraphDatabase
from subgraph_mining import subgraph_mining

# Neo4j数据库的连接信息
URL = "neo4j://120.55.15.198:7687"
USERNAME = "neo4j"
PASSWORD = "Zju302Ch"



TABLE = "neo4j"
node_type = "TestNodes"
edge_type = "service_service_Edge"
node_id = 5
def main():
    # 创建Neo4j数据库连接驱动程序
    with GraphDatabase.driver(URL, auth=(USERNAME, PASSWORD)) as driver:
        with driver.session(database=TABLE) as session:

            delete_nodes(session)

            test_preparation(session)


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
    session.run(delete_node)
    
    delete_edge = ("""
            MATCH ()-[r:service_service_Edge]-()
            DELETE r;
    """)
    session.run(delete_edge)

    delete_node = ("""
        MATCH (alertnodes:TestNodes)
        DETACH DELETE alertnodes
        """
    )
    session.run(delete_node)

def test_preparation(session):
    num = 10
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
    result = tx.run(f"""
        MATCH (node1:TestNodes), (node2:TestNodes)
        WHERE  node1.id < {num} AND node2.id < {num} AND node1.id + 1 = node2.id
        MERGE (node1)-[r:{edge_type}]->(node2)
        """
        )

main()