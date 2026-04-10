/**
 * Build Wrapper Extension for Pi Coding Agent
 * 
 * 统一的嵌入式项目编译命令，支持多种平台：
 * - ESP-IDF (ESP32)
 * - STM32 (Make + OpenOCD)
 * - Pico SDK (RP2040)
 * - PlatformIO (多平台)
 * - Arduino CLI
 * - Zephyr
 * 
 * Installation: Copy to ~/.pi/agent/extensions/build-wrapper.ts
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type, Static } from "@sinclair/typebox";
import { StringEnum } from "@mariozechner/pi-ai";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const BuildActionSchema = StringEnum([
  "detect",      // 检测项目类型
  "build",       // 编译项目
  "flash",       // 烧录固件
  "monitor",     // 串口监控
  "clean",       // 清理构建
  "config",      // 配置操作
  "size",        // 查看大小
  "debug",       // 启动调试
] as const);

type BuildAction = Static<typeof BuildActionSchema>;

interface ProjectInfo {
  type: string;
  name: string;
  target?: string;
  port?: string;
  buildDir: string;
  configFiles: string[];
}

const PROJECT_MARKERS: Record<string, string[]> = {
  "esp-idf": ["CMakeLists.txt", "sdkconfig", "main/"],
  "esp-idf-component": ["CMakeLists.txt", "idf_component.yml"],
  "stm32-cubeide": [".project", ".cproject"],
  "stm32-makefile": ["Makefile", "startup_"],
  "pico-sdk": ["pico_sdk_import.cmake", "pico_sdk.h"],
  "platformio": ["platformio.ini"],
  "arduino": [".ino"],
  "zephyr": ["west.yml", "zephyr/"],
  "nrf5-sdk": ["sdk_config.h", "nrf_drv_"],
};

export default function (pi: ExtensionAPI) {
  // ============================================
  // Tool: embedded_build
  // ============================================
  pi.registerTool({
    name: "embedded_build",
    label: "Embedded Build",
    description: "统一的嵌入式项目编译命令。支持 ESP-IDF, STM32, Pico SDK, PlatformIO, Arduino, Zephyr。",
    promptSnippet: "Build embedded projects with unified interface",
    promptGuidelines: [
      "Use embedded_build for all embedded compilation tasks",
      "First detect project type, then execute build actions",
      "Parse error output to diagnose issues",
    ],
    parameters: Type.Object({
      action: BuildActionSchema,
      target: Type.Optional(Type.String({ description: "目标芯片 (如 esp32s3, stm32f4)" })),
      port: Type.Optional(Type.String({ description: "串口设备 (如 COM3, /dev/ttyUSB0)" })),
      baud: Type.Optional(Type.Number({ description: "波特率", default: 115200 })),
      verbose: Type.Optional(Type.Boolean({ description: "详细输出" })),
      clean: Type.Optional(Type.Boolean({ description: "清理后编译" })),
      config: Type.Optional(Type.String({ description: "配置值 (key=value)" })),
    }),
    async execute(toolCallId, params, signal, onUpdate, ctx) {
      const action = params.action;

      try {
        switch (action) {
          case "detect":
            return await detectProject(ctx);

          case "build":
            return await buildProject(params, ctx, signal, onUpdate);

          case "flash":
            return await flashProject(params, ctx, signal, onUpdate);

          case "monitor":
            return await monitorProject(params, ctx, signal);

          case "clean":
            return await cleanProject(params, ctx, signal);

          case "config":
            return await configProject(params, ctx, signal);

          case "size":
            return await sizeProject(params, ctx, signal);

          case "debug":
            return await debugProject(params, ctx, signal);

          default:
            return {
              content: [{ type: "text", text: `未知操作: ${action}` }],
              isError: true,
            };
        }
      } catch (error: any) {
        return {
          content: [{ type: "text", text: `错误: ${error.message}` }],
          isError: true,
          details: { error: error.message },
        };
      }
    },
  });

  // ============================================
  // Tool: embedded_diagnose
  // ============================================
  pi.registerTool({
    name: "embedded_diagnose",
    label: "Embedded Diagnose",
    description: "分析编译错误并提供修复建议",
    parameters: Type.Object({
      errorOutput: Type.String({ description: "编译错误输出" }),
      maxSuggestions: Type.Optional(Type.Number({ description: "最大建议数", default: 5 })),
    }),
    async execute(toolCallId, params, signal, onUpdate, ctx) {
      const errors = parseBuildErrors(params.errorOutput);
      const suggestions = generateErrorSuggestions(errors);

      let output = `## 编译错误诊断\n\n`;
      output += `发现 ${errors.length} 个错误\n\n`;

      for (const error of errors.slice(0, params.maxSuggestions || 5)) {
        output += `### ${error.file}:${error.line}\n`;
        output += `- **类型**: ${error.severity}\n`;
        output += `- **信息**: ${error.message}\n`;
        if (error.suggestion) {
          output += `- **建议**: ${error.suggestion}\n`;
        }
        output += "\n";
      }

      return {
        content: [{ type: "text", text: output }],
        details: { errors, suggestions, count: errors.length },
      };
    },
  });

  // ============================================
  // Command: /build
  // ============================================
  pi.registerCommand("build", {
    description: "编译当前嵌入式项目",
    getArgumentCompletions: (prefix: string) => {
      const actions = ["detect", "build", "flash", "monitor", "clean", "size"];
      return actions
        .filter((a) => a.startsWith(prefix))
        .map((a) => ({ value: a, label: a }));
    },
    handler: async (args, ctx) => {
      const [action, ...rest] = (args || "build").split(" ");
      
      const result = await buildProject({ action: action as any }, ctx, undefined, undefined);
      ctx.ui.notify(result.content[0]?.text?.substring(0, 100) || "Done", 
        result.isError ? "error" : "success");
    },
  });

  // ============================================
  // Command: /flash
  // ============================================
  pi.registerCommand("flash", {
    description: "烧录固件到目标设备",
    handler: async (args, ctx) => {
      const port = args || await detectSerialPort(ctx);
      if (!port) {
        ctx.ui.notify("未找到串口设备", "warning");
        return;
      }
      ctx.ui.notify(`正在烧录到 ${port}...`, "info");
      const result = await flashProject({ action: "flash", port }, ctx, undefined, undefined);
      ctx.ui.notify(result.isError ? "烧录失败" : "烧录成功", result.isError ? "error" : "success");
    },
  });

  // ============================================
  // Helper Functions
  // ============================================

  async function detectProject(ctx: any): Promise<any> {
    const cwd = ctx.cwd;
    const detected: ProjectInfo[] = [];

    for (const [type, markers] of Object.entries(PROJECT_MARKERS)) {
      const found = markers.filter((m) => {
        const fullPath = join(cwd, m);
        return existsSync(fullPath) || m.endsWith("/") && existsSync(fullPath.slice(0, -1));
      });

      if (found.length >= Math.ceil(markers.length / 2)) {
        detected.push({
          type,
          name: cwd.split("/").pop() || cwd.split("\\").pop() || "unknown",
          buildDir: getBuildDir(type, cwd),
          configFiles: found,
        });
      }
    }

    if (detected.length === 0) {
      return {
        content: [{ type: "text", text: "未检测到已知的嵌入式项目类型" }],
        details: { detected: [], cwd },
      };
    }

    const output = detected
      .map((p) => `- **${p.type}**: ${p.name}\n  配置文件: ${p.configFiles.join(", ")}`)
      .join("\n\n");

    return {
      content: [{ type: "text", text: `## 检测到的项目类型\n\n${output}` }],
      details: { detected, cwd },
    };
  }

  async function buildProject(
    params: any,
    ctx: any,
    signal: any,
    onUpdate: any
  ): Promise<any> {
    const projectInfo = await getProjectInfo(ctx);
    if (!projectInfo) {
      return {
        content: [{ type: "text", text: "无法检测项目类型，请确保在正确的项目目录" }],
        isError: true,
      };
    }

    onUpdate?.({ content: [{ type: "text", text: `正在编译 ${projectInfo.type} 项目...` }] });

    const buildCmd = getBuildCommand(projectInfo.type, params);
    const result = await executeCommand(buildCmd, ctx, signal);

    if (result.success) {
      return {
        content: [
          { type: "text", text: `✅ 编译成功\n\n${result.output.slice(-500)}` },
        ],
        details: { projectInfo, command: buildCmd },
      };
    } else {
      const errors = parseBuildErrors(result.output);
      return {
        content: [
          { type: "text", text: `❌ 编译失败\n\n发现 ${errors.length} 个错误` },
        ],
        isError: true,
        details: { projectInfo, errors, output: result.output },
      };
    }
  }

  async function flashProject(
    params: any,
    ctx: any,
    signal: any,
    onUpdate: any
  ): Promise<any> {
    const projectInfo = await getProjectInfo(ctx);
    if (!projectInfo) {
      return {
        content: [{ type: "text", text: "无法检测项目类型" }],
        isError: true,
      };
    }

    const port = params.port || (await detectSerialPort(ctx));
    if (!port) {
      return {
        content: [{ type: "text", text: "未指定串口设备" }],
        isError: true,
      };
    }

    onUpdate?.({ content: [{ type: "text", text: `正在烧录到 ${port}...` }] });

    const flashCmd = getFlashCommand(projectInfo.type, port, params);
    const result = await executeCommand(flashCmd, ctx, signal);

    return {
      content: [
        {
          type: "text",
          text: result.success
            ? `✅ 烧录成功`
            : `❌ 烧录失败: ${result.output.slice(-200)}`,
        },
      ],
      isError: !result.success,
      details: { projectInfo, port, command: flashCmd },
    };
  }

  async function monitorProject(
    params: any,
    ctx: any,
    signal: any
  ): Promise<any> {
    const projectInfo = await getProjectInfo(ctx);
    const port = params.port || (await detectSerialPort(ctx));
    const baud = params.baud || 115200;

    if (!port) {
      return {
        content: [{ type: "text", text: "未指定串口设备，使用方式: embedded_build action=monitor port=COM3" }],
        isError: true,
      };
    }

    return {
      content: [
        {
          type: "text",
          text: `串口监控命令:\n\n根据平台选择:\n- ESP-IDF: idf.py -p ${port} monitor\n- PlatformIO: pio device monitor -p ${port} -b ${baud}\n- 通用: screen ${port} ${baud} 或 picocom ${port} -b ${baud}`,
        },
      ],
      details: { port, baud, projectType: projectInfo?.type },
    };
  }

  async function cleanProject(
    params: any,
    ctx: any,
    signal: any
  ): Promise<any> {
    const projectInfo = await getProjectInfo(ctx);
    if (!projectInfo) {
      return {
        content: [{ type: "text", text: "无法检测项目类型" }],
        isError: true,
      };
    }

    const cleanCmd = getCleanCommand(projectInfo.type);
    const result = await executeCommand(cleanCmd, ctx, signal);

    return {
      content: [
        { type: "text", text: result.success ? "✅ 清理完成" : `❌ 清理失败: ${result.output}` },
      ],
      isError: !result.success,
    };
  }

  async function configProject(
    params: any,
    ctx: any,
    signal: any
  ): Promise<any> {
    const projectInfo = await getProjectInfo(ctx);
    
    return {
      content: [
        {
          type: "text",
          text: `配置命令:\n\n- ESP-IDF: idf.py menuconfig\n- PlatformIO: 编辑 platformio.ini\n- STM32: 编辑 sdk_config.h 或使用 STM32CubeMX\n- Zephyr: west build -t menuconfig`,
        },
      ],
      details: { projectType: projectInfo?.type },
    };
  }

  async function sizeProject(
    params: any,
    ctx: any,
    signal: any
  ): Promise<any> {
    const projectInfo = await getProjectInfo(ctx);
    if (!projectInfo) {
      return { content: [{ type: "text", text: "无法检测项目类型" }], isError: true };
    }

    const sizeCmd = getSizeCommand(projectInfo.type);
    const result = await executeCommand(sizeCmd, ctx, signal);

    return {
      content: [{ type: "text", text: result.output || "无法获取大小信息" }],
      details: { projectType: projectInfo.type },
    };
  }

  async function debugProject(
    params: any,
    ctx: any,
    signal: any
  ): Promise<any> {
    return {
      content: [
        {
          type: "text",
          text: `调试命令:\n\n- ESP-IDF: idf.py openocd 然后 idf.py gdb\n- STM32: openocd -f board/st_nucleo.cfg\n- PlatformIO: pio debug\n- Pico: picoprobe + openocd`,
        },
      ],
    };
  }

  // ============================================
  // Utility Functions
  // ============================================

  async function getProjectInfo(ctx: any): Promise<ProjectInfo | null> {
    const result = await detectProject(ctx);
    return result.details?.detected?.[0] || null;
  }

  function getBuildDir(type: string, cwd: string): string {
    const dirs: Record<string, string> = {
      "esp-idf": "build",
      "platformio": ".pio/build",
      "stm32-makefile": "build",
      "pico-sdk": "build",
      "zephyr": "build",
    };
    return join(cwd, dirs[type] || "build");
  }

  function getBuildCommand(type: string, params: any): string {
    const cmds: Record<string, string> = {
      "esp-idf": params.clean ? "idf.py fullclean && idf.py build" : "idf.py build",
      "platformio": params.clean ? "pio run -t clean && pio run" : "pio run",
      "stm32-makefile": params.clean ? "make clean && make all" : "make all",
      "pico-sdk": params.clean ? "cd build && make clean && make" : "cd build && make",
      "arduino": `arduino-cli compile --fqbn ${params.target || "esp32:esp32:esp32"} .`,
      "zephyr": params.clean ? "west build -t pristine && west build" : "west build",
    };
    return cmds[type] || "make";
  }

  function getFlashCommand(type: string, port: string, params: any): string {
    const cmds: Record<string, string> = {
      "esp-idf": `idf.py -p ${port} flash`,
      "platformio": `pio run -t upload -p ${port}`,
      "stm32-makefile": `make flash PORT=${port}`,
      "pico-sdk": `picotool load build/*.uf2`,
      "arduino": `arduino-cli upload -p ${port} --fqbn ${params.target || "esp32:esp32:esp32"} .`,
      "zephyr": `west flash`,
    };
    return cmds[type] || "";
  }

  function getCleanCommand(type: string): string {
    const cmds: Record<string, string> = {
      "esp-idf": "idf.py fullclean",
      "platformio": "pio run -t clean",
      "stm32-makefile": "make clean",
      "pico-sdk": "cd build && make clean",
      "zephyr": "west build -t pristine",
    };
    return cmds[type] || "make clean";
  }

  function getSizeCommand(type: string): string {
    const cmds: Record<string, string> = {
      "esp-idf": "idf.py size",
      "platformio": "pio run -t sizedata",
      "stm32-makefile": "arm-none-eabi-size build/*.elf",
      "pico-sdk": "arm-none-eabi-size build/*.elf",
    };
    return cmds[type] || "";
  }

  async function detectSerialPort(ctx: any): Promise<string | null> {
    const isWindows = process.platform === "win32";
    const listCmd = isWindows
      ? "mode"
      : "ls /dev/ttyUSB* /dev/ttyACM* /dev/cu.usb* 2>/dev/null";

    try {
      const result = await pi.exec("sh", ["-c", listCmd]);
      if (result.stdout) {
        if (isWindows) {
          const match = result.stdout.match(/COM\d+/);
          return match ? match[0] : null;
        } else {
          const ports = result.stdout.split("\n").filter((p: string) => p);
          return ports[0] || null;
        }
      }
    } catch {}

    return null;
  }

  async function executeCommand(cmd: string, ctx: any, signal: any): Promise<any> {
    try {
      const result = await pi.exec("sh", ["-c", cmd], { signal, cwd: ctx.cwd });
      return {
        success: result.code === 0,
        output: result.stdout + result.stderr,
      };
    } catch (error: any) {
      return {
        success: false,
        output: error.message,
      };
    }
  }

  function parseBuildErrors(output: string): any[] {
    const errors: any[] = [];
    const patterns = [
      /^([^:]+):(\d+):(\d+):\s+(error|warning):\s+(.+)$/gm,
      /^([^:]+):(\d+):\s+(error|warning):\s+(.+)$/gm,
      /^fatal error:\s+(.+)$/gm,
    ];

    for (const pattern of patterns) {
      let match;
      while ((match = pattern.exec(output)) !== null) {
        errors.push({
          file: match[1] || "unknown",
          line: parseInt(match[2]) || 0,
          column: parseInt(match[3]) || 0,
          severity: match[4] || "error",
          message: match[5] || match[1] || "",
          suggestion: getSuggestion(match[5] || match[1] || ""),
        });
      }
    }

    return errors;
  }

  function generateErrorSuggestions(errors: any[]): any[] {
    return errors.map((e) => ({
      file: e.file,
      line: e.line,
      suggestion: e.suggestion,
    }));
  }

  function getSuggestion(message: string): string {
    const suggestions: Record<string, string> = {
      "undeclared": "检查变量是否已声明，或添加 #include",
      "undefined reference": "检查链接库是否正确添加",
      "cannot find": "检查文件路径或安装依赖",
      "multiple definition": "检查是否有重复定义或缺少 include guard",
      "implicit declaration": "添加函数声明或 #include",
      "incompatible pointer": "检查指针类型是否匹配",
    };

    for (const [key, value] of Object.entries(suggestions)) {
      if (message.toLowerCase().includes(key)) {
        return value;
      }
    }

    return "查看错误信息并检查相关代码";
  }

  // Session start notification
  pi.on("session_start", async (_event, ctx) => {
    ctx.ui.notify("Build Wrapper extension loaded", "info");
  });
}
