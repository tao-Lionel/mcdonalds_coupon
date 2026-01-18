"""
麦当劳麦麦省优惠券领取脚本
功能：
1. 麦麦省券列表查询
2. 麦麦省一键领券
3. 我的优惠券查询
"""

import os
import json
import requests
from datetime import datetime
from typing import Optional, Dict, Any


class McDonaldsMCPClient:
    """麦当劳 MCP 客户端"""

    def __init__(self, token: Optional[str] = None):
        """
        初始化客户端

        Args:
            token: MCP Token，如果为None则从环境变量MCD_MCP_TOKEN读取
        """
        self.token = token or os.getenv("MCD_MCP_TOKEN")
        if not self.token:
            raise ValueError("请设置环境变量 MCD_MCP_TOKEN 或直接传入token")

        self.base_url = "https://mcp.mcd.cn/mcp-servers/mcd-mcp"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.request_id = 0

    def _call_tool(self, tool_name: str, arguments: Optional[Dict] = None) -> Dict[str, Any]:
        """
        调用 MCP 工具

        Args:
            tool_name: 工具名称
            arguments: 工具参数

        Returns:
            工具执行结果
        """
        self.request_id += 1

        payload = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        }

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            if "error" in result:
                print(f"错误: {result['error']}")
                return {}

            return result.get("result", {})

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return {}

    def get_available_coupons(self) -> None:
        """查询麦麦省券列表"""
        print("=" * 50)
        print("📋 麦麦省券列表查询")
        print("=" * 50)

        result = self._call_tool("available-coupons")

        if result:
            content = result.get("content", [])
            for item in content:
                if item.get("type") == "text":
                    print(item.get("text", ""))
                elif item.get("type") == "image":
                    print(f"[图片]: {item.get('source', '')}")

    def auto_bind_coupons(self) -> None:
        """一键领取所有可用优惠券"""
        print("=" * 50)
        print("🎉 麦麦省一键领券")
        print("=" * 50)

        result = self._call_tool("auto-bind-coupons")

        if result:
            content = result.get("content", [])
            for item in content:
                if item.get("type") == "text":
                    print(item.get("text", ""))
                elif item.get("type") == "image":
                    print(f"[图片]: {item.get('source', '')}")

    def get_my_coupons(self) -> None:
        """查询我的优惠券列表"""
        print("=" * 50)
        print("👛 我的优惠券查询")
        print("=" * 50)

        result = self._call_tool("my-coupons")

        if result:
            content = result.get("content", [])
            for item in content:
                if item.get("type") == "text":
                    print(item.get("text", ""))
                elif item.get("type") == "image":
                    print(f"[图片]: {item.get('source', '')}")

    def get_campaign_calendar(self, specified_date: Optional[str] = None) -> None:
        """
        查询活动日历

        Args:
            specified_date: 指定日期范围(格式: yyyy-MM-dd)，返回该日期附近一共三天的活动
        """
        print("=" * 50)
        print("📅 活动日历查询")
        print("=" * 50)

        args = {}
        if specified_date:
            args["specifiedDate"] = specified_date

        result = self._call_tool("campaign-calender", args)

        if result:
            content = result.get("content", [])
            for item in content:
                if item.get("type") == "text":
                    print(item.get("text", ""))
                elif item.get("type") == "image":
                    print(f"[图片]: {item.get('source', '')}")

    def get_current_time(self) -> None:
        """获取当前时间信息"""
        print("=" * 50)
        print("🕐 当前时间信息")
        print("=" * 50)

        result = self._call_tool("now-time-info")

        if result:
            content = result.get("content", [])
            for item in content:
                if item.get("type") == "text":
                    print(item.get("text", ""))


def main():
    """主函数"""
    # 打印欢迎信息
    print("""
    ╔════════════════════════════════════════════════╗
    ║       麦当劳麦麦省优惠券领取工具 v1.0        ║
    ╚════════════════════════════════════════════════╝
    """)

    # 检查环境变量
    token = os.getenv("MCD_MCP_TOKEN")
    if not token:
        print("⚠️  请先设置环境变量 MCD_MCP_TOKEN")
        print("   Windows: set MCD_MCP_TOKEN=your_token_here")
        print("   Linux/Mac: export MCD_MCP_TOKEN=your_token_here")
        print("   或在代码中直接传入token参数")
        return

    try:
        # 初始化客户端
        client = McDonaldsMCPClient(token)

        while True:
            print("\n" + "=" * 50)
            print("请选择操作：")
            print("  1. 查询麦麦省券列表")
            print("  2. 一键领取优惠券")
            print("  3. 查询我的优惠券")
            print("  4. 查询活动日历")
            print("  5. 获取当前时间")
            print("  6. 全部执行（查询->领券->查看我的券）")
            print("  0. 退出")
            print("=" * 50)

            choice = input("\n请输入选项 (0-6): ").strip()

            if choice == "0":
                print("👋 再见！")
                break
            elif choice == "1":
                client.get_available_coupons()
            elif choice == "2":
                client.auto_bind_coupons()
            elif choice == "3":
                client.get_my_coupons()
            elif choice == "4":
                date_input = input("请输入日期 (yyyy-MM-dd，留空查询当前月): ").strip()
                client.get_campaign_calendar(date_input if date_input else None)
            elif choice == "5":
                client.get_current_time()
            elif choice == "6":
                print("\n🔄 开始执行完整流程...\n")
                client.get_available_coupons()
                print("\n" + "-" * 50 + "\n")
                client.auto_bind_coupons()
                print("\n" + "-" * 50 + "\n")
                client.get_my_coupons()
                print("\n✅ 流程执行完成！")
            else:
                print("❌ 无效选项，请重新选择")

    except KeyboardInterrupt:
        print("\n\n👋 用户中断，再见！")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")


if __name__ == "__main__":
    main()
