import ipaddress
import sys

def generate_nginx_config(ip_lines):
    ipv4_list = []
    ipv6_list = []

    for line in ip_lines:
        line = line.strip()
        if not line:
            continue
        try:
            ip = ipaddress.ip_network(line, strict=False)
            if ip.version == 4:
                ipv4_list.append(line)
            else:
                ipv6_list.append(line)
        except ValueError:
            # 忽略无效的 IP 格式
            continue

    output = []
    output.append("           # ==========================================================")
    output.append("           # ESA / CDN 真实 IP 识别配置开始")
    output.append("           # ==========================================================")
    output.append("")
    
    if ipv4_list:
        output.append("           # 信任的 ESA IPv4 回源段")
        for ip in ipv4_list:
            output.append(f"           set_real_ip_from {ip};")
        output.append("")

    if ipv6_list:
        output.append("           # 信任的 ESA IPv6 回源段")
        for ip in ipv6_list:
            output.append(f"           set_real_ip_from {ip};")
        output.append("")

    output.append("           # 告诉 Nginx 真实访客 IP 存在哪个 Header 中")
    output.append("           # ESA 默认会将真实 IP 放在 X-Forwarded-For 的最左侧")
    output.append("           real_ip_header X-Forwarded-For;")
    output.append("")
    output.append("           # 开启递归解析，排除掉 set_real_ip_from 中定义的信任 IP，剩下的最后一个就是真实访客 IP")
    output.append("           real_ip_recursive on;")
    output.append("")
    output.append("           # ==========================================================")
    output.append("           # ESA / CDN 真实 IP 识别配置结束")
    output.append("           # ==========================================================")

    return "
".join(output)

if __name__ == "__main__":
    print("请输入 ESA 回源地址列表（一行一个，输入完成后 Windows 按 Ctrl+Z 并在回车结束，Linux 按 Ctrl+D）:")
    input_data = sys.stdin.read().splitlines()
    
    if not input_data:
        print("未检测到输入内容。")
    else:
        nginx_config = generate_nginx_config(input_data)
        print("
--- 生成的 Nginx 配置如下 ---
")
        print(nginx_config)
        
        with open("nginx_esa_config.conf", "w", encoding="utf-8") as f:
            f.write(nginx_config)
        print("
--- 配置已保存至 nginx_esa_config.conf ---")
