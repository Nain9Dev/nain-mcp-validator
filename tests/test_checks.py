from nain_mcp_validator.domain.checks import (
    Point3D,
    validate_triangular_mesh,
)


def test_closed_tetrahedron_is_conforming() -> None:
    # Regular tetrahedron (4 vertices, 4 faces)
    vertices = [
        Point3D(x=1.0, y=1.0, z=1.0),
        Point3D(x=-1.0, y=-1.0, z=1.0),
        Point3D(x=-1.0, y=1.0, z=-1.0),
        Point3D(x=1.0, y=-1.0, z=-1.0),
    ]
    # Outward winding
    faces = [
        (0, 1, 2),
        (0, 3, 1),
        (0, 2, 3),
        (1, 3, 2),
    ]

    result = validate_triangular_mesh(vertices, faces, bodies=1, genus=0)
    assert result.is_conforming is True
    assert result.c1_buffer_integrity is True
    assert result.c2_degenerate_faces == 0
    assert result.c3_is_manifold is True
    assert result.c4_is_watertight is True
    assert result.c5_is_winding_consistent is True
    assert result.euler_characteristic == 2  # V=4, E=6, F=4 -> 4 - 6 + 4 = 2


def test_degenerate_micro_face_fails_quantum_threshold() -> None:
    # Triangle with collinear vertices (area = 0.0)
    vertices = [
        Point3D(x=0.0, y=0.0, z=0.0),
        Point3D(x=1.0, y=0.0, z=0.0),
        Point3D(x=2.0, y=0.0, z=0.0),  # Collinear!
    ]
    faces = [(0, 1, 2)]

    result = validate_triangular_mesh(vertices, faces)
    assert result.is_conforming is False
    assert result.c2_degenerate_faces == 1
    assert any("C2:" in err for err in result.errors)


def test_open_mesh_fails_watertight_check() -> None:
    # Single triangle is open (3 boundary edges)
    vertices = [
        Point3D(x=0.0, y=0.0, z=0.0),
        Point3D(x=1.0, y=0.0, z=0.0),
        Point3D(x=0.0, y=1.0, z=0.0),
    ]
    faces = [(0, 1, 2)]

    result = validate_triangular_mesh(vertices, faces)
    assert result.is_conforming is False
    assert result.c4_is_watertight is False
    assert any("C4:" in err for err in result.errors)


def test_non_manifold_mesh_fails_manifold_check() -> None:
    # 3 triangles sharing edge (0, 1) -> non-manifold book fold
    vertices = [
        Point3D(x=0.0, y=0.0, z=0.0),
        Point3D(x=0.0, y=1.0, z=0.0),
        Point3D(x=1.0, y=0.0, z=0.0),
        Point3D(x=-1.0, y=0.0, z=0.0),
        Point3D(x=0.0, y=0.0, z=1.0),
    ]
    faces = [
        (0, 1, 2),
        (1, 0, 3),
        (0, 1, 4),  # Third face on edge (0, 1)
    ]

    result = validate_triangular_mesh(vertices, faces)
    assert result.is_conforming is False
    assert result.c3_is_manifold is False
    assert any("C3:" in err for err in result.errors)
