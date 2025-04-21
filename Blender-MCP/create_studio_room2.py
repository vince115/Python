#!/usr/bin/env python3
"""
詳細套房生成器 (Socket 版本)
生成包含完整傢俱和細節的套房
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
        time.sleep(0.2)  # 增加延遲確保命令執行完成

def main():
    print("🏠 開始生成詳細套房...")

    # 清除場景
    print("🧹 清除現有場景...")
    send_to_blender("""
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
""")

    # 設置渲染引擎
    print("⚙️ 設置渲染引擎...")
    send_to_blender("""
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.cycles.samples = 128
""")

    # 創建地板
    print("🔨 創建地板...")
    send_to_blender("""
bpy.ops.mesh.primitive_plane_add(size=8)
floor = bpy.context.active_object
floor.name = 'Floor'
mat = bpy.data.materials.new(name='Floor_Material')
mat.use_nodes = True
nodes = mat.node_tree.nodes
principled = nodes["Principled BSDF"]
principled.inputs[0].default_value = (0.8, 0.8, 0.8, 1)
principled.inputs[7].default_value = 0.2  # 粗糙度
floor.data.materials.append(mat)
""")

    # 創建牆壁
    print("🧱 創建牆壁...")
    send_to_blender("""
# 建立牆壁材質
wall_mat = bpy.data.materials.new(name='Wall_Material')
wall_mat.use_nodes = True
wall_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.9, 0.9, 1)

# 後牆
bpy.ops.mesh.primitive_cube_add(location=(0, -4, 1.5))
back_wall = bpy.context.active_object
back_wall.scale = (4, 0.1, 1.5)
back_wall.data.materials.append(wall_mat)

# 左牆
bpy.ops.mesh.primitive_cube_add(location=(-4, 0, 1.5))
left_wall = bpy.context.active_object
left_wall.scale = (0.1, 4, 1.5)
left_wall.data.materials.append(wall_mat)

# 右牆
bpy.ops.mesh.primitive_cube_add(location=(4, 0, 1.5))
right_wall = bpy.context.active_object
right_wall.scale = (0.1, 4, 1.5)
right_wall.data.materials.append(wall_mat)
""")

    # 創建門
    print("🚪 創建門...")
    send_to_blender("""
# 門框
bpy.ops.mesh.primitive_cube_add(location=(2, -3.9, 1.1))
door_frame = bpy.context.active_object
door_frame.scale = (0.6, 0.15, 1.1)

# 門板
bpy.ops.mesh.primitive_cube_add(location=(2, -3.85, 1))
door = bpy.context.active_object
door.scale = (0.5, 0.05, 1)

# 門把手
bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.2, location=(1.7, -3.8, 1))
handle = bpy.context.active_object
handle.rotation_euler[0] = 1.5708

# 門的材質
door_mat = bpy.data.materials.new(name='Door_Material')
door_mat.use_nodes = True
door_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.4, 0.2, 0.1, 1)
door.data.materials.append(door_mat)
door_frame.data.materials.append(door_mat)
""")

    # 創建窗戶
    print("🪟 創建窗戶...")
    send_to_blender("""
# 窗框
bpy.ops.mesh.primitive_cube_add(location=(-3.9, 0, 1.5))
window_frame = bpy.context.active_object
window_frame.scale = (0.15, 1.2, 1)

# 玻璃
bpy.ops.mesh.primitive_cube_add(location=(-3.85, 0, 1.5))
window = bpy.context.active_object
window.scale = (0.05, 1, 0.8)

# 玻璃材質
glass_mat = bpy.data.materials.new(name='Glass_Material')
glass_mat.use_nodes = True
glass_mat.blend_method = 'BLEND'
glass_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.9, 1, 0.2)
glass_mat.node_tree.nodes["Principled BSDF"].inputs['Transmission'].default_value = 0.95
window.data.materials.append(glass_mat)
""")

    # 創建床
    print("🛏️ 創建床...")
    send_to_blender("""
# 床框
bpy.ops.mesh.primitive_cube_add(location=(-2.5, -2.5, 0.3))
bed_frame = bpy.context.active_object
bed_frame.scale = (1.2, 2, 0.3)

# 床墊
bpy.ops.mesh.primitive_cube_add(location=(-2.5, -2.5, 0.5))
mattress = bpy.context.active_object
mattress.scale = (1.1, 1.9, 0.1)

# 枕頭
bpy.ops.mesh.primitive_cube_add(location=(-2.5, -3.8, 0.7))
pillow = bpy.context.active_object
pillow.scale = (0.8, 0.3, 0.1)

# 被子
bpy.ops.mesh.primitive_cube_add(location=(-2.5, -2, 0.6))
blanket = bpy.context.active_object
blanket.scale = (1, 1.5, 0.05)

# 床的材質
bed_mat = bpy.data.materials.new(name='Bed_Material')
bed_mat.use_nodes = True
bed_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.3, 0.8, 1)
mattress.data.materials.append(bed_mat)
blanket.data.materials.append(bed_mat)
""")

    # 創建書桌和椅子
    print("🪑 創建書桌和椅子...")
    send_to_blender("""
# 桌面
bpy.ops.mesh.primitive_cube_add(location=(2, -2, 0.75))
desk = bpy.context.active_object
desk.scale = (1, 0.6, 0.05)

# 桌腳
for x in [-0.8, 0.8]:
    for y in [-0.4, 0.4]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1.4, location=(2+x, -2+y, 0.35))

# 椅子座位
bpy.ops.mesh.primitive_cube_add(location=(2, -1.2, 0.45))
chair_seat = bpy.context.active_object
chair_seat.scale = (0.4, 0.4, 0.05)

# 椅背
bpy.ops.mesh.primitive_cube_add(location=(2, -0.8, 0.8))
chair_back = bpy.context.active_object
chair_back.scale = (0.4, 0.05, 0.4)
""")

    # 創建衣櫃
    print("🗄️ 創建衣櫃...")
    send_to_blender("""
# 衣櫃主體
bpy.ops.mesh.primitive_cube_add(location=(3.5, -2, 1.2))
wardrobe = bpy.context.active_object
wardrobe.scale = (0.4, 1, 1.2)

# 衣櫃門把手
bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.2, location=(3.1, -2.5, 1.2))
handle = bpy.context.active_object
handle.rotation_euler[0] = 1.5708
""")

    # 設置燈光
    print("💡 設置燈光...")
    send_to_blender("""
# 主燈
bpy.ops.object.light_add(type='AREA', location=(0, 0, 2.9))
main_light = bpy.context.active_object
main_light.data.energy = 800
main_light.scale = (3, 3, 1)

# 床頭燈
bpy.ops.object.light_add(type='POINT', location=(-2.5, -3.5, 1.2))
bed_light = bpy.context.active_object
bed_light.data.energy = 100
""")

    # 設置相機
    print("📸 設置相機...")
    send_to_blender("""
import math
bpy.ops.object.camera_add(location=(8, -8, 5))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(135))
bpy.context.scene.camera = camera
""")

    # 設置渲染參數
    print("🎨 設置渲染參數並開始渲染...")
    send_to_blender("""
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.filepath = "//detailed_room_render.png"
bpy.ops.render.render(write_still=True)
""")

    print("✨ 完成：詳細套房已生成！")
    print("🖼️ 渲染結果將保存為 'detailed_room_render.png'")

if __name__ == "__main__":
    main()