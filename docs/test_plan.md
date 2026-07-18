# Frappe CRM 测试计划

## 1. 文档信息

| 项目 | 内容 |
| --- | --- |
| 项目名称 | Frappe CRM 测试自动化 |
| 被测系统 | Frappe CRM |
| 文档版本 | 1.0 |
| 更新日期 | 2026-07-18 |
| 当前阶段 | 登录与 Lead 基础功能、接口和自动化验证 |

## 2. 测试背景

本项目面向本地部署的 Frappe CRM，通过 Web 功能测试、REST API 测试、pytest 自动化测试和数据库核对，验证登录及 Lead 核心流程。

当前仓库已经包含 Web 登录用例、Postman 集合、pytest 脚本、数据库查询脚本和测试截图。本计划以仓库中实际存在的内容为准，不将尚未实现的 Contact、Deal 等模块列为已完成范围。

## 3. 测试目标

1. 验证有效用户可以正常登录 Frappe CRM。
2. 验证错误密码、无效用户、必填项和异常输入能够被系统正确处理。
3. 验证登录 API 的状态码、响应内容和会话行为。
4. 验证 Lead 列表查询和 Lead 创建接口可以正常工作。
5. 验证接口创建的 Lead 数据能够写入 MariaDB。
6. 使用 pytest 建立可重复执行的基础回归测试。
7. 保存测试用例、执行结果和截图，保证测试过程可追溯。

## 4. 测试范围

### 4.1 范围内

| 模块 | 测试内容 | 测试方式 |
| --- | --- | --- |
| 登录页面 | 正常登录、错误密码、不存在用户、用户名/密码为空 | Web 手工测试、pytest |
| 登录输入校验 | 特殊字符、超长用户名、首尾空格 | Web 手工测试 |
| 登录安全性 | 连续多次错误登录 | Web 手工测试 |
| 登录 API | 成功与失败响应 | Postman、pytest |
| Lead 查询 | 查询列表、返回数据结构 | Postman、pytest |
| Lead 创建 | 正常创建、空姓名、非法手机号 | Postman、pytest |
| 数据持久化 | 核对最新 Lead 数据 | SQL |

### 4.2 暂不在范围内

- Contact 联系人管理
- Deal 商机管理
- Lead 修改与删除
- 权限、角色和多租户测试
- 性能、压力和容量测试
- 跨浏览器和移动端兼容性测试
- 完整安全渗透测试
- CI/CD 自动执行

以上内容可作为后续迭代范围，但当前仓库没有相应测试实现。

## 5. 测试对象与接口

| 对象 | 方法或入口 | 用途 |
| --- | --- | --- |
| CRM 登录页 | `http://localhost:8000` | Web 登录测试 |
| 登录接口 | `POST /api/method/login` | 建立登录会话 |
| Lead 资源接口 | `GET /api/resource/CRM%20Lead` | 查询 Lead 列表 |
| Lead 资源接口 | `POST /api/resource/CRM%20Lead` | 创建 Lead |
| Lead 数据表 | `tabCRM Lead` | 数据库结果核对 |

## 6. 测试环境

| 项目 | 环境 |
| --- | --- |
| 操作系统 | Windows 11 |
| 部署环境 | WSL2 + Docker |
| 被测系统 | Frappe CRM |
| 后端框架 | Frappe Framework |
| 数据库 | MariaDB |
| Web 浏览器 | 以当前执行截图所用浏览器为准 |
| 接口测试工具 | Postman |
| 自动化框架 | Python requests + pytest |
| 已验证 Python | `D:\anaconda\python.exe` |
| 数据库工具 | Navicat 或其他 MariaDB 客户端 |

### 6.1 环境前提

- Frappe CRM 服务已启动，`localhost:8000` 可以访问。
- 测试账号 `Administrator/admin` 可用。
- Python 解释器已安装 `pytest` 和 `requests`。
- 执行测试的账号拥有查询和创建 CRM Lead 的权限。
- MariaDB 客户端可以访问 Frappe CRM 使用的数据库。

## 7. 测试策略

### 7.1 Web 功能测试

从用户角度操作登录页面，验证页面跳转、提示信息、输入限制和连续失败后的系统行为。

### 7.2 等价类划分

登录数据划分为：

- 有效账号和有效密码
- 有效账号和错误密码
- 不存在的账号
- 空用户名
- 空密码
- 特殊字符用户名

### 7.3 边界值分析

重点检查超长用户名、空字符串和包含首尾空格的用户名。

### 7.4 API 测试

使用 Postman 和 requests 验证：

- HTTP 状态码
- JSON 响应结构
- 登录成功标志
- Lead 列表类型
- 创建结果中的字段值
- 非法输入不会触发服务器 500 错误

### 7.5 自动化回归

pytest 自动化包含：

- 登录参数化测试：5 组数据
- Lead 测试：4 个测试
- 合计：9 个测试实例

执行命令：

```powershell
python -m pytest automation -v
```

### 7.6 数据库验证

使用以下 SQL 查询最新 Lead：

```sql
SELECT *
FROM `tabCRM Lead`
ORDER BY creation DESC;
```

将接口请求数据、接口响应和数据库记录进行一致性核对。

## 8. 测试用例与覆盖情况

### 8.1 Web 登录用例

`testcases/login_web_testcase.xlsx` 当前包含 9 条用例：

| 用例 | 测试点 | 当前状态 |
| --- | --- | --- |
| login_001 | 正确账号密码登录 | 通过 |
| login_002 | 错误密码校验 | 通过 |
| login_003 | 不存在用户校验 | 失败 |
| login_004 | 用户名必填校验 | 通过 |
| login_005 | 密码必填校验 | 通过 |
| login_006 | 特殊字符输入校验 | 通过 |
| login_007 | 用户名长度边界校验 | 通过 |
| login_008 | 用户名首尾空格处理 | 失败 |
| login_009 | 错误登录次数限制 | 失败 |

汇总：通过 6 条，失败 3 条。

失败用例表示实际结果与当前预期不一致，需要进一步确认是产品缺陷还是需求预期需要调整：

- `login_003`：预期提示“用户不存在”，实际统一提示“登录无效”。
- `login_008`：带首尾空格的用户名实际可以登录。
- `login_009`：连续错误登录后未出现预期的锁定或安全限制提示。

### 8.2 Postman 集合

`postman/FrappeCRM.postman_collection.json` 包含 5 个请求：

1. Login Success
2. Login Wrong Password
3. Query Lead
4. Create Lead
5. Query Created Lead

Lead 请求保存了固定 Cookie。会话过期或环境重启后，需要重新登录并更新会话。

### 8.3 API Excel 用例

`testcases/api_testcase.xlsx` 当前包含 3 个工作表，但工作表内容为空。现阶段 API 覆盖以 Postman 集合和 pytest 脚本为准，后续应补充正式的 API 用例编号、请求数据、预期结果、实际结果和状态。

### 8.4 自动化脚本

| 文件 | 覆盖内容 |
| --- | --- |
| `automation/tests/test_login.py` | 登录成功、错误密码、不存在用户、空用户名、空密码 |
| `automation/tests/test_lead.py` | Lead 列表查询、正常创建、空姓名、非法手机号 |
| `automation/utils/api_client.py` | 登录、查询 Lead、创建 Lead 的请求封装 |

2026-07-18 本地完整执行结果：

```text
9 passed in 1.89s
```

## 9. 准入标准

开始执行测试前应满足：

- Frappe CRM 和 MariaDB 已正常启动。
- 登录页面及 API 可访问。
- 测试账号和权限准备完成。
- pytest、requests 和 Postman 可用。
- 测试数据不会影响生产或其他共享环境。

## 10. 准出标准

本阶段测试完成应满足：

- 计划内 Web 用例已执行并记录实际结果。
- pytest 测试可成功收集并执行。
- Postman 核心请求已执行并保存证据。
- Lead 创建结果已通过接口或数据库核对。
- 失败用例已记录，且明确后续处理方式。
- 测试截图、用例表和脚本已归档到仓库。

## 11. 缺陷分级建议

| 级别 | 定义 | 示例 |
| --- | --- | --- |
| 严重 | 核心流程不可用、数据损坏或服务崩溃 | 正确账号无法登录、创建 Lead 导致 500 |
| 高 | 主要功能错误且无可接受替代方案 | 未授权用户可以读取 Lead |
| 中 | 局部功能或校验不符合预期 | 登录安全限制未生效 |
| 低 | 提示文字、显示或易用性问题 | 错误提示与预期文案不一致 |

## 12. 风险与限制

| 风险或限制 | 影响 | 建议 |
| --- | --- | --- |
| API 地址和账号密码硬编码 | 无法直接切换环境 | 使用环境变量或 pytest 配置 |
| Postman 使用固定 Cookie | 会话过期后请求失败 | 使用登录脚本自动保存 Cookie |
| Lead 测试不清理数据 | 多次运行产生重复记录 | 增加测试数据清理机制 |
| 非法 Lead 仅断言“不为 500” | 无法确认业务校验是否正确 | 明确预期状态码和错误消息 |
| API Excel 用例为空 | 手工 API 用例不可追溯 | 补充结构化 API 测试用例 |
| Web 失败项尚未定性 | 可能混合缺陷与预期偏差 | 与需求方确认后更新预期 |
| 当前未配置依赖清单 | 新环境搭建不稳定 | 增加 `requirements.txt` |

## 13. 测试输出物

- `docs/test_plan.md`：测试计划
- `testcases/login_web_testcase.xlsx`：Web 登录测试用例及结果
- `testcases/api_testcase.xlsx`：API 测试用例空模板
- `postman/FrappeCRM.postman_collection.json`：Postman 集合
- `automation/`：pytest 自动化脚本
- `sql/lead_check.sql`：数据库验证 SQL
- `images/web/`：Web 测试截图
- `images/api_postman/`：Postman 测试截图
- `images/pytest/`：pytest 执行截图

## 14. 后续改进

1. 补充 API Excel 测试用例。
2. 将服务地址、用户名和密码改为环境配置。
3. 增加 Lead 更新、删除和精确错误响应断言。
4. 为自动化创建的数据增加清理步骤。
5. 增加 `requirements.txt` 和 pytest 项目配置。
6. 确认 3 条 Web 失败用例的需求预期并形成缺陷记录。
7. 在基础用例稳定后扩展 Contact 和 Deal 模块。
