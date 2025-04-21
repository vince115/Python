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
        print("❌ 無法連線到 Blender（port 9876）")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 發生錯誤：{str(e)}")
        sys.exit(1)
    finally:
        client.close()
        time.sleep(0.1)

def main():
    print("🛋️ 建立 KIVIK 雙人沙發（修正版）...")

    # 主體座架（底座）
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.2))")
    send_to_blender("bpy.context.object.name = 'SofaBase'")
    send_to_blender("bpy.context.object.scale = (0.95, 0.475, 0.2)")

    # 椅墊（軟墊）
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.425))")
    send_to_blender("bpy.context.object.name = 'Cushion'")
    send_to_blender("bpy.context.object.scale = (0.9, 0.45, 0.05)")

    # 背靠
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.5, 0.6))")
    send_to_blender("bpy.context.object.name = 'Backrest'")
    send_to_blender("bpy.context.object.scale = (0.95, 0.05, 0.25)")

    # 左扶手（位置向內移動）
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.5, 0, 0.4))")
    send_to_blender("bpy.context.object.name = 'ArmrestLeft'")
    send_to_blender("bpy.context.object.scale = (0.05, 0.45, 0.4)")

    # 右扶手（位置向內移動）
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5, 0, 0.4))")
    send_to_blender("bpy.context.object.name = 'ArmrestRight'")
    send_to_blender("bpy.context.object.scale = (0.05, 0.45, 0.4)")

    # 材質（Tresund 淺米色）
    mat_code = '''
import bpy

mat = bpy.data.materials.new(name="Tresund_Beige")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.9, 0.85, 0.75, 1)

parts = ["SofaBase", "Backrest", "ArmrestLeft", "ArmrestRight", "Cushion"]
for name in parts:
    obj = bpy.data.objects.get(name)
    if obj:
        if len(obj.data.materials):
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
'''

    send_to_blender(mat_code)

    print("✅ 完成：沙發已完整建立！")

if __name__ == "__main__":
    main()
