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
            "params": {"code": code}
        }
        client.send(json.dumps(command).encode('utf-8'))

        try:
            response = client.recv(1024).decode('utf-8')
            print("✅ MCP 回應：", response)
        except socket.timeout:
            print("⚠️ 警告：未收到 MCP 回應")
    except ConnectionRefusedError:
        print("❌ Blender 無法連線（請確認 MCP 插件與 port）")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 發生錯誤：{str(e)}")
        sys.exit(1)
    finally:
        client.close()
        time.sleep(0.1)

def main():
    print("🗄️ 建立 PLATSA 抽屜櫃（60x57x53 cm）...")

    # 主體櫃身：60x57x53 cm = 0.6 x 0.57 x 0.53 m
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.265))")
    send_to_blender("bpy.context.object.name = 'CabinetBody'")
    send_to_blender("bpy.context.object.scale = (0.3, 0.285, 0.265)")

    # 上抽屜
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.01, 0.365))")
    send_to_blender("bpy.context.object.name = 'DrawerTop'")
    send_to_blender("bpy.context.object.scale = (0.29, 0.01, 0.11)")

    # 下抽屜
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.01, 0.165))")
    send_to_blender("bpy.context.object.name = 'DrawerBottom'")
    send_to_blender("bpy.context.object.scale = (0.29, 0.01, 0.11)")

    # 四個腳座
    foot_positions = [
        ( 0.23,  0.23, 0.05),
        (-0.23,  0.23, 0.05),
        ( 0.23, -0.23, 0.05),
        (-0.23, -0.23, 0.05),
    ]
    for i, pos in enumerate(foot_positions):
        send_to_blender(f"bpy.ops.mesh.primitive_cube_add(size=1, location={pos})")
        send_to_blender(f"bpy.context.object.name = 'Foot_{i+1}'")
        send_to_blender("bpy.context.object.scale = (0.035, 0.035, 0.05)")

    # 加入白色材質
    material_code = '''
import bpy

mat = bpy.data.materials.new(name="WhiteMat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.95, 0.95, 0.95, 1)

for obj_name in ["CabinetBody", "DrawerTop", "DrawerBottom"] + [f"Foot_{i}" for i in range(1, 5)]:
    obj = bpy.data.objects.get(obj_name)
    if obj:
        if len(obj.data.materials):
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
    '''

    send_to_blender(material_code)

    print("✅ 完成：PLATSA 抽屜櫃建立成功！")

if __name__ == "__main__":
    main()
