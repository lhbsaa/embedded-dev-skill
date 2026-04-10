# Contributing to Embedded Development Skill

感谢您有兴趣为本项目做出贡献！

## 如何贡献

### 报告问题

如果您发现了 bug 或有功能建议：

1. 检查 [Issues](https://github.com/lhbsaa/embedded-dev-skill/issues) 是否已有相关问题
2. 如果没有，创建新 Issue，包含：
   - 清晰的标题和描述
   - 复现步骤（如果是 bug）
   - 预期行为和实际行为
   - 环境信息（芯片型号、框架版本等）

### 提交代码

1. **Fork 仓库**

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-fix-name
   ```

3. **进行更改**
   - 遵循现有代码风格
   - 添加必要的文档
   - 测试您的更改

4. **提交更改**
   ```bash
   git commit -m "描述您的更改"
   ```

5. **推送到 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **创建 Pull Request**
   - 描述您的更改
   - 关联相关 Issue
   - 等待审核

## 开发指南

### 代码风格

**TypeScript 扩展**
- 使用 TypeScript 编写
- 遵循 Pi 扩展 API 规范
- 添加适当的类型注释

**Markdown 文档**
- 使用标准 Markdown 格式
- 表格使用 GitHub 风格
- 代码块指定语言

**Python 脚本**
- 使用 Python 3.8+ 语法
- 添加 docstring
- 遵循 PEP 8 风格

### 目录结构

```
embedded-dev/
├── SKILL.md            # 核心 Skill 定义
├── extensions/         # TypeScript 扩展
├── references/         # 参考文档
└── scripts/            # Python 辅助脚本
```

### 添加新芯片支持

1. 在 `references/chips.md` 添加芯片规格
2. 在 `references/hardware-interfaces.md` 添加接口配置
3. 更新 `SKILL.md` 的支持列表

### 添加新扩展

1. 在 `extensions/` 创建新 `.ts` 文件
2. 遵循 Pi 扩展 API
3. 更新 `SKILL.md` 的工具列表
4. 更新 `README.md`

## 测试

### 测试 Skill

```bash
# 启动 Pi
pi

# 重新加载
/reload

# 测试嵌入式相关问题
"ESP32-S3 如何配置 SPI"
```

### 测试扩展

```bash
# 测试 image_read
image_read test.png

# 测试 todo_list
todo_list action=add "Test task"
todo_list action=list
```

### 测试 Python 脚本

```bash
# 测试摄像头捕获
python scripts/camera_capture.py --list

# 测试图像对比
python scripts/image_compare.py --before img1.png --after img2.png
```

## 版本发布

版本号遵循 [语义化版本](https://semver.org/)：

- **主版本号**: 不兼容的 API 更改
- **次版本号**: 向后兼容的功能新增
- **修订号**: 向后兼容的问题修复

## 行为准则

- 尊重所有贡献者
- 保持建设性讨论
- 专注于改进项目

## 联系方式

- GitHub Issues: https://github.com/lhbsaa/embedded-dev-skill/issues
- GitHub: [@lhbsaa](https://github.com/lhbsaa)

---

再次感谢您的贡献！
