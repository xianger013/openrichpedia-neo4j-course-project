# OpenRichpedia Neo4j 课程项目设计

## 1. 目标

基于 OpenKG-ORG/OpenRichpedia 仓库中公开的多模态知识图谱数据，构建一个适合知识图谱课程作业的 Neo4j 可视化项目。项目必须做到：原始数据可追溯、预处理可复现、Neo4j 可导入、Cypher 查询可演示、实验报告可直接据此完成。

## 2. 数据来源

上游仓库：`OpenKG-ORG/OpenRichpedia`

固定数据版本：`0ded4b2c9414160b5b39914d43e42168e4d0762c`

使用文件：

- `data_src/city_sight/city.js`：城市及其景点层级。
- `data_src/city_sight/city_sight.js`：Wikidata 风格地点实体名称。
- `data_src/city_sight/pic_city.js`：地点实体与图片实体映射。
- `data_src/city_sight/contain.js`：图片实体之间的 contain 关系。
- `data_src/people/people.js`：人物实体。
- `data_src/people/pic_people.js`：人物实体与图片实体映射。

上游 README 声明 Richpedia 为多模态知识图谱，并以 CC BY 4.0 发布。项目只复用课程演示所需的结构化子集，不包含大型原始图片文件。

## 3. 图模型

节点类型：

- `City`：城市节点，例如 `wd:Q956`（Beijing）。
- `Sight`：城市下的景点节点，例如 `rps:0290`（Forbidden City）。
- `Place`：`city_sight.js` 中的其他 Wikidata 地点实体。
- `Person`：人物节点，例如 `rpp:01`。
- `Image`：图片实体，不存储图片二进制，只存储图片实体 ID。

关系类型：

- `HAS_SIGHT`：`City -> Sight`。
- `HAS_IMAGE`：`City/Place/Person -> Image`。
- `CONTAINS`：`Image -> Image`，来自上游 contain 关系。

图数据可用集合形式表示为：

$$G=(V,E)$$

其中节点集合为：

$$V=V_{city}\cup V_{sight}\cup V_{place}\cup V_{person}\cup V_{image}$$

关系集合为：

$$E=E_{has\_sight}\cup E_{has\_image}\cup E_{contains}$$

## 4. 数据标准化规则

1. `city.js` 的 `wd:Q...` 原样保留。
2. `city_sight.js` 与 `pic_city.js` 中裸 `Q...` ID 统一规范化为 `wd:Q...`。
3. `people.js` 的 `rpp:...` 原样保留。
4. `pic_people.js` 的 `rp:...` 原样保留。
5. `pic_city.js` 图片 ID 使用前缀 `img-city:`，避免与实体 ID 冲突。
6. `contain.js` 中 URI 图片实体保留完整 URI，并在名称中显示最后一个路径片段。
7. 节点 ID 全局唯一；重复节点合并时，类型优先级为 `City > Sight > Person > Place > Image`。
8. 关系按 `(source_id, target_id, type)` 去重。

## 5. 处理产物

- `data/processed/nodes.csv`
  - `id`
  - `name`
  - `kind`
  - `source_file`
- `data/processed/relationships.csv`
  - `source_id`
  - `target_id`
  - `type`
  - `source_file`
- `data/processed/stats.json`
  - 节点数、各类型节点数、关系数、各类型关系数、数据质量统计。

## 6. Neo4j 导入策略

采用 Neo4j 5.26 LTS。所有节点先导入为 `:Entity`，再根据 `kind` 增加 `:City`、`:Sight`、`:Place`、`:Person`、`:Image` 标签。关系类型只允许固定白名单 `HAS_SIGHT`、`HAS_IMAGE`、`CONTAINS`，避免动态 Cypher 注入。

提供两种方式：

1. 推荐：Python 官方 Neo4j Driver 批量导入。
2. 教学：`LOAD CSV` Cypher 脚本，便于课堂展示数据库操作。

## 7. 可视化与查询

至少提供：

1. 北京及景点一跳查询。
2. 某人物与其图片实体查询。
3. 节点类型统计。
4. 关系类型统计。
5. 度数最高实体查询。
6. 两跳路径查询。
7. 图片 `CONTAINS` 子图查询。

## 8. 验证标准

预处理完成后必须满足：

- 节点 ID 非空且唯一。
- 关系端点均存在。
- 关系类型全部在白名单中。
- 不存在完全重复关系。
- `stats.json` 统计与 CSV 实际内容一致。
- 单元测试全部通过。

## 9. 文档与提交

仓库必须包含：

- 从零运行 README。
- 数据集分析文档。
- Neo4j 安装与配置文档。
- 数据预处理说明。
- 导入与查询教程。
- 截图清单。
- 完整课程实验报告 Markdown 模板。

所有数学表达统一使用 LaTeX。
