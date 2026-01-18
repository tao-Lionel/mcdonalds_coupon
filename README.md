# 麦当劳优惠券 MCP 服务器

基于 FastMCP 框架的麦当劳麦麦省优惠券管理工具，可集成到 Claude Code CLI 中使用。

## 功能特性

- 查询麦麦省可用优惠券列表
- 一键领取所有可用优惠券
- 查询我的优惠券（已领取）
- 查询麦当劳活动日历
- 获取服务器当前时间

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/mcdonalds_coupon.git
cd mcdonalds_coupon
```

### 2. 安装依赖

```bash
pip install mcp requests
```

### 3. 配置 Token

复制环境变量模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 Token（从 [https://mcp.mcd.cn](https://mcp.mcd.cn) 获取）：

```bash
MCD_MCP_TOKEN=your_token_here
```

## 配置 MCP 服务

### 方法一：使用 claude mcp 命令（推荐）

使用 Claude Code CLI 的 MCP 命令进行配置。支持三种配置范围：

#### 用户级配置（全局可用，推荐）

```bash
claude mcp add -s user -e MCD_MCP_TOKEN=你的token mcdonalds-coupon -- python "/path/to/mcd_server.py"
```

配置后需要手动添加环境变量到 `~/.claude.json`：

```json
{
  "mcpServers": {
    "mcdonalds-coupon": {
      "type": "stdio",
      "command": "python",
      "args": ["/path/to/mcd_server.py"],
      "env": {
        "MCD_MCP_TOKEN": "你的token"
      }
    }
  }
}
```

#### 项目级配置（仅当前项目）

```bash
# 在项目目录下执行
claude mcp add -s project -e MCD_MCP_TOKEN=你的token mcdonalds-coupon -- python "/path/to/mcd_server.py"
```

#### 本地级配置（默认方式）

```bash
claude mcp add -e MCD_MCP_TOKEN=你的token mcdonalds-coupon -- python "/path/to/mcd_server.py"
```

#### 配置范围对比

| 配置方式 | 作用范围 | 推荐场景 |
|---------|---------|---------|
| 用户级 (`-s user`) | 所有项目 | **推荐**，多项目共用 |
| 项目级 (`-s project`) | 仅当前项目 | 项目特定配置 |
| 本地级（默认） | 当前位置 | 快速测试 |

#### 其他有用的 MCP 命令

| 命令 | 说明 |
|------|------|
| `claude mcp list` | 列出所有已配置的 MCP 服务器 |
| `claude mcp remove <name>` | 移除指定的 MCP 服务器 |
| `claude mcp enable <name>` | 启用某个 MCP 服务器 |
| `claude mcp disable <name>` | 禁用某个 MCP 服务器 |
| `claude mcp edit` | 编辑 MCP 配置文件 |

### 方法二：手动编辑配置文件

在 Claude Code 的配置文件中添加：

```json
{
  "mcpServers": {
    "mcdonalds-coupon": {
      "command": "python",
      "args": ["这里填写 mcd_server.py 的绝对路径"],
      "env": {
        "MCD_MCP_TOKEN": "这里填写你的 token"
      }
    }
  }
}
```

参考 `.codex.json.example` 文件。

## MCP 工具列表

| 工具名称 | 说明 |
|---------|------|
| `query_available_coupons` | 查询麦麦省当前可用的优惠券列表 |
| `auto_claim_coupons` | 一键领取所有可用的优惠券 |
| `query_my_coupons` | 查询我的优惠券列表（已领取） |
| `query_campaign_calendar` | 查询麦当劳活动日历 |
| `get_current_time` | 获取服务器当前时间信息 |

## MCP 资源列表

| 资源 URI | 说明 |
|----------|------|
| `mcdonalds://coupons/available` | 获取可用优惠券（作为资源） |
| `mcdonalds://coupons/mine` | 获取我的优惠券（作为资源） |

## 独立 CLI 工具

项目还包含一个可独立运行的命令行工具 `mcdonalds_coupon.py`：

```bash
python mcdonalds_coupon.py
```

运行后会显示交互式菜单，支持：
1. 查询麦麦省券列表
2. 一键领取优惠券
3. 查询我的优惠券
4. 查询活动日历
5. 获取当前时间
6. 全部执行（查询->领券->查看我的券）

## 项目结构

```
mcdonalds_coupon/
├── mcd_server.py          # MCP 服务器主文件
├── mcdonalds_coupon.py    # 独立 CLI 工具
├── .gitignore
├── .env.example           # 环境变量模板
├── .codex.json.example    # MCP 配置模板
├── README.md
└── .codex/
    └── skills/
        └── mcdonalds-coupon/
            └── SKILL.md   # Skill 定义文件
```

## 许可证

MIT License

## 相关链接

- [FastMCP 文档](https://github.com/jlowin/fastmcp)
- [MCP 协议规范](https://modelcontextprotocol.io/)
