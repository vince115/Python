import socket
import json
import time
import sys

def send_to_blender(code):
    try:
        # 建立 socket 連線
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 9876))

        # 建立 JSON 指令格式
        command = {
            "type": "execute_code",
            "params": {
                "code": code
            }
        }

        # 傳送指令
        client.send(json.dumps(command).encode('utf-8'))

        # 接收回應
        try:
            response = client.recv(1024).decode('utf-8')
            print("✅ MCP 回應：", response)
        except socket.timeout:
            print("⚠️ 警告：未收到 MCP 回應，但指令可能已執行")

    except ConnectionRefusedError:
        print("❌ 錯誤：無法連接到 Blender，請確認：")
        print("1. Blender 是否已啟動")
        print("2. MCP 插件是否已啟用")
        print("3. Port 9876 是否正確")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 錯誤：{str(e)}")
        sys.exit(1)
    finally:
        client.close()
        time.sleep(0.1)

def main():
    print("🚀 開始建立球體...")
    
    # 建立三顆球體的位置設定
    sphere_positions = [
        (0, 0, 0),
        (2, 0, 0),
        (-2, 0, 0)
    ]

    # 建立並發送指令
    for i, pos in enumerate(sphere_positions):
        cmd = f"bpy.ops.mesh.primitive_uv_sphere_add(location={pos})"
        print(f"▶ 發送第 {i+1} 顆球體指令 - 位置：{pos}")
        send_to_blender(cmd)

    print("✅ 完成：已成功建立三個球體！")

if __name__ == "__main__":
    main()
