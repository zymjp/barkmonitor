#!/usr/bin/env python3
import requests
import time
from datetime import datetime

# ========== 仅需修改这1处 ==========
BARK_KEY = "NruGLN4EpLvBoeN8ez62J6"  # 只填密钥，不要加/，比如：abc123456789xyz
# ==================================

MONITOR_URL = "http://10.0.0.108:3001"
CHECK_INTERVAL = 120

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def check_url_availability():
    try:
        response = requests.get(MONITOR_URL, timeout=10, verify=False)
        print(f"{get_current_time()} - URL检测响应码：{response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"{get_current_time()} - URL检测失败：{str(e)}")
        return False

def send_bark_alert():
    if not BARK_KEY:
        print(f"{get_current_time()} - 错误：Bark密钥为空！")
        return
    
    # 清理密钥（去掉首尾空格/多余的/，避免格式错误）
    clean_key = BARK_KEY.strip().rstrip("/")
    # Bark官方POST接口（固定格式）
    bark_api = f"https://api.day.app/{clean_key}"
    
    # 推送内容（JSON格式，避免编码问题）
    alert_data = {
        "title": "服务访问异常",
        "body": f"{get_current_time()} - {MONITOR_URL} 无法正常访问！",
        "sound": "alarm.caf"  # 可选：推送铃声（Bark支持的铃声）
    }
    
    print(f"{get_current_time()} - 推送接口：{bark_api}")
    print(f"{get_current_time()} - 推送内容：{alert_data}")
    
    try:
        # POST请求（推荐方式），设置超时10秒
        resp = requests.post(
            bark_api,
            json=alert_data,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        print(f"{get_current_time()} - Bark响应：{resp.status_code} | {resp.text}")
        
        # 验证推送结果（新版Bark code=0为成功）
        resp_json = resp.json()
        if resp_json.get("code") == 0:
            print(f"{get_current_time()} - Bark推送成功！")
        else:
            print(f"{get_current_time()} - Bark推送失败：{resp_json.get('message', '未知错误')}")
    except Exception as e:
        print(f"{get_current_time()} - Bark推送异常：{str(e)}")

def main():
    print(f"{get_current_time()} - 开始监控 {MONITOR_URL}，间隔{CHECK_INTERVAL}秒")
    last_status = True
    
    # 首次运行强制测试推送（快速验证）
    print(f"{get_current_time()} - 首次运行，测试Bark推送...")
    send_bark_alert()
    
    while True:
        current_status = check_url_availability()
        
        if current_status:
            print(f"{get_current_time()} - {MONITOR_URL} 访问正常：ok")
        else:
            if last_status:
                print(f"{get_current_time()} - 检测到URL异常，触发推送...")
                send_bark_alert()
        
        last_status = current_status
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()