# AI Serial Monitor for PowerShell
# Version: 1.0
# Usage: .\serial_monitor.ps1 -Port COM4 [-BaudRate 115200] [-Duration 10]

param(
    [string]$Port = "COM4",
    [int]$BaudRate = 115200,
    [int]$Duration = 10,
    [string]$OutputFile = "",
    [switch]$ListPorts,
    [switch]$Continuous
)

# 列出所有串口
if ($ListPorts) {
    $ports = [System.IO.Ports.SerialPort]::GetPortNames()
    Write-Host "可用串口列表:" -ForegroundColor Green
    $ports | ForEach-Object { Write-Host "  - $_" }
    return
}

# 创建串口对象
$serial = New-Object System.IO.Ports.SerialPort
$serial.PortName = $Port
$serial.BaudRate = $BaudRate
$serial.Parity = "None"
$serial.DataBits = 8
$serial.StopBits = "One"
$serial.ReadTimeout = 1000
$serial.WriteTimeout = 1000

try {
    # 打开串口
    $serial.Open()
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "AI串口监控工具 v1.0" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "端口: $Port" -ForegroundColor Yellow
    Write-Host "波特率: $BaudRate" -ForegroundColor Yellow
    Write-Host "监控时长: $Duration 秒" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    # 收集数据
    $startTime = Get-Date
    $output = @()
    $lineCount = 0
    
    # 读取循环
    while (((Get-Date) - $startTime).TotalSeconds -lt $Duration) {
        try {
            $data = $serial.ReadLine()
            $timestamp = Get-Date -Format "HH:mm:ss.fff"
            $logLine = "[$timestamp] $data"
            
            # 输出到控制台
            Write-Host $logLine
            
            # 添加到结果
            $output += $logLine
            $lineCount++
        }
        catch {
            # 超时继续
        }
        
        # 连续模式
        if ($Continuous) {
            $startTime = Get-Date
        }
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "监控结束" -ForegroundColor Green
    Write-Host "总读取行数: $lineCount" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    
    # 保存到文件
    if ($OutputFile -ne "") {
        $output | Out-File -FilePath $OutputFile -Encoding UTF8
        Write-Host "数据已保存到: $OutputFile" -ForegroundColor Green
    }
    
    # 返回JSON格式结果
    $result = @{
        success = $true
        port = $Port
        baudrate = $BaudRate
        duration = $Duration
        lines_count = $lineCount
        data = $output
    }
    
    Write-Host ""
    Write-Host "JSON输出:" -ForegroundColor Magenta
    $result | ConvertTo-Json -Depth 3
}
catch {
    Write-Host "错误: $_" -ForegroundColor Red
    $result = @{
        success = $false
        error = $_.Exception.Message
    }
    $result | ConvertTo-Json
}
finally {
    # 关闭串口
    if ($serial.IsOpen) {
        $serial.Close()
        Write-Host ""
        Write-Host "串口已关闭" -ForegroundColor Green
    }
}