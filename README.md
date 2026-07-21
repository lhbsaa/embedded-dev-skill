# Embedded Development Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pi Compatible](https://img.shields.io/badge/Pi-Compatible-green.svg)](https://github.com/badlogic/pi-mono)
[![OpenCode Compatible](https://img.shields.io/badge/OpenCode-Compatible-blue.svg)](https://opencode.ai)
[![Version](https://img.shields.io/badge/version-3.3-purple.svg)](https://github.com/lhbsaa/embedded-dev-skill)
[![中文](https://img.shields.io/badge/Lang-中文-blue)](README_ZH.md)

AI-assisted embedded system development skill for **Pi Coding Agent** and **OpenCode** dual platforms.

**v3.3.0 Superpowers Integration**: Iron Law, Skill Chain, two-stage review — inspired by Superpowers' gating mechanisms.

> Also available as part of [apex-unified](https://github.com/lhbsaa/apex-unified) — the unified AI coding agent with embedded-dev mode, zero dependencies, and cross-platform plugin support.

---

## Features

### Core Capabilities
- **Dual Platform**: Pi Coding Agent + OpenCode
- **Multi-chip Support**: ESP32, STM32, RP2040, nRF52 series
- **Hardware Interfaces**: SPI, I2C, UART, GPIO, ADC, PWM configuration templates
- **Communication Protocols**: Wi-Fi, TCP/IP, HTTP, MQTT, BLE, Modbus
- **GUI Visual Feedback**: Camera capture + image analysis
- **Serial Monitoring**: AI-friendly log parsing
- **Real-world Cases**: 6 project case studies
- **FAQ**: 20 quick-answer questions

### v3.3.0 New (Superpowers Integration)
- **Iron Law**: Compile-first verification gate
- **Red Flags**: 12 stop signals + 7 symptom signals
- **Rationalization Table**: 11 excuse-counter tables
- **Verification Gate**: 5-step verification workflow
- **Skill Chain**: 5-stage chain (brainstorming → design → implementation → verification → gui-feedback)
- **Two-stage Review**: Hardware spec review + MISRA C review

---

## Quick Start

### Pi Coding Agent

```bash
git clone https://github.com/lhbsaa/embedded-dev-skill.git
# Copy to Pi's skills directory
cp -r embedded-dev-skill ~/.pi/agent/skills/embedded-dev
```

### OpenCode

```bash
git clone https://github.com/lhbsaa/embedded-dev-skill.git
cp -r embedded-dev-skill .opencode/skills/embedded-dev
```

---

## Skill Structure

```
embedded-dev/
├── skills/           # Core skill files
│   ├── esp32/        # ESP32-specific skills
│   ├── stm32/        # STM32-specific skills
│   ├── common/       # Shared hardware patterns
│   └── ...
├── scripts/          # Automation scripts
├── adapters/         # Platform adapters
├── hooks/            # Git hooks for code quality
├── prompts/          # Prompt templates
├── references/       # Reference materials
├── extensions/       # Platform extensions
└── SKILL.md          # Main skill definition (23KB)
```

---

## Supported Hardware

| Chip Family | Interfaces | Tools |
|-------------|-----------|-------|
| **ESP32-S3** | SPI, I2C, UART, I2S, ADC, PWM, USB OTG | ESP-IDF, PlatformIO, Arduino |
| **ESP32** | SPI, I2C, UART, ADC, DAC, PWM | ESP-IDF, PlatformIO, Arduino |
| **STM32** | SPI, I2C, UART, ADC, PWM, CAN | STM32Cube, HAL, LL |
| **RP2040** | SPI, I2C, UART, PIO, ADC | Pico SDK, Arduino |
| **nRF52** | SPI, I2C, UART, BLE, ADC | nRF5 SDK, Zephyr |

---

## Communication Protocol Templates

| Protocol | Use Case | Example |
|----------|----------|---------|
| **Wi-Fi** | IoT connectivity | ESP32 HTTP client |
| **TCP/IP** | Socket communication | Data streaming |
| **HTTP/HTTPS** | REST API | Web service client |
| **MQTT** | Pub/sub messaging | Sensor data publish |
| **BLE** | Low-power peripheral | Beacon advertising |
| **Modbus** | Industrial control | RTU/ASCII master |

---

## Installation

```bash
git clone https://github.com/lhbsaa/embedded-dev-skill.git
cd embedded-dev-skill

# Pi Coding Agent
cp -r skills ~/.pi/agent/skills/embedded-dev

# OpenCode
cp -r skills .opencode/skills/embedded-dev
```

For detailed installation: see [INSTALL.md](INSTALL.md)

---

## Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| **Pi Coding Agent** | ✅ Full | All 6 skill branches |
| **OpenCode** | ✅ Full | All 6 skill branches |
| **Claude Code** | ⚠️ Partial | Via AGENTS.md |
| **apex-unified** | ✅ Full | embedded-dev mode native |

See [COMPATIBILITY.md](COMPATIBILITY.md) for details.

---

## Version History

| Version | Highlights |
|---------|-----------|
| **v3.3.0** | Superpowers Integration: Iron Law, Skill Chain, two-stage review |
| **v3.2.0** | Dual Platform: Pi + OpenCode |
| **v3.1.0** | Enhanced ESP32 toolchain support |
| **v3.0.0** | Multi-chip architecture |
| **v2.0.0** | Pi Coding Agent integration |
| **v1.0.0** | Initial release |

See [VERSION_HISTORY.md](VERSION_HISTORY.md) for details.

---

## Case Studies

6 real-world embedded projects demonstrating the skill in action:

1. **ESP32-S3 Robot** — Differential drive with ultrasonic obstacle avoidance
2. **STM32 Motor Control** — BLDC FOC with hall sensors
3. **RP2040 MIDI Controller** — USB MIDI with analog controls
4. **nRF52 BLE Sensor** — Low-power environmental monitoring
5. **ESP32 Camera** — AI vision with OV2640
6. **Multi-chip Gateway** — ESP32 + STM32 UART bridge

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for full version history.

---

## License

MIT License. See [LICENSE](LICENSE).
