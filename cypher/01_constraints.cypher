// 建议在导入前执行：为统一的 Entity.id 创建唯一约束。
CREATE CONSTRAINT entity_id_unique IF NOT EXISTS
FOR (n:Entity) REQUIRE n.id IS UNIQUE;
