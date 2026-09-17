# frontend · 前端

负责人：D · 网站前后端

Vue 3 + Vite + Three.js。W3-D2 建立骨架：三维点云浏览（旋转、平移、缩放）+ 右下角后端状态。

## 安装

需要 Node.js 18 以上。在 `frontend/` 目录下执行（Windows 下 PowerShell 跑不了 npm 的话，用 cmd）：

```bash
npm install
```

## 启动

先按 [backend/README.md](../backend/README.md) 启动后端，再执行：

```bash
npm run dev
```

打开 http://localhost:5173 ：

- 能看到示例点云（一栋楼 + 地面），鼠标左键旋转、右键平移、滚轮缩放
- 右下角显示“后端在线 · v0.1.0”；后端没开时显示“后端离线”

端口固定为 5173（后端 CORS 只放行这个端口），被占用时会直接报错。

## 目录

| 路径 | 说明 |
| --- | --- |
| `src/api/index.js` | **所有后端请求都从这里发**，页面组件里不要直接写 fetch 和后端地址 |
| `src/components/Viewer.vue` | 三维点云浏览，`src` 属性传入 ply 地址 |
| `src/App.vue` | 页面框架、后端状态 |
| `public/sample.ply` | 示例点云，由 `scripts/make_sample_ply.py` 生成 |
| `public/models/` | 放 A 导出的 `areaA.ply`、`cameras.json`（W5-A2，大文件不进仓库） |
| `.env.example` | 后端地址配置示例，复制为 `.env.local` 修改 |

## 约定

- 模型坐标 z 轴竖直向上，Viewer 里已设置 `camera.up = (0, 0, 1)`。
- COLMAP“世界到相机”位姿到 Three.js 的转换只在前端统一做，见 `docs/interfaces.md`。
