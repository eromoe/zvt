# Storage 配置说明 (Phase 2)

在 `config.json`（或 `zvt_home/config.json`）中可添加 `storage` 配置块，用于自定义存储路径和路由。

## 配置结构

```json
{
  "storage": {
    "base_path": null,
    "path_template": null,
    "storage_routes": {}
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `base_path` | string \| null | 数据根路径。`null` 时使用 `zvt_env["data_path"]`（即 `zvt_home/data`） |
| `path_template` | string \| null | 路径模板。占位符：`{base_path}`, `{provider}`, `{db_name}`, `{storage_id}`。`null` 时使用默认规则 |
| `storage_routes` | object | 路由覆盖。键格式 `"provider\|db_name"`，值为自定义 `storage_id` |

### 默认行为（不配置时）

- `storage_id = "{provider}_{db_name}"`（如 `em_stock_meta`）
- 路径：`{data_path}/{provider}/{provider}_{db_name}.db`

### 示例

**自定义 base_path：**
```json
{
  "storage": {
    "base_path": "/custom/data/path"
  }
}
```

**自定义 path_template（扁平目录）：**
```json
{
  "storage": {
    "path_template": "{base_path}/{storage_id}.db"
  }
}
```

**自定义 storage_routes（某 provider 使用不同 storage_id）：**
```json
{
  "storage": {
    "storage_routes": {
      "qmt|stock_1d_kdata": "qmt_realtime_stock_1d"
    }
  }
}
```
