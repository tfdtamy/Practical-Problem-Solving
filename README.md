# 时叠 Chronoscope

校园历史影像三维定位与定年平台 —— 以四川大学望江校区为例

《问题求解实战》课程项目。把散落的校园历史照片定位到三维校园模型中，推断建筑变化年代与照片拍摄年代，并提供三维时空浏览与检索。

## 目录结构

| 目录 | 负责人 | 内容 |
| --- | --- | --- |
| `docs/` | 组长 | 数据接口 `interfaces.md`、目标区域 `areas.md`、评测方案、问题清单 `issues.md` |
| `recon/` | A · 三维基底 | 重建脚本、各区域的 `report.md`（模型文件放网盘，不进仓库） |
| `register/` | B · 照片配准 | `localize.py`、`batch.py`、`mask.py`、测试集脚本 |
| `reasoning/` | C · 数据与推理 | `project_elements.py`、`presence.py`、`intervals.py`、`dating.py` |
| `tools/` | C、组长 | `exif_extract.py`、`preprocess.py`、`face_blur.py`、`import_registrations.py` |
| `backend/` | D · 网站 | FastAPI 后端 |
| `frontend/` | D · 网站 | Vue 3 + Three.js 前端 |
| `eval/` | 组长 | 评测脚本、人工判定表、`results/` 实验结果 |

## 交付规范

1. 代码提交到仓库对应目录，commit 信息以任务编号开头，例如 `W4-B1 完成定位脚本`。
2. 照片、三维模型等大文件放共享网盘，不要提交到仓库。
3. 完成任务后在群里发：任务编号 + 交付物截图或路径 + 一句话说明。
4. 每周四中午 12:00 截止，课后开 20 分钟周会。
5. 卡住超过 1 小时直接在群里问，附上报错截图。

## 数据放在哪

| 内容 | 位置 |
| --- | --- |
| 代码 | 本仓库 |
| 照片原图、处理图、展示图 | 网盘 `chronoscope_data/photos/` |
| 照片登记表 `photos_meta.xlsx` | 网盘 `chronoscope_data/` |
| 现代影像 | 网盘 `chronoscope_data/modern/areaA`、`areaB`、`path_AB` |
| COLMAP 模型、导出的 ply | 网盘 `chronoscope_data/recon/` |
| 需求文档、任务分工表 | 课程文件夹 PPS |

## 各模块怎么跑

- 后端：见 [backend/README.md](backend/README.md)
- 前端：见 `frontend/README.md`（W3-D2 建立）
- 其余模块在各自目录的 README 中说明

## 约定

- 模型坐标单位为米，z 轴竖直向上。
- 相机位姿沿用 COLMAP 的“世界到相机”约定，网页显示时由前端统一转换，其他模块不要自行转换。
- 模块之间交换的文件格式以 [docs/interfaces.md](docs/interfaces.md) 为准，改动需经组长同意。
