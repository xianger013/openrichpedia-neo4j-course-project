# 4. Neo4j 导入、查询与可视化

## 4.1 两种导入方式

### 方式 A：Python Driver（推荐实际运行）

```bash
python scripts/import_neo4j.py
```

优点：不需要寻找 Neo4j 的 `import` 目录，最容易一次成功。

### 方式 B：LOAD CSV（推荐课堂讲解）

如果老师希望看数据库语句：

1. 将 `nodes.csv`、`relationships.csv` 复制到当前 Neo4j DBMS 的 `import` 目录；
2. 在 Query 中执行 `cypher/01_constraints.cypher`；
3. 执行 `cypher/02_load_csv.cypher`。

## 4.2 唯一约束

```cypher
CREATE CONSTRAINT entity_id_unique IF NOT EXISTS
FOR (n:Entity) REQUIRE n.id IS UNIQUE;
```

它表达：每个知识实体以 `id` 唯一识别，重复导入时 `MERGE` 不会无限复制同一节点。

## 4.3 第一组：规模验证

```cypher
MATCH (n)
RETURN count(n) AS node_count;
```

```cypher
MATCH ()-[r]->()
RETURN count(r) AS relationship_count;
```

**截图 1：** 将两个统计结果与 `stats.json` 对照，报告中说明导入前后规模一致。

## 4.4 第二组：节点/关系分布

```cypher
MATCH (n:Entity)
RETURN n.kind AS kind, count(*) AS count
ORDER BY count DESC;
```

```cypher
MATCH ()-[r]->()
RETURN type(r) AS relationship_type, count(*) AS count
ORDER BY count DESC;
```

**截图 2：** 表格视图即可。它能证明你不是只看到了“几个圆点”，而是检查了图谱整体结构。

## 4.5 第三组：北京与景点

```cypher
MATCH p=(c:City {name:'Beijing'})-[:HAS_SIGHT]->(s:Sight)
RETURN p;
```

切换到 Graph 视图。

**截图 3（最重要）：** 以 Beijing 为中心展示 `HAS_SIGHT` 边。

建议图注：

> 图 X 展示了 Beijing 城市实体与其景点实体之间的 `HAS_SIGHT` 关系。城市节点作为中心节点，通过有向边连接多个景点，体现了图数据库对层级型知识关系的直观表达能力。

## 4.6 第四组：人物与图片

```cypher
MATCH p=(person:Person)-[:HAS_IMAGE]->(img:Image)
RETURN p LIMIT 50;
```

**截图 4：** 体现 Richpedia 的“多模态”特色：文本人物实体与视觉实体并不是两个独立数据表，而是通过关系直接连接。

## 4.7 第五组：图片关系

```cypher
MATCH p=(a:Image)-[:CONTAINS]->(b:Image)
RETURN p LIMIT 50;
```

**截图 5：** 展示图片资源之间的关系。

## 4.8 第六组：寻找度数最大的实体

```cypher
MATCH (n:Entity)-[r]-()
RETURN n.id AS id, n.name AS name, n.kind AS kind, count(r) AS degree
ORDER BY degree DESC
LIMIT 10;
```

定义节点度：

$$
d(v)=|N(v)|$$

其中 $N(v)$ 表示与节点 $v$ 相邻的节点集合。该查询可以帮助观察哪些实体处于图谱的连接中心。

## 4.9 可选：两跳邻域

```cypher
MATCH p=(c:Entity {name:'Beijing'})-[*1..2]-(x)
RETURN p LIMIT 100;
```

它展示：从一个实体出发，不仅能找直接邻居，还能沿关系继续寻找更远的关联知识。

## 4.10 Neo4j 图视图美化建议

在 Browser / Query 图视图中：

- 节点 Caption 设为 `name`；
- 不同标签使用默认不同颜色即可；
- 单次查询限制在 30–100 条路径，避免画面过密；
- 截图前把最重要节点拖到中央；
- 保留关系名称；
- 报告中不要只放图，要在图下写 2–4 句解释。

不要人为伪造截图。最终截图必须来自你本机真实 Neo4j 查询结果。
