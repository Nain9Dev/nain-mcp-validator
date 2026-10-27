# nain-mcp-validator

> Servidor independiente de Model Context Protocol (MCP) que proporciona validación determinista de activos 3D (verificaciones C1-C10), comprobación de integridad direccionada por contenido (SHA-256) e informes de conformidad fail-closed para agentes de ingeniería con IA.

[![Language: English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
[![Versión en Español](https://img.shields.io/badge/Versión-Español-red.svg)](#)
[![Protocolo](https://img.shields.io/badge/MCP-2024--11--05-0047AB)](https://modelcontextprotocol.io/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB)](https://www.python.org/)
[![Validación](https://img.shields.io/badge/Checks-C1_a_C10-22c55e)](docs/01-requirements.md)
[![Licencia](https://img.shields.io/badge/License-MIT-gray)](LICENSE)

---

## 1. Visión general

`nain-mcp-validator` resuelve la brecha de fiabilidad cuando los agentes de IA generan geometría CAD, mallas o especificaciones de ingeniería. En lugar de depender de inspecciones de texto probabilísticas, equipa a los agentes con herramientas de validación deterministas:

- `validate_mesh_invariants`: Validación topológica que impone cierre hermético (watertight), variedades 2-manifold, coherencia de normales hacia el exterior y el umbral cuántico de triángulos degenerados ($10^{-12}\text{ m}^2$).
- `verify_content_digest`: Verificación criptográfica de hashes de contenido SHA-256.
- `generate_conformance_report`: Produce auditorías de conformidad estandarizadas en Markdown con un veredicto fail-closed.

## 2. Inicio rápido y pruebas

```bash
# Ejecutar la suite de verificación pytest
pytest -v
```

## 3. Integración con clientes de IA

Añade el servidor a tu configuración de Claude Desktop o Cursor:

```json
{
  "mcpServers": {
    "nain-validator": {
      "command": "python",
      "args": ["-m", "nain_mcp_validator.server"],
      "cwd": "/ruta/a/nain-mcp-validator"
    }
  }
}
```

---

**Autor**: Aitor Nain Mendoza Vallejo  
**Estándares**: [NainDev Engineering Handbook](https://github.com/Nain9Dev/engineering-handbook)
