from nain_mcp_validator.domain.checks import MeshValidationResult


def generate_markdown_report(asset_name: str, result: MeshValidationResult) -> str:
    verdict_badge = "**PASSED (Conforming)**" if result.is_conforming else "**FAILED (Non-Conforming)**"

    report_lines = [
        f"# Deterministic 3D Conformance Report: {asset_name}",
        "",
        f"- **Verdict**: {verdict_badge}",
        f"- **Euler Characteristic**: $\\chi = {result.euler_characteristic}$ (V={result.vertex_count}, E={result.edge_count}, F={result.face_count})",
        "",
        "## Invariant Validation Matrix",
        "",
        "| Check Code | Invariant Target | Result | Details |",
        "| :--- | :--- | :---: | :--- |",
        f"| **C1** | Buffer Integrity & Bounds | {'PASS' if result.c1_buffer_integrity else 'FAIL'} | 0 NaN or out-of-bound indices |",
        f"| **C2** | Quantum Threshold ($10^{{-12}}\\text{{ m}}^2$) | {'PASS' if result.c2_degenerate_faces == 0 else 'FAIL'} | {result.c2_degenerate_faces} degenerate faces detected |",
        f"| **C3** | 2-Manifold Topology | {'PASS' if result.c3_is_manifold else 'FAIL'} | Edge-to-face adjacency bound <= 2 |",
        f"| **C4** | Watertight Closure | {'PASS' if result.c4_is_watertight else 'FAIL'} | Closed boundary envelope |",
        f"| **C5** | Winding & Normal Consistency | {'PASS' if result.c5_is_winding_consistent else 'FAIL'} | Coherent half-edge orientations |",
        "",
    ]

    if result.errors:
        report_lines.append("## Gating Discrepancies & Violations")
        report_lines.append("")
        for err in result.errors:
            report_lines.append(f"- `{err}`")
        report_lines.append("")
    else:
        report_lines.append("## Gate Verdict")
        report_lines.append("")
        report_lines.append("All deterministic invariants satisfied. Asset cleared for downstream manufacturing / 3D rendering pipeline.")
        report_lines.append("")

    return "\n".join(report_lines)
