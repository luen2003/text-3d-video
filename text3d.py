import bpy

# --- XÓA TOÀN BỘ CẢNH ---
if bpy.context.object and bpy.context.object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# --- TẠO CHỮ 3D ---
bpy.ops.object.text_add(location=(0, 0, 0))
text_obj = bpy.context.object
text_obj.data.body = "DLUONGTA"
text_obj.data.extrude = 0.3
text_obj.data.bevel_depth = 0.02
text_obj.data.align_x = 'CENTER'

# --- CĂN CHỈNH TỌA ĐỘ CHỮ ĐỂ TÂM VÀO GỐC (0,0,0) ---
bpy.context.view_layer.update()
text_height = text_obj.dimensions.z
# ĐÃ SỬA: Đặt tâm hình học của chữ tại Z=0 để chữ không bị nằm dưới
text_obj.location.z = -text_height / 2
bpy.context.view_layer.update()

# --- VẬT LIỆU CAM ---
mat = bpy.data.materials.new(name="DarkOrange")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (1.0, 0.3, 0.0, 1)
bsdf.inputs["Roughness"].default_value = 0.4
if text_obj.data.materials:
    text_obj.data.materials[0] = mat
else:
    text_obj.data.materials.append(mat)

# === CAMERA ===
z_center = 0
camera_height = z_center + 1 # Z=1

cam_start = (0, 0, camera_height + 8) 
cam_end = (0, 0, camera_height + 16)

bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, z_center))
target = bpy.context.object
target.name = "CameraTarget"

bpy.ops.object.camera_add(location=cam_start)
cam = bpy.context.object
bpy.context.scene.camera = cam

track = cam.constraints.new(type='TRACK_TO')
track.target = target
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

# === ĐÈN ===
bpy.ops.object.light_add(type='AREA', location=(0, -5, z_center + 4))
light = bpy.context.object
light.data.energy = 1500
light.data.size = 8

# === NỀN ĐEN ===
bpy.context.scene.world.use_nodes = True
bg = bpy.context.scene.world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value = (0, 0, 0, 1)

# === ANIMATION CAMERA ĐI LÙI ===
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 80

cam.location = cam_start
cam.keyframe_insert(data_path="location", frame=scene.frame_start)

cam.location = cam_end
cam.keyframe_insert(data_path="location", frame=scene.frame_end)

text_obj.keyframe_insert(data_path="location", frame=scene.frame_start)
text_obj.keyframe_insert(data_path="location", frame=scene.frame_end)

# === RENDER SETTINGS ===
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.filepath = "//dluongta_animation.mp4"
scene.render.film_transparent = False
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.fps = 30

# === RENDER VIDEO ===
print("Bắt đầu render animation...")
bpy.ops.render.render(animation=True)
print("Render hoàn tất! File được lưu tại:", scene.render.filepath)