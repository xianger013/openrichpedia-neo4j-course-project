// 手工教学版导入脚本。
// 先把 data/processed/nodes.csv 和 relationships.csv 复制到 Neo4j 的 import 目录。

LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
MERGE (n:Entity {id: row.id})
SET n.name = row.name, n.kind = row.kind, n.source_file = row.source_file;

LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.kind = 'City'
MATCH (n:Entity {id: row.id}) SET n:City;
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.kind = 'Sight'
MATCH (n:Entity {id: row.id}) SET n:Sight;
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.kind = 'Place'
MATCH (n:Entity {id: row.id}) SET n:Place;
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.kind = 'Person'
MATCH (n:Entity {id: row.id}) SET n:Person;
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.kind = 'Image'
MATCH (n:Entity {id: row.id}) SET n:Image;

LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
WITH row WHERE row.type = 'HAS_SIGHT'
MATCH (s:Entity {id: row.source_id}), (t:Entity {id: row.target_id})
MERGE (s)-[:HAS_SIGHT]->(t);

LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
WITH row WHERE row.type = 'HAS_IMAGE'
MATCH (s:Entity {id: row.source_id}), (t:Entity {id: row.target_id})
MERGE (s)-[:HAS_IMAGE]->(t);

LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
WITH row WHERE row.type = 'CONTAINS'
MATCH (s:Entity {id: row.source_id}), (t:Entity {id: row.target_id})
MERGE (s)-[:CONTAINS]->(t);
