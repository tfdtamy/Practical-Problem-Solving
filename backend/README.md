# 后端（backend）

FastAPI 服务，负责用户与权限、照片上传审核、检索，并把配准与推理结果提供给前端。

## 安装

在 `backend/` 目录下执行（Windows PowerShell）：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS / Linux 把第二行换成 `source .venv/bin/activate`。

## 启动

```bash
uvicorn main:app --reload
```

启动后：

- 健康检查：http://localhost:8000/api/health 应返回 `{"status":"ok","version":"0.1.0"}`
- 接口文档：http://localhost:8000/docs

## 说明

- 前端开发服务器在 5173 端口，已在 `main.py` 中允许跨域。
- 按约定，所有计算（重建、配准、推理）都在服务器端完成，前端只通过接口访问，不包含计算代码。这样以后才能打包成桌面端或移动端应用。

## 接口

| 方法 | 路径 | 说明 | 对应需求 |
| --- | --- | --- | --- |
| GET | `/api/health` | 健康检查 | — |

后续接口按任务表推进，新增接口请在本表登记。
