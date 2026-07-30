# Frappe CRM 综合测试项目

## 项目简介

本项目围绕本地 Docker 环境部署的 Frappe CRM 登录与 CRM Lead（线索）模块开展综合测试，覆盖：

- Web 登录功能测试
- Postman REST API 测试
- Python + requests + pytest 接口自动化测试
- MariaDB 数据一致性验证
- JMeter 基准测试与梯度负载测试
- 禅道用例录入、测试单执行及 Bug 跟踪实践
- 测试计划、测试用例、截图和结果记录

完整测试策略、准入准出标准和风险说明见 [测试计划](docs/test_plan.md)。

## 测试覆盖情况

| 测试类型 | 测试内容 | 结果 |
| --- | --- | --- |
| Web 功能测试 | 正确登录、错误密码、不存在用户、必填校验、特殊字符、超长用户名、首尾空格、连续失败 | 9 条用例：6 条通过，3 条实际结果与预期不一致 |
| Postman 接口测试 | 登录成功、登录失败、查询 Lead、创建 Lead、查询已创建 Lead | 5 个请求 |
| pytest 自动化测试 | 登录参数化、Lead 查询、创建及异常输入校验 | 9 个测试实例，全部通过 |
| 数据库验证 | 查询 `tabCRM Lead`，核对接口响应和数据库记录 | 1 个 SQL 脚本 |
| JMeter 性能测试 | 1、5、10、20 线程梯度负载测试 | 4 个场景，错误率均为 0% |
| 禅道测试管理 | 录入用例、创建并执行测试单、失败用例转 Bug、跟踪缺陷状态 | 已完成基础流程实践 |

本地执行全部 pytest 自动化测试的结果：

```text
9 passed
```

## 性能测试结果

### 场景设计

- 测试对象：登录接口、Lead 列表查询接口
- 登录策略：每个线程仅登录 1 次，由 Cookie 管理器维护会话
- 查询请求：`GET /api/resource/CRM%20Lead?limit_page_length=20`
- 断言：登录响应包含 `Logged In`，Lead 响应包含 `data`
- 思考时间：每次查询间隔 0.5～1.5 秒
- 持续时间：每个场景 5 分钟
- 执行方式：JMeter 非 GUI 模式
- 结果指标：吞吐量、平均响应时间、P90、P95、P99、最大响应时间和错误率

### Lead 查询结果

| 线程数 | Lead 样本数 | 吞吐量 | 平均响应时间 | P90 | P95 | P99 | 最大响应时间 | 错误率 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 294 | 0.986 次/秒 | 9.96 ms | 12 ms | 13 ms | 19.3 ms | 36 ms | 0% |
| 5 | 1466 | 4.906 次/秒 | 9.92 ms | 12 ms | 14 ms | 25 ms | 62 ms | 0% |
| 10 | 2937 | 9.828 次/秒 | 9.85 ms | 12 ms | 14 ms | 22 ms | 172 ms | 0% |
| 20 | 5769 | 19.328 次/秒 | 10.14 ms | 13 ms | 17 ms | 27 ms | 87 ms | 0% |

### 结果分析

- 20 线程持续 5 分钟，共完成 5769 次 Lead 查询，错误率为 0%。
- 线程数从 1 增加到 20 时，吞吐量接近线性增长。
- 平均响应时间保持在约 10 ms，20 线程场景下 P95 为 17 ms、P99 为 27 ms。
- 当前测试没有出现明显性能拐点，因此只能说明系统在本次测试环境和负载下运行稳定，不能将 20 线程描述为系统最大并发能力。
- 以上数据来自本地 Docker 开发环境和较小数据集，不代表生产环境容量。
- 为避免本地环境中 Redis Worker 空闲超时带停开发 Web 服务，本次 HTTP 查询负载测试暂时关闭了后台 Worker，因此结果仅代表 Web 查询场景。

## 项目结构

```text
Frappe-CRM-Test-Automation/
├─ automation/
│  ├─ tests/
│  │  ├─ test_login.py                  # 登录接口参数化测试
│  │  └─ test_lead.py                   # Lead 查询、创建及异常输入测试
│  └─ utils/
│     └─ api_client.py                  # Frappe API 请求封装
├─ docs/
│  └─ test_plan.md                      # 测试计划
├─ images/
│  ├─ api_postman/                      # Postman 测试截图
│  ├─ pytest/                           # pytest 运行截图
│  └─ web/                              # Web 登录测试截图
├─ performance/
│  └─ frappe_lead_performance.jmx       # JMeter 性能测试脚本
├─ postman/
│  └─ FrappeCRM.postman_collection.json
├─ sql/
│  └─ lead_check.sql                    # Lead 数据库验证 SQL
├─ testcases/
│  ├─ login_web_testcase.xlsx           # Web 登录测试用例和执行结果
│  └─ api_testcase.xlsx                 # API 测试用例工作簿
├─ .gitignore
└─ README.md
```

JMeter 的原始 JTL 文件和 HTML 报告由本地运行生成，已通过 `.gitignore` 排除，不提交到仓库。

## 测试环境

| 项目 | 配置 |
| --- | --- |
| 操作系统 | Windows 11 |
| 部署方式 | WSL2 + Docker |
| 被测系统 | Frappe CRM |
| 服务地址 | `http://localhost:8000` |
| 数据库 | MariaDB |
| 接口测试工具 | Postman |
| 自动化测试 | Python + requests + pytest |
| 性能测试工具 | Apache JMeter 5.6.3 |
| 测试管理工具 | 禅道 |
| Python 解释器 | `D:\anaconda\python.exe` |

## 运行前准备

1. 启动 Frappe CRM，并确认浏览器可以访问：

   ```text
   http://localhost:8000
   ```

2. 准备具有 CRM Lead 访问权限的测试账号。不要将真实账号密码提交到仓库。

3. 安装自动化测试依赖：

   ```powershell
   python -m pip install pytest requests
   ```

4. 运行性能测试前安装 Java 8 或更高版本，并准备 Apache JMeter 5.6.3。

## 运行 pytest 自动化测试

在项目根目录执行：

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
5. 将运行配置的工作目录设置为项目根目录。
6. 点击测试函数左侧的绿色三角运行。

成功时会看到类似结果：

```text
9 passed
进程已结束，退出代码为 0
```

## 运行 JMeter 性能测试

JMX 文件中的用户名和密码使用 JMeter 属性读取：

- `CRM_USER`：默认值为 `Administrator`
- `CRM_PASSWORD`：无默认值，必须在运行时传入

PowerShell 示例：

```powershell
$run = "load_test_01"
$jmeter = "D:\xz\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat"
$result = "performance\results\$run\result.jtl"
$report = "performance\reports\$run"

New-Item -ItemType Directory -Force "performance\results\$run"

& $jmeter `
  -n `
  -t "performance\frappe_lead_performance.jmx" `
  -JCRM_USER="Administrator" `
  -JCRM_PASSWORD="<本地测试密码>" `
  -l $result `
  -e `
  -o $report
```

注意：

- `<本地测试密码>`需要替换为本地测试环境的密码。
- 不要把密码直接写入 JMX、README 或 Git 提交记录。
- HTML 报告输出目录必须为空或不存在。
- 正式负载测试应禁用“查看结果树”和“汇总报告”等 GUI 监听器。
- 修改线程数、Ramp-Up 和持续时间后，应保存 JMX 再通过非 GUI 模式运行。

## Postman 使用说明

导入以下集合：

```text
postman/FrappeCRM.postman_collection.json
```

重新启动 Frappe、会话过期或切换环境后，应先执行登录请求，再执行需要身份认证的 Lead 请求。固定 Cookie 不适合直接跨环境复用。

## 数据库验证

执行 [lead_check.sql](sql/lead_check.sql) 查看最新创建的 Lead：

```sql
SELECT *
FROM `tabCRM Lead`
ORDER BY creation DESC;
```

可将接口响应中的姓名、手机号和邮箱与数据库记录进行一致性核对。

## 测试证据

- Web 登录截图：`images/web/`
- Postman 截图：`images/api_postman/`
- pytest 截图：`images/pytest/`
- Web 用例及执行结果：`testcases/login_web_testcase.xlsx`
- JMeter 脚本：`performance/frappe_lead_performance.jmx`
- 性能结果摘要：本 README 的“性能测试结果”章节

## 当前限制

- 自动化测试代码中的服务地址和部分测试账号数据仍为本地配置，后续可改为环境变量或配置文件。
- Postman 集合的会话信息不适合直接跨环境复用。
- 创建 Lead 后没有自动清理测试数据，多次运行会产生重复测试记录。
- Lead 的空姓名和非法手机号场景目前只检查服务器不返回 500，尚未严格断言业务校验结果。
- Contact、Deal、Lead 修改和删除等模块尚未纳入当前自动化范围。
- 当前仅完成基准测试和梯度负载测试，尚未通过持续加压找到系统性能拐点，也尚未完成长时间稳定性测试。
