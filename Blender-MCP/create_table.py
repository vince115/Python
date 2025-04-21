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
            print("⚠️ 未收到 MCP 回應")
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
        sys.exit(1)
    finally:
        client.close()
        time.sleep(0.1)

def main():
    print("🏠 建立修正座標後的套房模型...")

    # 地板（5x4m）
    send_to_blender("bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))")
    send_to_blender("bpy.context.object.name = 'Floor'")
    send_to_blender("bpy.context.object.scale = (2.5, 2, 1)")

    # 天花板
    send_to_blender("bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 2.5))")
    send_to_blender("bpy.context.object.name = 'Ceiling'")
    send_to_blender("bpy.context.object.scale = (2.5, 2, 1)")

    # 牆壁
    wall_thickness = 0.05
    walls = [
        ("Wall_Back",    (0, -2.0 + wall_thickness/2, 1.25), (2.5, wall_thickness, 1.25)),
        ("Wall_Front",   (0,  2.0 - wall_thickness/2, 1.25), (2.5, wall_thickness, 1.25)),
        ("Wall_Left",    (-2.5 + wall_thickness/2, 0, 1.25), (wall_thickness, 2, 1.25)),
        ("Wall_Right",   (2.5 - wall_thickness/2,  0, 1.25), (wall_thickness, 2, 1.25)),
    ]
    for name, pos, scale in walls:
        send_to_blender(f"bpy.ops.mesh.primitive_cube_add(size=1, location={pos})")
        send_to_blender(f"bpy.context.object.name = '{name}'")
        send_to_blender(f"bpy.context.object.scale = {scale}")

    # 床（靠左牆擺放）
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(-1.5, -1.2, 0.25))")
    send_to_blender("bpy.context.object.name = 'BedBase'")
    send_to_blender("bpy.context.object.scale = (0.9, 1.2, 0.25)")

    # 書桌（靠右牆）
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(1.6, -1.2, 0.4))")
    send_to_blender("bpy.context.object.name = 'Desk'")
    send_to_blender("bpy.context.object.scale = (0.6, 0.3, 0.4)")

    # 椅子（書桌前）
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(1.6, -0.6, 0.2))")
    send_to_blender("bpy.context.object.name = 'Chair'")
    send_to_blender("bpy.context.object.scale = (0.25, 0.25, 0.2)")

    # 衣櫃（靠近房門前側）
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(-1.6, 1.5, 1.0))")
    send_to_blender("bpy.context.object.name = 'Wardrobe'")
    send_to_blender("bpy.context.object.scale = (0.4, 0.3, 1.0)")

    # 簡易廚房（靠右上角）
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(1.6, 1.5, 0.45))")
    send_to_blender("bpy.context.object.name = 'KitchenUnit'")
    send_to_blender("bpy.context.object.scale = (0.6, 0.3, 0.45)")

    # 浴室隔牆（中央隔出空間）
    send_to_blender("bpy.ops.mesh.primitive_cube_add(size=1, location=(0.0, 0.3, 1.0))")
    send_to_blender("bpy.context.object.name = 'BathroomWall'")
    send_to_blender("bpy.context.object.scale = (0.05, 0.8, 1.0)")

    # 整合為群組 StudioRoom
    send_to_blender('''
import bpy

parent = bpy.data.objects.new("StudioRoom", None)
bpy.context.collection.objects.link(parent)

names = ["Floor", "Ceiling", "Wall_Back", "Wall_Front", "Wall_Left", "Wall_Right",
         "BedBase", "Desk", "Chair", "Wardrobe", "KitchenUnit", "BathroomWall"]

for name in names:
    obj = bpy.data.objects.get(name)
    if obj:
        obj.parent = parent
''')

    print("✅ 完成：套房模型已整合與重新定位！")

if __name__ == "__main__":
    main()
