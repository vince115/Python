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
            response = client.recv(4096).decode('utf-8')
            print("✅ MCP 回應：", response)
        except socket.timeout:
            print("⚠️ 未收到 MCP 回應")
        return True

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
        return False
    finally:
        client.close()
        time.sleep(0.1)

def main():
    print("🚀 正在建立套房室內設計場景...")

    cmds = [
        # 清空場景
        "import bpy; bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()",

        # 地板
        "bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))",
        "bpy.context.object.name = 'Floor'",
        "bpy.context.object.scale = (6.0, 8.0, 1)",

        # 背牆
        "bpy.ops.mesh.primitive_cube_add(location=(0, -4.0, 1.4))",
        "bpy.context.object.name = 'BackWall'",
        "bpy.context.object.scale = (6.0, 0.1, 1.4)",

        # 左牆
        "bpy.ops.mesh.primitive_cube_add(location=(-3.0, 0, 1.4))",
        "bpy.context.object.name = 'LeftWall'",
        "bpy.context.object.scale = (0.1, 8.0, 1.4)",

        # 右牆
        "bpy.ops.mesh.primitive_cube_add(location=(3.0, 0, 1.4))",
        "bpy.context.object.name = 'RightWall'",
        "bpy.context.object.scale = (0.1, 8.0, 1.4)",

        # 前牆左
        "bpy.ops.mesh.primitive_cube_add(location=(-1.5, 4.0, 1.4))",
        "bpy.context.object.name = 'FrontWall_Left'",
        "bpy.context.object.scale = (1.5, 0.1, 1.4)",

        # 前牆右
        "bpy.ops.mesh.primitive_cube_add(location=(1.5, 4.0, 1.4))",
        "bpy.context.object.name = 'FrontWall_Right'",
        "bpy.context.object.scale = (1.5, 0.1, 1.4)",

        # 門框上方
        "bpy.ops.mesh.primitive_cube_add(location=(0, 4.0, 2.6))",
        "bpy.context.object.name = 'Door_Top'",
        "bpy.context.object.scale = (1.2, 0.1, 0.2)",

        # 地板材質
        '''mat = bpy.data.materials.new(name="FloorMat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
bpy.data.objects["Floor"].data.materials.append(mat)''',

        # 增加一張床（基座）
        "bpy.ops.mesh.primitive_cube_add(location=(-1.8, -2.5, 0.3))",
        "bpy.context.object.name = 'Bed'",
        "bpy.context.object.scale = (1.0, 2.0, 0.3)",

        # 增加桌子
        "bpy.ops.mesh.primitive_cube_add(location=(2.2, -2.5, 0.4))",
        "bpy.context.object.name = 'Desk'",
        "bpy.context.object.scale = (0.8, 0.6, 0.4)",

        # 增加椅子
        "bpy.ops.mesh.primitive_cube_add(location=(2.2, -1.5, 0.25))",
        "bpy.context.object.name = 'Chair'",
        "bpy.context.object.scale = (0.4, 0.4, 0.25)",

        # 增加窗戶
        "bpy.ops.mesh.primitive_cube_add(location=(-2.95, 0, 1.5))",
        "bpy.context.object.name = 'Window_Frame'",
        "bpy.context.object.scale = (0.05, 1.5, 0.8)",

        # 增加攝影機
        "bpy.ops.object.camera_add(location=(0, -10, 1.7))",
        "bpy.context.object.name = 'Camera'",
        "bpy.context.scene.camera = bpy.context.object",
        "bpy.context.object.rotation_euler = (1.4, 0, 0)",

        # 增加燈光
        "bpy.ops.object.light_add(type='AREA', location=(0, 0, 2.6))",
        "bpy.context.object.name = 'MainLight'",
        "bpy.context.object.data.energy = 500",
        "bpy.context.object.data.size = 2.0"
    ]

    for cmd in cmds:
        send_to_blender(cmd)

    print("✅ 套房設計指令全部傳送完成！請至 Blender 查看結果。")

if __name__ == "__main__":
    main()
