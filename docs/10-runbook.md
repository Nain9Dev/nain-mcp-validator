# Operational Runbook: nain-mcp-validator

## 1. Running Tests

```bash
pytest -v
```

## 2. MCP Client Integration

### Claude Desktop (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "nain-validator": {
      "command": "python",
      "args": ["-m", "nain_mcp_validator.server"],
      "cwd": "D:/Development/Personal-Projects/nain-mcp-validator"
    }
  }
}
```

### Antigravity IDE (`mcp_config.json`)
```json
{
  "mcpServers": {
    "nain-validator": {
      "command": "python",
      "args": ["-m", "nain_mcp_validator.server"]
    }
  }
}
```
