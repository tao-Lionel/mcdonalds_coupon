---
name: mcdonalds-coupon
description: 麦当劳麦麦省优惠券查询和领取工具。支持查询可用优惠券、一键领券、查询我的优惠券、查询活动日历等功能。
author: Claude Code
version: 1.0.0
---

# 麦当劳优惠券工具

这个工具帮助你管理麦当劳麦麦省优惠券。

## 功能

- **查询可用优惠券** - 查看当前麦麦省可领取的优惠券列表
- **一键领取优惠券** - 自动领取所有可用的优惠券
- **查询我的优惠券** - 查看已领取的优惠券
- **查询活动日历** - 查看指定日期的麦当劳活动信息
- **获取当前时间** - 获取服务器当前时间信息

## 使用说明

在使用前，请确保已设置环境变量 `MCD_MCP_TOKEN`。

### 设置 Token

```bash
# Windows CMD
set MCD_MCP_TOKEN=your_token_here

# Windows PowerShell
$env:MCD_MCP_TOKEN="your_token_here"

# Linux/Mac
export MCD_MCP_TOKEN=your_token_here
```

## 指令说明

当用户想要：
- 查询/查看麦当劳优惠券 - 调用查询可用优惠券功能
- 领取/领取麦当劳优惠券 - 调用一键领取功能
- 查看我的优惠券/已领优惠券 - 调用查询我的优惠券功能
- 查询活动日历/麦当劳活动 - 调用查询活动日历功能

## 实现逻辑

你需要使用 `E:\Github\mcdonalds_coupon\mcdonalds_coupon.py` 文件中的 `McDonaldsMCPClient` 类来实现功能。

### 导入和初始化

```python
import sys
sys.path.insert(0, r"E:\Github\mcdonalds_coupon")

from mcdonalds_coupon import McDonaldsMCPClient

client = McDonaldsMCPClient()  # 会自动从环境变量读取 token
```

### 可用方法

| 方法 | 说明 |
|------|------|
| `client.get_available_coupons()` | 查询可用优惠券，打印结果 |
| `client.auto_bind_coupons()` | 一键领取所有优惠券，打印结果 |
| `client.get_my_coupons()` | 查询我的优惠券，打印结果 |
| `client.get_campaign_calendar(specified_date=None)` | 查询活动日历，可选指定日期 |
| `client.get_current_time()` | 获取当前时间信息 |

## 使用示例

用户输入 "帮我查询麦当劳优惠券"
你执行: `client.get_available_coupons()`

用户输入 "一键领取麦当劳优惠券"
你执行: `client.auto_bind_coupons()`

用户输入 "看看我有哪些优惠券"
你执行: `client.get_my_coupons()`

用户输入 "查询明天2025-01-19的活动"
你执行: `client.get_campaign_calendar("2025-01-19")`
