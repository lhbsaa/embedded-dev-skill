@echo off
REM Embedded-dev SessionStart Hook for Windows
REM Injects embedded development context at session start

setlocal enabledelayedexpansion

REM Get plugin root from environment
set PLUGIN_ROOT=%~dp0..
set PLUGIN_ROOT=%PLUGIN_ROOT:~0,-1%

REM Check for AGENTS.md
set AGENTS_WARNING=
if not exist "AGENTS.md" (
    set AGENTS_WARNING=\n\n<important-reminder>No AGENTS.md found in project root. Consider creating one with hardware configuration before starting development.</important-reminder>
)

REM Build session context
set SESSION_CONTEXT=<EXTREMELY_IMPORTANT>\nEmbedded Development Session Active.\n\n**Core Constraints:**\n- DMA buffer <= 4092 bytes on ESP32-S3\n- Always verify: build -> flash -> monitor\n- Use camera_capture for GUI verification\n- Read datasheet before hardware config changes\n\n**Iron Law:** NO CODE WITHOUT BUILD-FIRST VERIFICATION.\n\n**Workflow:** Compile-Flash-Monitor-Test loop is mandatory.\n%AGENTS_WARNING%\n</EXTREMELY_IMPORTANT>

REM Escape for JSON (basic escaping)
set SESSION_CONTEXT=%SESSION_CONTEXT:"=\"%
set SESSION_CONTEXT=%SESSION_CONTEXT:\=\\%
set SESSION_CONTEXT=%SESSION_CONTEXT:&=\u0026%

REM Output based on platform
REM Claude Code expects hookSpecificOutput format
REM OpenCode and others expect additionalContext format

if defined CLAUDE_PLUGIN_ROOT (
    echo {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "%SESSION_CONTEXT%"}}
) else (
    echo {"additionalContext": "%SESSION_CONTEXT%"}
)

exit /b 0