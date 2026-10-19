from __future__ import annotations

import math
from collections.abc import Sequence

from pydantic import BaseModel, Field

QUANTUM_AREA_THRESHOLD: float = 1e-12  # m^2 threshold for micro-degeneracy

class Point3D(BaseModel):
    x: float
    y: float
    z: float

class MeshValidationResult(BaseModel):
    is_conforming: bool
    vertex_count: int
    face_count: int
    edge_count: int
    euler_characteristic: int
    c1_buffer_integrity: bool
    c2_degenerate_faces: int
    c3_is_manifold: bool
    c4_is_watertight: bool
    c5_is_winding_consistent: bool
    errors: list[str] = Field(default_factory=list)

def _triangle_area(p0: Point3D, p1: Point3D, p2: Point3D) -> float:
    # Cross product of (p1 - p0) and (p2 - p0)
    v1x, v1y, v1z = p1.x - p0.x, p1.y - p0.y, p1.z - p0.z
    v2x, v2y, v2z = p2.x - p0.x, p2.y - p0.y, p2.z - p0.z

    cx = v1y * v2z - v1z * v2y
    cy = v1z * v2x - v1x * v2z
    cz = v1x * v2y - v1y * v2x

    cross_norm = math.sqrt(cx * cx + cy * cy + cz * cz)
    return 0.5 * cross_norm

def validate_triangular_mesh(
    vertices: Sequence[Point3D | tuple[float, float, float]],
    faces: Sequence[tuple[int, int, int]],
    bodies: int = 1,
    genus: int = 0,
) -> MeshValidationResult:
    errors: list[str] = []

    # Normalize vertices to Point3D
    pts: list[Point3D] = []
    for i, v in enumerate(vertices):
        if isinstance(v, Point3D):
            p = v
        else:
            p = Point3D(x=v[0], y=v[1], z=v[2])
        if math.isnan(p.x) or math.isnan(p.y) or math.isnan(p.z):
            errors.append(f"C1: Vertex {i} contains NaN coordinates")
        pts.append(p)

    vertex_count = len(pts)
    face_count = len(faces)

    # C1: Buffer integrity & index bounds
    c1_pass = True
    for f_idx, (i0, i1, i2) in enumerate(faces):
        if i0 < 0 or i0 >= vertex_count or i1 < 0 or i1 >= vertex_count or i2 < 0 or i2 >= vertex_count:
            errors.append(f"C1: Face {f_idx} references out-of-bounds vertex index ({i0}, {i1}, {i2})")
            c1_pass = False

    # C2: Quantum threshold degenerate faces
    degenerate_count = 0
    if c1_pass:
        for f_idx, (i0, i1, i2) in enumerate(faces):
            area = _triangle_area(pts[i0], pts[i1], pts[i2])
            if area < QUANTUM_AREA_THRESHOLD:
                degenerate_count += 1
                errors.append(f"C2: Face {f_idx} area ({area:.2e} m²) is below quantum threshold ({QUANTUM_AREA_THRESHOLD:.0e} m²)")

    # Build directed and undirected edge maps
    # Directed edge: (u, v) -> count
    # Undirected edge: (min(u, v), max(u, v)) -> list of faces
    edge_face_count: dict[tuple[int, int], int] = {}
    directed_edges: dict[tuple[int, int], int] = {}

    for f_idx, (i0, i1, i2) in enumerate(faces):
        tri_edges = [(i0, i1), (i1, i2), (i2, i0)]
        for u_idx, v_idx in tri_edges:
            directed_edges[(u_idx, v_idx)] = directed_edges.get((u_idx, v_idx), 0) + 1
            undirected = (min(u_idx, v_idx), max(u_idx, v_idx))
            edge_face_count[undirected] = edge_face_count.get(undirected, 0) + 1

    edge_count = len(edge_face_count)

    # C3: 2-Manifold check (each undirected edge shared by at most 2 faces)
    c3_manifold = True
    non_manifold_edges = [edge for edge, count in edge_face_count.items() if count > 2]
    if non_manifold_edges:
        c3_manifold = False
        errors.append(f"C3: Found {len(non_manifold_edges)} non-manifold edges shared by > 2 faces")

    # C4: Watertight closure (every undirected edge shared by exactly 2 faces)
    c4_watertight = True
    boundary_edges = [edge for edge, count in edge_face_count.items() if count == 1]
    if boundary_edges:
        c4_watertight = False
        errors.append(f"C4: Mesh has {len(boundary_edges)} boundary edges (open mesh / not watertight)")

    # C5: Normal / Winding consistency (opposing directed edges)
    c5_winding = True
    for (u_node, v_node), count in directed_edges.items():
        if count > 1:
            c5_winding = False
            errors.append(f"C5: Directed edge ({u_node}, {v_node}) appears {count} times (inconsistent face winding)")
            break

    # C10: Euler-Poincaré invariant: chi = V - E + F = 2 * (bodies - genus)
    expected_chi = 2 * (bodies - genus)
    actual_chi = vertex_count - edge_count + face_count
    if c4_watertight and actual_chi != expected_chi:
        errors.append(f"C10: Euler characteristic mismatch: V - E + F = {actual_chi}, expected {expected_chi}")

    is_conforming = (
        c1_pass
        and degenerate_count == 0
        and c3_manifold
        and c4_watertight
        and c5_winding
        and len(errors) == 0
    )

    return MeshValidationResult(
        is_conforming=is_conforming,
        vertex_count=vertex_count,
        face_count=face_count,
        edge_count=edge_count,
        euler_characteristic=actual_chi,
        c1_buffer_integrity=c1_pass,
        c2_degenerate_faces=degenerate_count,
        c3_is_manifold=c3_manifold,
        c4_is_watertight=c4_watertight,
        c5_is_winding_consistent=c5_winding,
        errors=errors,
    )
