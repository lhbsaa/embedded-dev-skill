#!/usr/bin/env python3
"""
Embedded Development MCP Server for OpenCode

Provides unified embedded development tools via MCP protocol:
- embedded_build: Unified build/flash/monitor commands
- embedded_diagnose: Compile error analysis and suggestions

Installation:
  pip install mcp pyserial
  cp mcp-server-embedded.py ~/.opencode/mcp/

Configuration (opencode.json):
  {
    "mcpServers": {
      "embedded-dev": {
        "command": "python",
        "args": ["~/.opencode/mcp/mcp-server-embedded.py"]
      }
    }
  }
"""

import asyncio
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent, ImageContent
except ImportError:
    print("Error: mcp package not installed. Run: pip install mcp")
    sys.exit(1)


app = Server("embedded-dev-mcp")


PROJECT_MARKERS: Dict[str, List[str]] = {
    "esp-idf": ["CMakeLists.txt", "sdkconfig", "main/"],
    "esp-idf-component": ["CMakeLists.txt", "idf_component.yml"],
    "stm32-cubeide": [".project", ".cproject"],
    "stm32-makefile": ["Makefile", "startup_"],
    "pico-sdk": ["pico_sdk_import.cmake", "pico_sdk.h"],
    "platformio": ["platformio.ini"],
    "arduino": [".ino"],
    "zephyr": ["west.yml", "zephyr/"],
    "nrf5-sdk": ["sdk_config.h", "nrf_drv_"],
}

BUILD_COMMANDS: Dict[str, Dict[str, str]] = {
    "esp-idf": {
        "build": "idf.py build",
        "flash": "idf.py -p {port} flash",
        "monitor": "idf.py -p {port} monitor",
        "clean": "idf.py fullclean",
        "size": "idf.py size",
        "config": "idf.py menuconfig",
    },
    "platformio": {
        "build": "pio run",
        "flash": "pio run -t upload -p {port}",
        "monitor": "pio device monitor -p {port} -b {baud}",
        "clean": "pio run -t clean",
        "size": "pio run -t sizedata",
    },
    "stm32-makefile": {
        "build": "make all",
        "flash": "make flash PORT={port}",
        "monitor": "",
        "clean": "make clean",
        "size": "arm-none-eabi-size build/*.elf",
    },
    "pico-sdk": {
        "build": "cd build && make",
        "flash": "picotool load build/*.uf2",
        "monitor": "",
        "clean": "cd build && make clean",
        "size": "arm-none-eabi-size build/*.elf",
    },
    "arduino": {
        "build": "arduino-cli compile --fqbn {fqbn} .",
        "flash": "arduino-cli upload -p {port} --fqbn {fqbn} .",
        "monitor": "",
        "clean": "",
        "size": "",
    },
    "zephyr": {
        "build": "west build",
        "flash": "west flash",
        "monitor": "",
        "clean": "west build -t pristine",
        "size": "",
    },
}

ERROR_SUGGESTIONS: Dict[str, str] = {
    "undeclared": "检查变量是否已声明，或添加 #include",
    "undefined reference": "检查链接库是否正确添加，确认 CMakeLists.txt 包含源文件",
    "cannot find": "检查文件路径或安装依赖",
    "multiple definition": "检查是否有重复定义或缺少 include guard",
    "implicit declaration": "添加函数声明或 #include",
    "incompatible pointer": "检查指针类型是否匹配",
    "format": "使用正确的格式说明符 (%lu, PRIu32 等)",
    "overflow": "检查缓冲区大小或数组边界",
    "section .text": "代码段超出容量，使用 Flash 存储常量或优化大小",
}


def detect_project_type(cwd: str) -> Optional[Dict[str, Any]]:
    for project_type, markers in PROJECT_MARKERS.items():
        found = []
        for marker in markers:
            path = Path(cwd) / marker
            if marker.endswith("/"):
                path = Path(cwd) / marker.rstrip("/")
            if path.exists():
                found.append(marker)
        
        if len(found) >= len(markers) / 2:
            return {
                "type": project_type,
                "markers": found,
                "cwd": cwd,
            }
    return None


def get_build_command(project_type: str, action: str, **kwargs) -> str:
    commands = BUILD_COMMANDS.get(project_type, {})
    cmd = commands.get(action, "")
    
    if cmd:
        cmd = cmd.replace("{port}", kwargs.get("port", "COM3"))
        cmd = cmd.replace("{baud}", str(kwargs.get("baud", 115200)))
        cmd = cmd.replace("{fqbn}", kwargs.get("fqbn", "esp32:esp32:esp32s3"))
    
    return cmd


def parse_build_errors(output: str) -> List[Dict[str, Any]]:
    errors = []
    patterns = [
        r'^([^:]+):(\d+):(\d+):\s+(error|warning):\s+(.+)$',
        r'^([^:]+):(\d+):\s+(error|warning):\s+(.+)$',
        r'^fatal error:\s+(.+)$',
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, output, re.MULTILINE):
            groups = match.groups()
            if len(groups) == 5:
                errors.append({
                    "file": groups[0],
                    "line": int(groups[1]),
                    "column": int(groups[2]),
                    "severity": groups[3],
                    "message": groups[4],
                })
            elif len(groups) == 4:
                errors.append({
                    "file": groups[0],
                    "line": int(groups[1]),
                    "severity": groups[2],
                    "message": groups[3],
                })
            elif len(groups) == 1:
                errors.append({
                    "file": "unknown",
                    "line": 0,
                    "severity": "error",
                    "message": groups[0],
                })
    
    return errors


def get_suggestion(message: str) -> str:
    message_lower = message.lower()
    for key, suggestion in ERROR_SUGGESTIONS.items():
        if key in message_lower:
            return suggestion
    return "查看错误信息并检查相关代码"


def run_command(cmd: str, cwd: str, timeout: int = 120) -> Dict[str, Any]:
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout + result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "Command timed out",
            "returncode": -1,
        }
    except Exception as e:
        return {
            "success": False,
            "output": str(e),
            "returncode": -1,
        }


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="embedded_build",
            description="统一嵌入式项目编译命令。支持 ESP-IDF, STM32, Pico SDK, PlatformIO, Arduino, Zephyr。动作: detect, build, flash, monitor, clean, size, config。",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["detect", "build", "flash", "monitor", "clean", "size", "config"],
                        "description": "执行的动作",
                    },
                    "port": {
                        "type": "string",
                        "description": "串口设备 (如 COM3, /dev/ttyUSB0)",
                    },
                    "baud": {
                        "type": "number",
                        "description": "波特率",
                        "default": 115200,
                    },
                    "fqbn": {
                        "type": "string",
                        "description": "Arduino FQBN (如 esp32:esp32:esp32s3)",
                    },
                    "verbose": {
                        "type": "boolean",
                        "description": "详细输出",
                        "default": False,
                    },
                    "clean": {
                        "type": "boolean",
                        "description": "清理后编译",
                        "default": False,
                    },
                },
                "required": ["action"],
            },
        ),
        Tool(
            name="embedded_diagnose",
            description="分析编译错误并提供修复建议",
            inputSchema={
                "type": "object",
                "properties": {
                    "errorOutput": {
                        "type": "string",
                        "description": "编译错误输出",
                    },
                    "maxSuggestions": {
                        "type": "number",
                        "description": "最大建议数",
                        "default": 5,
                    },
                },
                "required": ["errorOutput"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[Any]:
    cwd = os.getcwd()
    
    if name == "embedded_build":
        action = arguments.get("action", "build")
        
        if action == "detect":
            project = detect_project_type(cwd)
            if project:
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({
                            "success": True,
                            "project": project,
                        }, indent=2),
                    )
                ]
            else:
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({
                            "success": False,
                            "error": "未检测到已知的嵌入式项目类型",
                            "cwd": cwd,
                        }, indent=2),
                    )
                ]
        
        project = detect_project_type(cwd)
        if not project:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": "未检测到已知的嵌入式项目类型",
                    }, indent=2),
                )
            ]
        
        project_type = project["type"]
        
        if action == "clean" and arguments.get("clean"):
            clean_cmd = get_build_command(project_type, "clean")
            if clean_cmd:
                run_command(clean_cmd, cwd)
        
        if action == "config":
            config_cmd = get_build_command(project_type, "config")
            return [
                TextContent(
                    type="text",
                    text=f"配置命令:\n{config_cmd}\n请在终端手动执行",
                )
            ]
        
        cmd = get_build_command(
            project_type,
            action,
            port=arguments.get("port", "COM3"),
            baud=arguments.get("baud", 115200),
            fqbn=arguments.get("fqbn", "esp32:esp32:esp32s3"),
        )
        
        if not cmd:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": f"平台 {project_type} 不支持动作 {action}",
                    }, indent=2),
                )
            ]
        
        result = run_command(cmd, cwd)
        
        if result["success"]:
            return [
                TextContent(
                    type="text",
                    text=f"✅ {action} 成功\n{result['output'][-500:]}",
                )
            ]
        else:
            errors = parse_build_errors(result["output"])
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "errors": errors[:arguments.get("maxSuggestions", 5)],
                        "output": result["output"][-1000:],
                    }, indent=2),
                )
            ]
    
    elif name == "embedded_diagnose":
        error_output = arguments.get("errorOutput", "")
        max_suggestions = arguments.get("maxSuggestions", 5)
        
        errors = parse_build_errors(error_output)
        
        diagnosed = []
        for error in errors[:max_suggestions]:
            error["suggestion"] = get_suggestion(error["message"])
            diagnosed.append(error)
        
        return [
            TextContent(
                type="text",
                text=json.dumps({
                    "success": True,
                    "errorCount": len(errors),
                    "diagnosed": diagnosed,
                }, indent=2),
            )
        ]
    
    return [
        TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": f"未知工具: {name}",
            }, indent=2),
        )
    ]


async def main():
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())