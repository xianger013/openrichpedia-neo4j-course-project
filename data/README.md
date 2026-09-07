# 数据目录说明

- `raw/`：由 `scripts/fetch_openrichpedia.py` 从 OpenRichpedia 固定提交下载的 6 个原始文件。为避免重复分发大文件，默认不提交完整原始文件。
- `processed/`：预处理后生成 `nodes.csv`、`relationships.csv` 和 `stats.json`。
- `demo/`：使用 `tests/fixtures/` 的小型样例生成，便于在没有网络时验证完整流程。

完整数据来源：OpenKG-ORG/OpenRichpedia，许可证为 CC BY 4.0。使用数据时应保留来源和署名信息。
