# OpenRichpedia × Neo4j 知识图谱可视化课程项目

> 知识图谱课程作业：从 OpenKG / OpenRichpedia 公开数据中抽取实体与关系，完成数据预处理、Neo4j 图数据库导入、Cypher 查询和图谱可视化，并形成可复现实验报告。

## 1. 项目目标

本仓库不是复制 OpenRichpedia 原网站，而是把其中适合作为课程实验的结构化数据转换成 Neo4j 图模型。最终得到三类主要知识：

- 城市与景点：`(City)-[:HAS_SIGHT]->(Sight)`
- 人物/地点与图片：`(Entity)-[:HAS_IMAGE]->(Image)`
- 图片实体之间的包含关系：`(Image)-[:CONTAINS]->(Image)`

知识图谱统一表示为：

$$
G=(V,E)
$$

其中节点集合为：

$$
V=V_{city}\cup V_{sight}\cup V_{place}\cup V_{person}\cup V_{image}
$$

关系集合为：

$$
E=E_{has\_sight}\cup E_{has\_image}\cup E_{contains}
$$

## 2. 数据来源与可追溯性

- 上游仓库：<https://github.com/OpenKG-ORG/OpenRichpedia>
- 本项目固定上游提交：`0ded4b2c9414160b5b39914d43e42168e4d0762c`
- 上游许可：Creative Commons Attribution 4.0 International（CC BY 4.0）
- 实际使用文件：
  - `data_src/city_sight/city.js`
  - `data_src/city_sight/city_sight.js`
  - `data_src/city_sight/pic_city.js`
  - `data_src/city_sight/contain.js`
  - `data_src/people/people.js`
  - `data_src/people/pic_people.js`

固定提交可以保证同学、老师或未来的自己运行时得到相同输入版本。

## 3. 仓库结构

```text
.
├── README.md
├── pyproject.toml
├── requirements.txt
├── scripts/
│   ├── fetch_openrichpedia.py     # 下载固定版本原始数据
│   ├── preprocess.py              # 解析、清洗、去重、建图并导出 CSV
│   ├── validate_processed.py      # 验证导出结果
│   └── import_neo4j.py            # Python Driver 批量导入 Neo4j
├── src/openrichpedia_kg/
│   ├── model.py
│   ├── parsers.py
│   ├── graph.py
│   ├── io.py
│   └── neo4j_import.py
├── cypher/
│   ├── 01_constraints.cypher
│   ├── 02_load_csv.cypher         # 课堂友好的手工 LOAD CSV 方案
│   └── 03_queries.cypher          # 查询与可视化示例
├── data/
│   ├── raw/                       # 正式原始数据（运行下载脚本生成）
│   ├── processed/                 # 正式预处理结果（运行预处理脚本生成）
│   └── demo/                      # 仓库自带的小型验证结果
├── tests/
│   └── fixtures/                  # 小型离线测试数据
└── docs/
    ├── 01-数据集与任务分析.md
    ├── 02-环境安装与完整运行步骤.md
    ├── 03-图模型与数据预处理.md
    ├── 04-Neo4j导入查询与可视化.md
    ├── 05-实验报告与答辩指南.md
    ├── 实验报告.md
    └── 提交前检查清单.md
```

## 4. 最短复现路径

### 4.1 创建 Python 环境

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e ".[dev]"
```

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e ".[dev]"
```

要求 Python `>=3.10`。

### 4.2 下载 OpenRichpedia 数据

```bash
python scripts/fetch_openrichpedia.py
```

下载完成后 `data/raw/` 应有 6 个文件。

### 4.3 预处理并导出 Neo4j CSV

```bash
python scripts/preprocess.py
```

生成：

```text
data/processed/nodes.csv
data/processed/relationships.csv
data/processed/stats.json
```

### 4.4 做独立数据验证

```bash
python scripts/validate_processed.py
```

期望看到：

```text
验证通过：... 个节点，... 条关系。
```

### 4.5 启动 Neo4j

课程作业推荐使用 **Neo4j Desktop + Neo4j 5.26 LTS**。创建本地 DBMS 后记住密码，启动数据库。

### 4.6 导入数据库

推荐自动导入：

Windows PowerShell：

```powershell
$env:NEO4J_URI="neo4j://localhost:7687"
$env:NEO4J_USER="neo4j"
$env:NEO4J_PASSWORD="你的密码"
python scripts/import_neo4j.py
```

macOS / Linux：

```bash
export NEO4J_URI=neo4j://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD='你的密码'
python scripts/import_neo4j.py
```

如果老师希望你展示 `LOAD CSV`，按 `docs/04-Neo4j导入查询与可视化.md` 使用 `cypher/02_load_csv.cypher`。

### 4.7 查询与截图

打开 Neo4j Browser / Query，依次执行：

```cypher
MATCH p=(c:City {name:'Beijing'})-[:HAS_SIGHT]->(s:Sight)
RETURN p;
```

```cypher
MATCH p=(person:Person)-[:HAS_IMAGE]->(img:Image)
RETURN p LIMIT 50;
```

```cypher
MATCH p=(a:Image)-[:CONTAINS]->(b:Image)
RETURN p LIMIT 50;
```

更多查询见 `cypher/03_queries.cypher`。

## 5. 推荐报告截图

至少保存以下 5 张：数据库运行状态、节点/关系统计、北京—景点子图、人物—图片子图、图片 `CONTAINS` 子图。详细截图位置与图注见 `docs/04-Neo4j导入查询与可视化.md`。

## 6. 测试

```bash
pytest -q
```

本仓库的测试覆盖：源格式解析、ID 规范化、节点类型合并、关系生成、悬空边检查、CSV 输出以及 Neo4j 动态标签/关系类型白名单。

## 7. 离线 Demo

如果当前网络无法访问 GitHub，仍可验证预处理全链路：

```bash
python scripts/preprocess.py --raw-dir tests/fixtures --output-dir data/demo
python scripts/validate_processed.py --processed-dir data/demo
```

仓库内置 demo 当前应得到 11 个节点和 6 条关系。**该数字仅用于验证代码，不是正式实验数据规模。**正式报告必须使用 `data/processed/stats.json` 中完整数据的统计结果。

## 8. 文档入口

第一次做数据库作业，建议按顺序阅读：

1. `docs/01-数据集与任务分析.md`
2. `docs/02-环境安装与完整运行步骤.md`
3. `docs/03-图模型与数据预处理.md`
4. `docs/04-Neo4j导入查询与可视化.md`
5. `docs/实验报告.md`
6. `docs/05-实验报告与答辩指南.md`
