// 1. 数据规模验证
MATCH (n) RETURN count(n) AS node_count;
MATCH ()-[r]->() RETURN count(r) AS relationship_count;

// 2. 各类节点数量
MATCH (n:Entity)
RETURN n.kind AS kind, count(*) AS count
ORDER BY count DESC;

// 3. 各类关系数量
MATCH ()-[r]->()
RETURN type(r) AS relationship_type, count(*) AS count
ORDER BY count DESC;

// 4. 北京及其景点：适合作为报告核心截图
MATCH p=(c:City {name:'Beijing'})-[:HAS_SIGHT]->(s:Sight)
RETURN p;

// 5. 一个地点及其图片实体
MATCH p=(e:Entity)-[:HAS_IMAGE]->(img:Image)
RETURN p LIMIT 50;

// 6. 一个人物及其图片实体
MATCH p=(person:Person)-[:HAS_IMAGE]->(img:Image)
RETURN p LIMIT 50;

// 7. 图像之间的包含关系
MATCH p=(a:Image)-[:CONTAINS]->(b:Image)
RETURN p LIMIT 50;

// 8. 度数最高的实体
MATCH (n:Entity)-[r]-()
RETURN n.id AS id, n.name AS name, n.kind AS kind, count(r) AS degree
ORDER BY degree DESC
LIMIT 10;

// 9. 北京两跳邻域（若 HAS_IMAGE 数据中包含北京）
MATCH p=(c:Entity {name:'Beijing'})-[*1..2]-(x)
RETURN p LIMIT 100;
