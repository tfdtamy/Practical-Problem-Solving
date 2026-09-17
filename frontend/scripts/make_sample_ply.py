"""生成 public/sample.ply：一栋简化的楼 + 地面的示例点云，用于在 A 的真实点云到位前测试网页。

坐标单位为米，z 轴竖直向上（与 docs/interfaces.md 一致）。
用法（在 frontend/ 目录下）：python scripts/make_sample_ply.py
"""

from pathlib import Path

import numpy as np

rng = np.random.default_rng(2026)
parts = []

# 地面：40 m × 30 m，灰绿色
n = 12000
ground = np.column_stack([rng.uniform(-20, 20, n), rng.uniform(-15, 15, n), rng.normal(0, 0.02, n)])
ground_rgb = np.tile([110, 130, 95], (n, 1)) + rng.integers(-15, 15, (n, 3))
parts.append((ground, ground_rgb))

# 楼：长 16 m、宽 8 m、高 12 m，四个立面的砖红色墙面，带深色窗户
L, W, Hgt = 16.0, 8.0, 12.0
walls = [
    ("x", -W / 2), ("x", W / 2),  # 沿 x 方向的两个长立面，y 固定
    ("y", -L / 2), ("y", L / 2),  # 两个山墙，x 固定
]
for axis, fixed in walls:
    n = 9000 if axis == "x" else 4500
    u = rng.uniform(-L / 2, L / 2, n) if axis == "x" else rng.uniform(-W / 2, W / 2, n)
    z = rng.uniform(0, Hgt, n)
    pts = np.column_stack([u, np.full(n, fixed), z]) if axis == "x" else np.column_stack([np.full(n, fixed), u, z])
    rgb = np.tile([168, 82, 60], (n, 1)) + rng.integers(-12, 12, (n, 3))
    # 每层 3 m，窗户 1.2 m × 1.5 m
    in_window = ((u % 3.0) > 0.9) & ((u % 3.0) < 2.1) & ((z % 3.0) > 0.9) & ((z % 3.0) < 2.4) & (z > 1)
    rgb[in_window] = [45, 55, 70]
    parts.append((pts, rgb))

# 屋顶
n = 5000
roof = np.column_stack([rng.uniform(-L / 2, L / 2, n), rng.uniform(-W / 2, W / 2, n), np.full(n, Hgt)])
parts.append((roof, np.tile([90, 90, 95], (n, 1)) + rng.integers(-10, 10, (n, 3))))

xyz = np.vstack([p for p, _ in parts]).astype("<f4")
rgb = np.clip(np.vstack([c for _, c in parts]), 0, 255).astype("u1")

vertex = np.empty(len(xyz), dtype=[("x", "<f4"), ("y", "<f4"), ("z", "<f4"), ("red", "u1"), ("green", "u1"), ("blue", "u1")])
vertex["x"], vertex["y"], vertex["z"] = xyz.T
vertex["red"], vertex["green"], vertex["blue"] = rgb.T

header = (
    "ply\nformat binary_little_endian 1.0\n"
    f"element vertex {len(vertex)}\n"
    "property float x\nproperty float y\nproperty float z\n"
    "property uchar red\nproperty uchar green\nproperty uchar blue\n"
    "end_header\n"
)
out = Path(__file__).resolve().parent.parent / "public" / "sample.ply"
out.parent.mkdir(exist_ok=True)
with open(out, "wb") as f:
    f.write(header.encode("ascii"))
    f.write(vertex.tobytes())
print(f"写入 {out}，{len(vertex)} 个点，{out.stat().st_size / 1024:.0f} KB")
