# 数据接口 v1

各模块之间交换文件的格式。**冻结于 2026-09-17**，此后改动须经组长同意并在群里通知。

通用约定：

- 模型坐标单位为**米**，经尺度对齐后 **z 轴竖直向上**。
- 相机位姿沿用 **COLMAP 的“世界到相机”约定**（`qvec` 为四元数 `[w,x,y,z]`，`tvec` 为平移）。相机中心 = −Rᵀ·t。网页显示时由前端统一转换，其他模块不要自行转换。
- 照片编号格式：`P` + 8 位日期 + 4 位序号，例如 `P202609160001`，同时作为文件名。
- 元素编号格式：`E` + 2 位区域号 + 4 位序号，例如 `E010003`。
- 任务编号格式：`T` + 8 位日期 + 5 位序号。

---

## 1. photos_meta（照片登记表）

位置：网盘 `chronoscope_data/photos_meta.xlsx`，后续导入数据库 `photos` 表
生产：C　　使用：组长、B、D

| 字段 | 类型 | 说明 | 示例 |
| --- | --- | --- | --- |
| `photo_id` | 字符串 | 照片编号，同时是文件名 | P202609160001 |
| `area` | 字符串 | 所属区域：A、B、HX（华西）、其他 | A |
| `location_hint` | 字符串 | 大致地点，建筑名或位置描述 | 某楼正门 |
| `year_from` | 整数 | 起始年份；未知留空 | 1985 |
| `year_to` | 整数 | 截止年份；精确年份时与 `year_from` 相同 | 1989 |
| `year_basis` | 文本 | 年份依据：文件信息 / 出版物 / 原文写明 / 贡献者填写 / 无。**只有前三种算“可信年份”**，可作为定年证据 | 原文写明 |
| `source_type` | 文本 | 本人拍摄 / 家庭收藏 / 单位档案 / 网络公开资料 / 其他 | 单位档案 |
| `source_note` | 字符串 | 来源说明：书名页码、链接、提供人 | 校史馆展陈，说明牌：…… |
| `public_ok` | 文本 | 是否同意公开展示：是 / 否 | 否 |
| `description` | 字符串 | 画面内容说明 | 学生在楼前合影 |

---

## 2. elements.json（结构元素）

位置：`recon/elements.json`　　生产：A　　使用：C、D

```json
[
  {
    "element_id": "E010003",
    "name": "某楼东侧配楼",
    "building": "某楼",
    "bbox_min": [12.3, -4.1, 0.0],
    "bbox_max": [25.8, 6.7, 14.2]
  }
]
```

包围盒坐标单位为米，使用尺度对齐后的模型坐标系。

---

## 3. cameras.json（现代影像相机）

位置：`frontend/public/models/`　　生产：A　　使用：D

```json
[
  {
    "image_name": "areaA_0123.jpg",
    "center": [3.2, 1.6, -20.5],
    "qvec": [0.99, 0.01, -0.12, 0.02]
  }
]
```

---

## 4. registration（配准结果，每张照片一个 JSON）

位置：`register/results/<方法>/<photo_id>.json`　　生产：B　　使用：组长、C、D

| 字段 | 类型 | 说明 | 示例 |
| --- | --- | --- | --- |
| `photo_id` | 字符串 | 照片编号 | P202609160001 |
| `status` | 文本 | `registered` 已配准 / `need_manual` 待人工校正 / `out_of_scope` 超出建模范围 | registered |
| `reason` | 文本 | status 不是 registered 时的原因：`few_matches` / `low_confidence` / `timeout` / `no_candidate` | "" |
| `qvec` | `[w,x,y,z]` | 相机朝向四元数 | [0.98, 0.02, -0.18, 0.01] |
| `tvec` | `[x,y,z]` | 平移向量 | [1.2, -0.3, 18.7] |
| `focal_px` | 实数 | 焦距，以照片长边缩放到 1600 像素时的像素数计 | 1850.5 |
| `width` / `height` | 整数 | 缩放后照片宽高（长边 1600） | 1600 / 1067 |
| `confidence` | 实数 | 配准置信度 0–1（W7 起有值，之前填 `null`） | 0.72 |
| `reproj_median_px` | 实数 | 重投影误差中位数（像素） | 3.4 |
| `num_inliers` | 整数 | 内点数 | 186 |
| `inlier_coverage` | 实数 | 内点覆盖率 0–1 | 0.41 |
| `best_candidate` | 字符串 | 最相似的现代影像文件名（今昔对比用） | areaA_0088.jpg |
| `method` | 文本 | `sift` / `sp_lg` / `sp_lg_mask` / `manual` | sp_lg_mask |
| `model_version` | 字符串 | 所用基底模型版本 | areaAB_v2 |
| `elapsed_s` | 实数 | 耗时（秒） | 17.3 |

---

## 5. observations.csv（存在性观测）

位置：`reasoning/output/observations.csv`　　生产：C　　使用：C、D

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `photo_id` | 字符串 | 照片编号 |
| `element_id` | 字符串 | 元素编号 |
| `state` | 文本 | `present` 存在 / `absent` 缺席 / `unknown` 无信息 |
| `score` | 实数 | 判定可信程度 0–1 |

---

## 6. intervals.json（存在区间）

位置：`reasoning/output/intervals.json`　　生产：C　　使用：D

```json
[
  {
    "element_id": "E010003",
    "appear": [1996, 1998],
    "disappear": "present",
    "status": "ok",
    "support": 9,
    "conflict": 1
  }
]
```

- `appear`：出现年份区间；早于最早的照片则为 `null`
- `disappear`：消失年份区间；至今仍在填 `"present"`
- `status`：`ok` / `insufficient` 证据不足 / `review` 待复核

---

## 7. dating.json（照片定年）

位置：`reasoning/output/dating.json`　　生产：C　　使用：D

```json
[
  {
    "photo_id": "P202609160001",
    "status": "ok",
    "year_range": [1994, 1997],
    "confidence": 0.75,
    "evidence": [
      {
        "element_id": "E010003",
        "name": "某楼东侧配楼",
        "state": "present",
        "interval": [1993, "present"],
        "agree": true
      }
    ]
  }
]
```

`status`：`ok` / `insufficient` 证据不足 / `too_wide` 区间过宽 / `conflict` 与登记年份矛盾
