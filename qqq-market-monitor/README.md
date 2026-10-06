# QQQ Market Monitor

一个使用 Python 构建的 QQQ ETF 自动化市场简报与规则型风险监控系统。

项目每天获取 QQQ 的历史行情和估值元数据，计算 RSI、移动平均线、年化波动率和最大回撤，生成可解释的风险状态，并通过 HTML 邮件发送报告。

## Architecture

```text
Yahoo Finance
      ↓
Price history and metadata validation
      ↓
Indicators: RSI / SMA / volatility / drawdown
      ↓
Explainable risk engine
      ↓
HTML + plain-text report
      ↓
SMTP email delivery
```

## Local setup

需要 Python 3.11 或更高版本。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

复制 `.env.example`，然后设置环境变量。测试邮件生成时可以保持 `DRY_RUN=true`；这种模式只生成 `output/` 中的 HTML 报告，不会发送邮件。

真实发送时必须提供：

- `SMTP_USERNAME`：发件邮箱
- `SMTP_PASSWORD`：邮箱授权码，不是邮箱登录密码
- `RECEIVER_EMAILS`：收件人，多个地址用逗号分隔

运行：

```powershell
python -m qqq_monitor.main
```

## GitHub Actions

工作流使用 UTC 时间 `02:00` 运行，对应北京时间上午 `10:00`。GitHub Actions 的定时任务可能出现延迟，因此它适合“每天自动运行”，不应被描述为严格实时调度。

在仓库 Settings → Secrets and variables → Actions 中配置：

- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `RECEIVER_EMAILS`

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Limitations

- Yahoo Finance 的数据接口和 ETF 元数据可能暂时不可用。
- ETF 的 PE 是数据源提供的汇总字段，不等同于单一成分股 PE。
- 风险状态是可解释的规则监控，不是交易信号，也不构成投资建议。
- RSI 使用 Wilder smoothing，建议在后续版本中加入和基准软件的数值对照测试。
