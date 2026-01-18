"""
麦当劳优惠券 MCP 服务器
使用 FastMCP 框架创建，可集成到 Claude Code CLI 中
"""

import os
from typing import Optional
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, ImageContent
import requests


# 创建 FastMCP 实例
mcp = FastMCP("mcdonalds-coupon")


def get_token() -> str:
    """获取 MCP Token"""
    token = os.getenv("MCD_MCP_TOKEN")
    if not token:
        raise ValueError("请设置环境变量 MCD_MCP_TOKEN")
    return token


def call_mcp_tool(tool_name: str, arguments: dict = None) -> dict:
    """
    调用麦当劳 MCP 工具

    Args:
        tool_name: 工具名称
        arguments: 工具参数

    Returns:
        工具执行结果
    """
    token = get_token()
    base_url = "https://mcp.mcd.cn/mcp-servers/mcd-mcp"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments or {}
        }
    }

    response = requests.post(base_url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()

    if "error" in result:
        raise Exception(f"MCP API 错误: {result['error']}")

    return result.get("result", {})


@mcp.tool()
def query_available_coupons() -> str:
    """
    查询麦麦省当前可用的优惠券列表

    Returns:
        优惠券列表信息
    """
    result = call_mcp_tool("available-coupons")
    output = []
    for item in result.get("content", []):
        if item.get("type") == "text":
            output.append(item.get("text", ""))
    return "\n".join(output) if output else "暂无可用优惠券"


@mcp.tool()
def auto_claim_coupons() -> str:
    """
    一键领取所有可用的优惠券

    Returns:
        领取结果信息
    """
    result = call_mcp_tool("auto-bind-coupons")
    output = []
    for item in result.get("content", []):
        if item.get("type") == "text":
            output.append(item.get("text", ""))
    return "\n".join(output) if output else "领取失败"


@mcp.tool()
def query_my_coupons() -> str:
    """
    查询我的优惠券列表（已领取的优惠券）

    Returns:
        我的优惠券信息
    """
    result = call_mcp_tool("my-coupons")
    output = []
    for item in result.get("content", []):
        if item.get("type") == "text":
            output.append(item.get("text", ""))
    return "\n".join(output) if output else "暂无优惠券"


@mcp.tool()
def query_campaign_calendar(specified_date: Optional[str] = None) -> str:
    """
    查询麦当劳活动日历

    Args:
        specified_date: 指定日期范围，格式: yyyy-MM-dd。
                       如果不指定，返回当前日期附近三天的活动。

    Returns:
        活动日历信息
    """
    arguments = {}
    if specified_date:
        arguments["specifiedDate"] = specified_date

    result = call_mcp_tool("campaign-calender", arguments)
    output = []
    for item in result.get("content", []):
        if item.get("type") == "text":
            output.append(item.get("text", ""))
    return "\n".join(output) if output else "暂无活动信息"


@mcp.tool()
def get_current_time() -> str:
    """
    获取服务器当前时间信息

    Returns:
        当前时间信息
    """
    result = call_mcp_tool("now-time-info")
    output = []
    for item in result.get("content", []):
        if item.get("type") == "text":
            output.append(item.get("text", ""))
    return "\n".join(output) if output else "获取时间失败"


@mcp.resource("mcdonalds://coupons/available")
def available_coupons_resource() -> str:
    """获取可用优惠券（作为资源）"""
    return query_available_coupons()


@mcp.resource("mcdonalds://coupons/mine")
def my_coupons_resource() -> str:
    """获取我的优惠券（作为资源）"""
    return query_my_coupons()


if __name__ == "__main__":
    # 运行 MCP 服务器
    mcp.run(transport="stdio")
