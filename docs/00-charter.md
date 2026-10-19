# Project Charter: nain-mcp-validator

## 1. Executive Summary

**nain-mcp-validator** is a production-grade, open-source **Model Context Protocol (MCP)** server providing deterministic 3D asset validation (checks C1-C10), content-addressed artifact verification (SHA-256), and fail-closed conformance reporting for AI coding assistants and autonomous engineering agents (Claude Desktop, Cursor, Antigravity).

## 2. Problem Statement

LLM agents generating 3D models (GLB, glTF, STEP, STL) or CAD specifications often produce non-manifold boundaries, self-intersections, inverted normals, or degenerate sliver polygons. Because generative LLMs lack spatial awareness, validation must be strictly offloaded to a **deterministic validation gate** that fails closed when invariants are violated.

## 3. Core Principles

- **Zero Hallucination Tolerance**: All checks rely on deterministic topological geometry, not probabilistic heuristics.
- **Fail-Closed Gating**: An asset is rejected if any gate from C1 to C10 fails.
- **Content Addressing**: Every artifact is identified and verified against its SHA-256 hash.
- **Standard MCP Protocol**: Full compliance with the Anthropic Model Context Protocol specification over stdio JSON-RPC 2.0.
