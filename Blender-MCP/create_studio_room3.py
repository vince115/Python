#!/usr/bin/env python3
"""
簡約臥室生成器 (Socket 版本)
生成類似參考圖的簡約風格臥室
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
    print("🏠 開始生成簡約臥室...")

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

    # 創建地板
    send_to_blender("""
# 木地板
bpy.ops.mesh.primitive_plane_add(size=6)
floor = bpy.context.active_object
floor.name = 'Floor'

# 木質材質
wood_mat = bpy.data.materials.new(name='Wood_Material')
wood_mat.use_nodes = True
nodes = wood_mat.node_tree.nodes
principled = nodes["Principled BSDF"]
principled.inputs[0].default_value = (0.8, 0.7, 0.5, 1)
principled.inputs[7].default_value = 0.3
floor.data.materials.append(wood_mat)
""")

    # 創建牆壁
    send_to_blender("""
# 白色牆面材質
wall_mat = bpy.data.materials.new(name='Wall_Material')
wall_mat.use_nodes = True
wall_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.95, 0.95, 0.95, 1)

# 後牆
bpy.ops.mesh.primitive_cube_add(location=(0, -3, 1.5))
back_wall = bpy.context.active_object
back_wall.scale = (3, 0.1, 1.5)
back_wall.data.materials.append(wall_mat)

# 側牆
bpy.ops.mesh.primitive_cube_add(location=(-3, 0, 1.5))
side_wall = bpy.context.active_object
side_wall.scale = (0.1, 3, 1.5)
side_wall.data.materials.append(wall_mat)
""")

    # 創建窗戶
    send_to_blender("""
# 窗戶框架
bpy.ops.mesh.primitive_cube_add(location=(-2.9, 0, 1.5))
window_frame = bpy.context.active_object
window_frame.scale = (0.2, 2, 1.2)

# 玻璃
glass_mat = bpy.data.materials.new(name='Glass_Material')
glass_mat.use_nodes = True
glass_mat.blend_method = 'BLEND'
glass_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 1, 0.2)
glass_mat.node_tree.nodes["Principled BSDF"].inputs['Transmission'].default_value = 0.95
window_frame.data.materials.append(glass_mat)
""")

    # 創建床
    send_to_blender("""
# 床框
bpy.ops.mesh.primitive_cube_add(location=(0, -1.5, 0.25))
bed_frame = bpy.context.active_object
bed_frame.scale = (2, 1.2, 0.25)

# 床墊
bpy.ops.mesh.primitive_cube_add(location=(0, -1.5, 0.35))
mattress = bpy.context.active_object
mattress.scale = (1.9, 1.1, 0.15)

# 白色床單材質
bed_mat = bpy.data.materials.new(name='Bedding_Material')
bed_mat.use_nodes = True
bed_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.95, 0.95, 0.95, 1)
mattress.data.materials.append(bed_mat)

# 枕頭
bpy.ops.mesh.primitive_cube_add(location=(0, -2.3, 0.45))
pillow = bpy.context.active_object
pillow.scale = (0.8, 0.3, 0.1)
pillow.data.materials.append(bed_mat)

# 深藍色毯子
bpy.ops.mesh.primitive_cube_add(location=(0, -1, 0.4))
blanket = bpy.context.active_object
blanket.scale = (1.8, 0.6, 0.05)
blanket_mat = bpy.data.materials.new(name='Blanket_Material')
blanket_mat.use_nodes = True
blanket_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.1, 0.2, 0.4, 1)
blanket.data.materials.append(blanket_mat)
""")

    # 創建空調
    send_to_blender("""
bpy.ops.mesh.primitive_cube_add(location=(0, -2.9, 2.5))
ac = bpy.context.active_object
ac.scale = (0.8, 0.2, 0.25)
ac_mat = bpy.data.materials.new(name='AC_Material')
ac_mat.use_nodes = True
ac_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.9, 0.9, 1)
ac.data.materials.append(ac_mat)
""")

    # 創建床頭燈
    send_to_blender("""
# 燈座
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1.2, location=(-1.5, -2.3, 0.6))
lamp_stand = bpy.context.active_object
lamp_stand.rotation_euler[0] = 0.3

# 燈罩
bpy.ops.mesh.primitive_cone_add(radius1=0.15, radius2=0.08, depth=0.3, location=(-1.6, -2.4, 1.2))
lamp_shade = bpy.context.active_object
lamp_shade.rotation_euler[0] = 0.3
""")

    # 設置燈光
    send_to_blender("""
# 自然光
bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
sun = bpy.context.active_object
sun.data.energy = 5

# 床頭燈光源
bpy.ops.object.light_add(type='POINT', location=(-1.6, -2.4, 1.2))
lamp_light = bpy.context.active_object
lamp_light.data.energy = 30
lamp_light.data.color = (1, 0.95, 0.8)
""")

    # 設置相機
    send_to_blender("""
import math
bpy.ops.object.camera_add(location=(4, -4, 2))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(70), 0, math.radians(135))
bpy.context.scene.camera = camera
""")

    # 設置渲染參數
    send_to_blender("""
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.filepath = "//minimal_bedroom.png"
bpy.ops.render.render(write_still=True)
""")

    print("✨ 完成：簡約臥室已生成！")
    print("🖼️ 渲染結果將保存為 'minimal_bedroom.png'")

if __name__ == "__main__":
    main()