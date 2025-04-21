import socket
import json
import time
import sys

def send_to_blender(code):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 9876))

        command = {
            "type": "execute_code",
            "params": {
                "code": code
            }
        }

        client.send(json.dumps(command).encode('utf-8'))

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
    print("🛠️ 建立 LINNMON / ADILS 桌子 (100x60 cm)...")

    # 桌面尺寸：100x60x3.5 公分 = 1.0 x 0.6 x 0.035 公尺
    table_top_cmd = "bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.735))"
    send_to_blender(table_top_cmd)
    send_to_blender("bpy.context.object.name = 'TableTop'")
    send_to_blender("bpy.context.object.scale = (1.0, 0.6, 0.035)")

    # 桌腳尺寸：直徑 4 公分，高度 70 公分 => 半徑 0.02 公尺，高 0.7 公尺
    leg_height = 0.7
    leg_radius = 0.02
    leg_offset_x = 0.45
    leg_offset_y = 0.25

    leg_positions = [
        ( leg_offset_x,  leg_offset_y, leg_height / 2),
        (-leg_offset_x,  leg_offset_y, leg_height / 2),
        ( leg_offset_x, -leg_offset_y, leg_height / 2),
        (-leg_offset_x, -leg_offset_y, leg_height / 2),
    ]

    for i, pos in enumerate(leg_positions):
        print(f"▶ 建立第 {i+1} 支桌腳")
        leg_cmd = (
            f"bpy.ops.mesh.primitive_cylinder_add(radius={leg_radius}, depth={leg_height}, location={pos})"
        )
        send_to_blender(leg_cmd)
        send_to_blender(f"bpy.context.object.name = 'Leg_{i+1}'")

    print("✅ 完成：LINNMON / ADILS 桌子建立成功！")

if __name__ == "__main__":
    main()
