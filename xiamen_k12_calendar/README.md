# Xiamen K-12 Calendar (Apple Calendar / iPhone Subscribable ICS)

这是一个可维护的 **厦门中小学上学与假期日历** GitHub 项目模板，适用于：

- 苹果手机 / iPad **订阅日历（ICS）**
- GitHub 仓库托管
- 每年维护学年数据后，自动重新生成 `.ics` 文件
- 未来扩展“补课 / 调休 / 特殊安排”

## 当前已写入的数据范围

- 2025-2026 学年（小学 / 初中，含已确认的开学、寒假、暑假、学期结束）

## 已写入的 2025-2026 学年事件

1. 2025-07-05 至 2025-08-31：暑假
2. 2025-09-01：秋季学期开学 / 正式上课
3. 2026-01-30：学期结束
4. 2026-01-31 至 2026-02-25：寒假
5. 2026-02-26：春季学期开学 / 正式上课

> 说明：补课日期目前**未写入**，因为补课通常以当年教育局或学校后续通知为准。
> 未来 2026-2030 的数据文件已预留，请在正式校历发布后补充。

## 文件结构

```text
xiamen_k12_calendar/
├─ README.md
├─ xiamen_k12_calendar.ics
├─ data/
│  ├─ 2025_2026.json
│  ├─ 2026_2027.json
│  ├─ 2027_2028.json
│  ├─ 2028_2029.json
│  └─ 2029_2030.json
├─ tools/
│  └─ generate_calendar.py
└─ .github/
   └─ workflows/
      └─ build_ics.yml
```

## 如何维护

### 1）每年更新 JSON
进入 `data/` 目录，编辑对应学年文件，例如 `2026_2027.json`。

每条事件格式如下：

```json
{
  "summary": "寒假",
  "start": "2027-01-30",
  "end": "2027-02-25",
  "all_day": true,
  "description": "小学、初中寒假"
}
```

说明：
- `start`：开始日期
- `end`：结束日期
- 对于全天多日事件，程序会自动将 `end` 作为**包含最后一天**来处理并转为 ICS 的 `DTEND +1 天`
- 单日事件可令 `start == end`

### 2）重新生成 ICS
本地运行：

```bash
python tools/generate_calendar.py
```

会更新根目录下的：

```text
xiamen_k12_calendar.ics
```

### 3）提交到 GitHub
```bash
git add .
git commit -m "update school calendar"
git push
```

## GitHub 上如何提供苹果日历订阅

将仓库设为 Public 后，使用 GitHub Raw 链接订阅：

```text
https://raw.githubusercontent.com/<your-username>/xiamen_k12_calendar/main/xiamen_k12_calendar.ics
```

### iPhone 添加方式
1. 设置
2. 日历
3. 账户
4. 添加账户
5. 其他
6. 添加已订阅日历
7. 粘贴上面的 Raw 链接

## 自动维护（GitHub Actions）

本项目已提供 `.github/workflows/build_ics.yml`：

- 当你 `push` 更新 `data/*.json` 时，自动重新生成 ICS
- 也支持手动在 GitHub Actions 页面点击运行
- 每月会自动跑一次，确保 `ics` 文件格式持续有效

## 注意事项

- GitHub 仓库名我已按可维护和下载兼容性，规范化为：`xiamen_k12_calendar`
- 若你坚持中文仓库名，也可以，但为了链接兼容与文件管理稳定，**推荐英文仓库名**
- “补课 / 调休”强烈建议以官方年度校历发布后再补入 JSON
