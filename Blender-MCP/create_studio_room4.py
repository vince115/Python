#!/usr/bin/env python3
"""
豪華大床房生成器 (Socket 版本)
根據平面圖生成44平方米豪華大床房
"""

import socket
import json
import time
import sys

def send_to_blender(code):
    """發送指令到 Blender"""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 9876))
        command = {"type": "execute_code", "params": {"code": code}}
        client.send(json.dumps(command).encode('utf-8'))
        try:
            response = client.recv(1024).decode('utf-8')
            print("✅ 已執行")
        except socket.timeout:
            print("⚠️ 無回應，但指令可能已執行")
    except Exception as e:
        print(f"❌ 錯誤：{str(e)}")
        sys.exit(1)
    finally:
        client.close()
        time.sleep(0.2)

def main():
    print("🏨 開始生成豪華大床房...")

    # 清除場景
    send_to_blender("""
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
""")

    # 設置渲染引擎
    send_to_blender("""
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.cycles.samples = 256
""")

    # 創建地板（根據平面圖尺寸8.55m x 5.75m）
    send_to_blender("""
bpy.ops.mesh.primitive_plane_add(size=1)
floor = bpy.context.active_object
floor.name = 'Floor'
floor.scale = (8.55, 5.75, 1)

# 地板材質
floor_mat = bpy.data.materials.new(name='Floor_Material')
floor_mat.use_nodes = True
nodes = floor_mat.node_tree.nodes
principled = nodes["Principled BSDF"]
principled.inputs[0].default_value = (0.8, 0.8, 0.8, 1)
floor.data.materials.append(floor_mat)
""")

    # 創建牆壁
    send_to_blender("""
# 牆壁材質
wall_mat = bpy.data.materials.new(name='Wall_Material')
wall_mat.use_nodes = True
wall_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.95, 0.95, 0.95, 1)

# 創建四面牆（高度3米）
walls = [
    {'location': (0, -2.875, 1.5), 'scale': (8.55, 0.1, 3)},  # 後牆
    {'location': (0, 2.875, 1.5), 'scale': (8.55, 0.1, 3)},   # 前牆
    {'location': (-4.275, 0, 1.5), 'scale': (0.1, 5.75, 3)},  # 左牆
    {'location': (4.275, 0, 1.5), 'scale': (0.1, 5.75, 3)}    # 右牆
]

for wall_data in walls:
    bpy.ops.mesh.primitive_cube_add(location=wall_data['location'])
    wall = bpy.context.active_object
    wall.scale = wall_data['scale']
    wall.data.materials.append(wall_mat)
""")

    # 創建浴室和衛生間隔間
    send_to_blender("""
# 浴室隔間
bpy.ops.mesh.primitive_cube_add(location=(3, -1, 1.5))
bathroom_wall = bpy.context.active_object
bathroom_wall.scale = (2.15, 0.1, 3)
bathroom_wall.data.materials.append(bpy.data.materials['Wall_Material'])

# 浴缸（根據平面圖）
bpy.ops.mesh.primitive_cube_add(location=(3.5, -2, 0.3))
bathtub = bpy.context.active_object
bathtub.scale = (0.8, 1.6, 0.3)

# 浴缸材質
tub_mat = bpy.data.materials.new(name='Bathtub_Material')
tub_mat.use_nodes = True
tub_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.9, 0.9, 1)
bathtub.data.materials.append(tub_mat)
""")

    # 創建大床（1800 x 2000）
    send_to_blender("""
# 床框
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.3))
bed_frame = bpy.context.active_object
bed_frame.scale = (1.8, 2, 0.3)

# 床墊
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.4))
mattress = bpy.context.active_object
mattress.scale = (1.7, 1.9, 0.2)

# 床的材質
bed_mat = bpy.data.materials.new(name='Bed_Material')
bed_mat.use_nodes = True
bed_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.9, 0.9, 1)
mattress.data.materials.append(bed_mat)
""")

    # 創建書桌和椅子
    send_to_blender("""
# 書桌
bpy.ops.mesh.primitive_cube_add(location=(-2.5, -2, 0.75))
desk = bpy.context.active_object
desk.scale = (1, 0.6, 0.05)

# 椅子
bpy.ops.mesh.primitive_cube_add(location=(-2.5, -1.5, 0.45))
chair = bpy.context.active_object
chair.scale = (0.4, 0.4, 0.45)
""")

    # 創建迷你吧和保險箱區域
    send_to_blender("""
# 迷你吧櫃子
bpy.ops.mesh.primitive_cube_add(location=(-3.5, -2.5, 0.9))
minibar = bpy.context.active_object
minibar.scale = (0.6, 0.4, 0.9)

# 保險箱
bpy.ops.mesh.primitive_cube_add(location=(-3.5, -2.5, 1.8))
safe = bpy.context.active_object
safe.scale = (0.4, 0.3, 0.3)
""")

    # 設置燈光
    send_to_blender("""
# 主燈
bpy.ops.object.light_add(type='AREA', location=(0, 0, 2.8))
main_light = bpy.context.active_object
main_light.data.energy = 1000
main_light.scale = (3, 3, 1)

# 浴室燈
bpy.ops.object.light_add(type='POINT', location=(3, -2, 2.5))
bathroom_light = bpy.context.active_object
bathroom_light.data.energy = 300
""")

    # 設置相機
    send_to_blender("""
import math
bpy.ops.object.camera_add(location=(12, -8, 6))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(125))
bpy.context.scene.camera = camera
""")

    # 設置渲染參數
    send_to_blender("""
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.filepath = "//deluxe_king_room.png"
bpy.ops.render.render(write_still=True)
""")

    print("✨ 完成：豪華大床房已生成！")
    print("🖼️ 渲染結果將保存為 'deluxe_king_room.png'")

if __name__ == "__main__":
    main()