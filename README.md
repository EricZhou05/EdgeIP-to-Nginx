# EdgeIP-to-Nginx

这是一个用于将 ESA (Edge Service Accelerator) 回源 IP 列表转换为 Nginx `real_ip` 配置的 Python 脚本。

## 功能
- 自动识别并区分 IPv4 和 IPv6 地址。
- 生成符合 Nginx 规范的 `set_real_ip_from` 配置。
- 自动配置 `real_ip_header X-Forwarded-For` 和 `real_ip_recursive on`。
- 支持批量粘贴输入。

## 使用方法

### 1. 环境准备
确保你已安装 Python 3，并使用自带的虚拟环境：
```powershell
# 创建虚拟环境（如已创建可跳过）
python -m venv .venv

# 运行脚本
.venv\Scripts\python.exe convert_ips.py
```

### 2. 操作步骤
1. 运行脚本后，将 ESA 控制台获取的 IP 列表直接粘贴到命令行。
2. Windows 用户按 `Ctrl + Z` 再按 `回车` 提交输入。
3. 脚本将生成配置并在当前目录创建 `nginx_esa_config.conf` 文件。

## Nginx 配置示例
生成的配置可以直接放入 `http`, `server` 或 `location` 段落中。

```nginx
# ESA / CDN 真实 IP 识别配置
set_real_ip_from 103.21.244.0/22;
...
real_ip_header X-Forwarded-For;
real_ip_recursive on;
```
