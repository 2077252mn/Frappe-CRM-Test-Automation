# Frappe CRM 测试自动化项目

## 项目简介

本项目用于验证本地部署的 Frappe CRM，当前覆盖登录和 CRM Lead（线索）相关场景，包括：

- Web 登录功能测试
- Frappe REST API 接口测试
- pytest 接口自动化测试
- Postman 接口调试与断言
- MariaDB 数据核对
- 测试过程截图与结果留档

完整测试策略、准入准出标准和风险说明见 [测试计划](docs/test_plan.md)。

## 当前覆盖情况

| 测试类型 | 当前内容 | 数量或状态 |
| --- | --- | --- |
| Web 功能测试 | 登录成功、错误密码、不存在用户、必填、特殊字符、超长用户名、空格、连续失败 | 9 条用例 |
| Web 执行结果 | 通过 6 条，失败 3 条 | 失败项已记录在用例表 |
| Postman 接口测试 | 登录成功、登录失败、查询 Lead、创建 Lead、查询已创建 Lead | 5 个请求 |
| pytest 自动化 | 登录参数化测试、Lead 查询与创建校验 | 9 个测试实例 |
| 数据库验证 | 查询 `tabCRM Lead` 并按创建时间倒序检查 | 1 个 SQL 脚本 |
| API Excel 用例 | `api_testcase.xlsx` | 当前为 3 个空工作表，待补充 |

2026-07-18 在本地执行全部自动化测试的结果：

```text
9 passed in 1.89s
```

## 项目结构

```text
Frappe-CRM-Test-Automation/
├─ automation/
│  ├─ tests/
│  │  ├─ test_login.py          # 登录接口参数化测试
│  │  └─ test_lead.py           # Lead 查询和创建测试
│  └─ utils/
│     └─ api_client.py          # Frappe API 请求封装
├─ docs/
│  └─ test_plan.md              # 测试计划
├─ images/
│  ├─ api_postman/              # Postman 测试截图
│  ├─ pytest/                   # pytest 运行截图
│  └─ web/                      # Web 登录测试截图
├─ postman/
│  └─ FrappeCRM.postman_collection.json
├─ sql/
│  └─ lead_check.sql
├─ testcases/
│  ├─ login_web_testcase.xlsx   # Web 登录测试用例和结果
│  └─ api_testcase.xlsx         # API 用例空模板
└─ README.md
```

## 测试环境

| 项目 | 配置 |
| --- | --- |
| 操作系统 | Windows 11 |
| 部署方式 | WSL2 + Docker |
| 被测系统 | Frappe CRM |
| 服务地址 | `http://localhost:8000` |
| 数据库 | MariaDB |
| 接口工具 | Postman |
| 自动化框架 | Python + requests + pytest |
| 已验证解释器 | `D:\anaconda\python.exe` |

## 运行前准备

1. 确认 Frappe CRM 已启动，并且浏览器可以访问：

   ```text
   http://localhost:8000
   ```

2. 确认测试环境存在以下账号：

   ```text
   用户名：Administrator
   密码：admin
   ```

3. 安装自动化测试依赖：

   ```powershell
   python -m pip install pytest requests
   ```

> 当前服务地址和登录数据写在代码中。如果本地环境不同，需要修改 `automation/utils/api_client.py` 和对应测试数据。

## 命令行运行

必须在项目根目录运行：

```powershell
python -m pytest automation -v
```

仅运行登录测试：

```powershell
python -m pytest automation/tests/test_login.py -v
```

仅运行 Lead 测试：

```powershell
python -m pytest automation/tests/test_lead.py -v
```

## 在 PyCharm 中运行

1. 打开“设置 → Python → 解释器”。
2. 选择已安装 `pytest` 和 `requests` 的解释器，例如 `D:\anaconda\python.exe`。
3. 打开“设置 → Python → 集成工具”。
4. 将“默认测试运行程序”设置为 `pytest`。
5. 打开测试文件，点击测试函数或测试类左侧的绿色三角运行。

运行配置的工作目录应为：

```text
D:\rjcstest\Frappe-CRM-Test-Automation
```

成功时会看到类似结果：

```text
9 passed
进程已结束，退出代码为 0
```

## Postman 使用说明

导入以下集合：

```text
postman/FrappeCRM.postman_collection.json
```

集合中的 Lead 请求目前保存了固定的 `Cookie`。重新启动 Frappe、会话过期或切换环境后，应先执行登录请求，再更新会话信息，否则 Lead 请求可能返回未授权。

## 数据库验证

执行 [lead_check.sql](sql/lead_check.sql) 可以查看最新创建的 Lead：

```sql
SELECT *
FROM `tabCRM Lead`
ORDER BY creation DESC;
```

可将接口响应中的姓名、手机号和邮箱与数据库记录进行核对。

## 测试证据

- Web 登录截图：`images/web/`
- Postman 截图：`images/api_postman/`
- pytest 截图：`images/pytest/`
- Web 用例执行结果：`testcases/login_web_testcase.xlsx`

## 当前限制

- API 地址、管理员账号和密码仍为硬编码。
- Postman 集合包含固定会话 Cookie，不适合直接跨环境使用。
- 创建 Lead 后没有自动清理测试数据，多次运行会产生重复测试记录。
- Lead 的空姓名和非法手机号场景目前只检查服务器不返回 500，尚未严格断言业务校验结果。
- `api_testcase.xlsx` 当前没有实际测试用例。
- Contact、Deal、Lead 修改和删除等模块尚未实现，不属于当前已完成范围。
