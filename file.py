import bpy
import math
from mathutils import Vector

# =====================================================
# تنظيف المشهد
# =====================================================

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# =====================================================
# الخامات
# =====================================================

def mat(name, color, metallic=0.0, roughness=0.6):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color, 1)
    material.use_nodes = True

    bsdf = material.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness

    return material

PAINT = mat("Old Blue Paint", (0.055, 0.16, 0.22), 0.35, 0.55)
RUST = mat("Dark Rust", (0.12, 0.025, 0.008), 0.2, 0.85)
BLACK = mat("Black Rubber", (0.008, 0.009, 0.008), 0, 0.95)
DARK = mat("Dark Plastic", (0.018, 0.014, 0.010), 0, 0.8)
CHROME = mat("Old Chrome", (0.38, 0.38, 0.32), 0.8, 0.3)
GLASS = mat("Dirty Glass", (0.025, 0.12, 0.14), 0.15, 0.28)
LEATHER = mat("Old Brown Seats", (0.14, 0.035, 0.012), 0, 0.85)
YELLOW = mat("Yellow Headlights", (1.0, 0.48, 0.10), 0.1, 0.18)
RED = mat("Red Rear Lights", (0.65, 0.01, 0.005), 0.1, 0.25)
SAND = mat("Desert Sand", (0.28, 0.15, 0.055), 0, 1.0)
WHITE = mat("Old White Plastic", (0.55, 0.50, 0.38), 0, 0.75)

# =====================================================
# أدوات الإنشاء
# =====================================================

def apply_scale(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )
    obj.select_set(False)

def bevel(obj, amount=0.04, segments=2):
    modifier = obj.modifiers.new("Bevel", "BEVEL")
    modifier.width = amount
    modifier.segments = segments
    modifier.limit_method = "ANGLE"

def cube(name, loc, size, material, rot=(0, 0, 0), bevel_size=0.03):
    bpy.ops.mesh.primitive_cube_add(
        location=loc,
        rotation=rot
    )

    obj = bpy.context.object
    obj.name = name
    obj.dimensions = size
    apply_scale(obj)

    if bevel_size > 0:
        bevel(obj, bevel_size, 2)

    obj.data.materials.append(material)
    return obj

def cylinder(
    name,
    loc,
    radius,
    depth,
    material,
    rot=(0, 0, 0),
    vertices=16
):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=loc,
        rotation=rot
    )

    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    bevel(obj, 0.01, 1)
    return obj

def sphere(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16,
        ring_count=8,
        location=loc
    )

    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    apply_scale(obj)
    obj.data.materials.append(material)
    return obj

def torus(name, loc, major, minor, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major,
        minor_radius=minor,
        major_segments=20,
        minor_segments=8,
        location=loc,
        rotation=rot
    )

    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    return obj

# =====================================================
# المقاسات الرئيسية
#
# X = طول السيارة
# Y = عرض السيارة
# Z = الارتفاع
# =====================================================

# الشاصي
cube(
    "Pickup Chassis",
    (0, 0, 0.92),
    (5.0, 1.55, 0.25),
    RUST,
    bevel_size=0.08
)

# أرضية المقصورة
cube(
    "Cabin Floor",
    (0.25, 0, 1.17),
    (2.65, 1.45, 0.15),
    DARK,
    bevel_size=0.035
)

# جسم المقصورة
cube(
    "Cabin Body",
    (0.35, 0, 1.72),
    (2.70, 1.62, 1.18),
    PAINT,
    bevel_size=0.14
)

# مقدمة المحرك
cube(
    "Front Nose",
    (1.75, 0, 1.60),
    (1.00, 1.60, 0.95),
    PAINT,
    bevel_size=0.12
)

# غطاء المحرك
hood = cube(
    "Separate Hood",
    (1.62, 0, 2.14),
    (1.42, 1.42, 0.20),
    PAINT,
    bevel_size=0.07
)

# سقف الكابينة
cube(
    "Pickup Roof",
    (-0.15, 0, 2.65),
    (1.95, 1.46, 0.18),
    PAINT,
    bevel_size=0.08
)

# =====================================================
# الحوض الخلفي المفتوح
# =====================================================

# أرضية الحوض
cube(
    "Truck Bed Floor",
    (-1.75, 0, 1.25),
    (1.75, 1.43, 0.16),
    RUST,
    bevel_size=0.04
)

# الجدار الأمامي للحوض
cube(
    "Truck Bed Front Wall",
    (-0.92, 0, 1.82),
    (0.16, 1.48, 1.10),
    PAINT,
    bevel_size=0.05
)

# جانبا الحوض
for y in (-0.76, 0.76):
    cube(
        "Truck Bed Side",
        (-1.78, y, 1.72),
        (1.72, 0.15, 0.98),
        PAINT,
        bevel_size=0.06
    )

# الباب الخلفي للحوض
tailgate = cube(
    "Separate Tailgate",
    (-2.63, 0, 1.62),
    (0.15, 1.48, 0.86),
    PAINT,
    bevel_size=0.06
)

# خطوط على الباب الخلفي
for y in (-0.50, 0, 0.50):
    cube(
        "Tailgate Line",
        (-2.715, y, 1.62),
        (0.025, 0.035, 0.65),
        RUST,
        bevel_size=0.005
    )

# حواف الحوض المعدنية
for y in (-0.84, 0.84):
    cube(
        "Bed Top Rail",
        (-1.75, y, 2.24),
        (1.85, 0.10, 0.12),
        CHROME,
        bevel_size=0.025
    )

# =====================================================
# الزجاج والأعمدة
# =====================================================

# الزجاج الأمامي
cube(
    "Front Windshield",
    (0.72, 0, 2.37),
    (0.07, 1.26, 0.60),
    GLASS,
    rot=(0, math.radians(-13), 0),
    bevel_size=0.025
)

# الزجاج الخلفي للكابينة
cube(
    "Cabin Rear Window",
    (-0.72, 0, 2.35),
    (0.06, 1.25, 0.55),
    GLASS,
    rot=(0, math.radians(5), 0),
    bevel_size=0.025
)

# الأعمدة
for y in (-0.70, 0.70):
    cube(
        "Front Window Pillar",
        (0.68, y, 2.38),
        (0.13, 0.12, 0.90),
        RUST,
        rot=(0, math.radians(-12), 0),
        bevel_size=0.025
    )

    cube(
        "Rear Window Pillar",
        (-0.68, y, 2.38),
        (0.13, 0.12, 0.88),
        RUST,
        rot=(0, math.radians(8), 0),
        bevel_size=0.025
    )

# =====================================================
# الأبواب المنفصلة
# =====================================================

def create_door(name, y, side):
    bpy.ops.object.empty_add(
        type="PLAIN_AXES",
        location=(1.00, y, 1.65)
    )

    hinge = bpy.context.object
    hinge.name = name + " Hinge"

    door = cube(
        name,
        (0.05, y, 1.62),
        (1.80, 0.11, 1.10),
        PAINT,
        bevel_size=0.07
    )
    door.parent = hinge

    window_frame = cube(
        name + " Window Frame",
        (0.03, y + side * 0.06, 2.22),
        (1.42, 0.04, 0.48),
        RUST,
        bevel_size=0.025
    )
    window_frame.parent = hinge

    window = cube(
        name + " Window",
        (0.03, y + side * 0.085, 2.23),
        (1.20, 0.025, 0.34),
        GLASS,
        bevel_size=0.015
    )
    window.parent = hinge

    handle = cube(
        name + " Handle",
        (0.48, y + side * 0.10, 1.91),
        (0.28, 0.04, 0.06),
        CHROME,
        bevel_size=0.012
    )
    handle.parent = hinge

    # مفصلات الباب
    for z in (1.36, 1.88):
        pin = cylinder(
            name + " Hinge Pin",
            (0.98, y + side * 0.10, z),
            0.045,
            0.18,
            CHROME,
            rot=(math.radians(90), 0, 0),
            vertices=8
        )
        pin.parent = hinge

    # فتح بسيط
    hinge.rotation_euler[2] = math.radians(side * 3)

    return hinge

create_door("Left Door", -0.84, -1)
create_door("Right Door", 0.84, 1)

# =====================================================
# المقاعد
# =====================================================

def create_seat(name, x, y):
    cube(
        name + " Cushion",
        (x, y, 1.48),
        (0.80, 0.56, 0.22),
        LEATHER,
        bevel_size=0.08
    )

    cube(
        name + " Back",
        (x - 0.25, y, 2.00),
        (0.25, 0.56, 0.85),
        LEATHER,
        rot=(0, math.radians(-8), 0),
        bevel_size=0.09
    )

    cube(
        name + " Headrest",
        (x - 0.45, y, 2.45),
        (0.18, 0.40, 0.23),
        LEATHER,
        bevel_size=0.07
    )

create_seat("Driver Seat", -0.25, -0.42)
create_seat("Passenger Seat", -0.25, 0.42)

# =====================================================
# لوحة القيادة والدركسون
# =====================================================

cube(
    "Dashboard",
    (0.78, 0, 2.00),
    (0.28, 1.40, 0.38),
    DARK,
    bevel_size=0.06
)

cube(
    "Dashboard Top",
    (0.62, 0, 2.22),
    (0.55, 1.40, 0.12),
    DARK,
    bevel_size=0.035
)

# العدادات
for y in (-0.30, 0, 0.30):
    cylinder(
        "Gauge",
        (0.57, y, 2.23),
        0.08,
        0.03,
        WHITE,
        rot=(0, math.radians(90), 0),
        vertices=16
    )

# عمود الدركسون
cylinder(
    "Steering Column",
    (0.38, -0.42, 2.02),
    0.05,
    0.48,
    BLACK,
    rot=(0, math.radians(58), 0),
    vertices=10
)

# الدركسون
torus(
    "Steering Wheel",
    (0.17, -0.42, 2.20),
    0.22,
    0.035,
    BLACK,
    rot=(math.radians(70), 0, 0)
)

cylinder(
    "Steering Center",
    (0.17, -0.42, 2.20),
    0.06,
    0.06,
    CHROME,
    rot=(math.radians(70), 0, 0),
    vertices=12
)

# ناقل الحركة
cylinder(
    "Gear Stick",
    (0.25, -0.04, 1.75),
    0.035,
    0.34,
    BLACK,
    rot=(0, math.radians(-10), 0),
    vertices=8
)

sphere(
    "Gear Knob",
    (0.22, -0.04, 1.93),
    (0.08, 0.08, 0.08),
    BLACK
)

# =====================================================
# الرفارف
# =====================================================

for x in (1.35, -1.35):
    for y in (-0.88, 0.88):
        cube(
            "Wheel Fender",
            (x, y, 1.35),
            (0.90, 0.18, 0.38),
            RUST,
            bevel_size=0.12
        )

# =====================================================
# العجلات والجنوط
# =====================================================

wheel_positions = [
    (1.42, -0.98, 0.93),
    (1.42,  0.98, 0.93),
    (-1.45, -0.98, 0.93),
    (-1.45,  0.98, 0.93)
]

def create_wheel(number, pos):
    x, y, z = pos

    cylinder(
        "Tire " + str(number),
        (x, y, z),
        0.56,
        0.34,
        BLACK,
        rot=(math.radians(90), 0, 0),
        vertices=20
    )

    face_y = y - 0.19 if y < 0 else y + 0.19

    cylinder(
        "Steel Rim " + str(number),
        (x, face_y, z),
        0.31,
        0.045,
        CHROME,
        rot=(math.radians(90), 0, 0),
        vertices=16
    )

    cylinder(
        "Hub " + str(number),
        (x, face_y, z),
        0.11,
        0.065,
        BLACK,
        rot=(math.radians(90), 0, 0),
        vertices=12
    )

    for angle in range(0, 360, 60):
        a = math.radians(angle)
        sx = x + math.cos(a) * 0.20
        sz = z + math.sin(a) * 0.20

        cube(
            "Rim Spoke " + str(number),
            (sx, face_y, sz),
            (0.20, 0.035, 0.035),
            CHROME,
            rot=(0, 0, a),
            bevel_size=0.008
        )

for i, position in enumerate(wheel_positions):
    create_wheel(i + 1, position)

# =====================================================
# المصابيح الأمامية والشبك
# =====================================================

for y in (-0.55, 0.55):
    cylinder(
        "Headlight Housing",
        (2.31, y, 1.90),
        0.24,
        0.10,
        BLACK,
        rot=(0, math.radians(90), 0),
        vertices=16
    )

    cylinder(
        "Headlight",
        (2.37, y, 1.90),
        0.17,
        0.035,
        YELLOW,
        rot=(0, math.radians(90), 0),
        vertices=16
    )

# شبك أمامي
for y in (-0.52, -0.26, 0, 0.26, 0.52):
    cube(
        "Grille Bar",
        (2.37, y, 1.57),
        (0.06, 0.035, 0.36),
        BLACK,
        bevel_size=0.008
    )

# شعار أمامي
cylinder(
    "Front Emblem",
    (2.41, 0, 1.63),
    0.11,
    0.035,
    CHROME,
    rot=(0, math.radians(90), 0),
    vertices=16
)

# =====================================================
# المصابيح الخلفية
# =====================================================

for y in (-0.57, 0.57):
    cube(
        "Rear Light Housing",
        (-2.58, y, 1.84),
        (0.07, 0.24, 0.27),
        BLACK,
        bevel_size=0.025
    )

    cube(
        "Rear Red Light",
        (-2.625, y, 1.84),
        (0.025, 0.16, 0.16),
        RED,
        bevel_size=0.012
    )

# =====================================================
# الصدامات
# =====================================================

cube(
    "Front Bumper",
    (2.47, 0, 1.25),
    (0.18, 1.90, 0.20),
    CHROME,
    bevel_size=0.05
)

cube(
    "Rear Bumper",
    (-2.70, 0, 1.24),
    (0.18, 1.90, 0.20),
    CHROME,
    bevel_size=0.05
)

# =====================================================
# المرايا
# =====================================================

for y, side in [(-0.96, -1), (0.96, 1)]:
    cylinder(
        "Mirror Arm",
        (0.78, y, 2.31),
        0.035,
        0.30,
        BLACK,
        rot=(math.radians(90), 0, 0),
        vertices=8
    )

    cube(
        "Side Mirror",
        (0.78, y + side * 0.11, 2.37),
        (0.20, 0.11, 0.18),
        BLACK,
        bevel_size=0.04
    )

    cube(
        "Mirror Glass",
        (0.78, y + side * 0.17, 2.37),
        (0.12, 0.025, 0.10),
        GLASS,
        bevel_size=0.015
    )

# =====================================================
# العادم
# =====================================================

cylinder(
    "Exhaust Pipe",
    (-1.80, -0.80, 0.75),
    0.07,
    0.90,
    CHROME,
    rot=(0, math.radians(90), 0),
    vertices=10
)

cylinder(
    "Exhaust Tip",
    (-2.25, -0.80, 0.75),
    0.09,
    0.18,
    BLACK,
    rot=(0, math.radians(90), 0),
    vertices=10
)

# =====================================================
# الأرضية الصحراوية
# =====================================================

cube(
    "Desert Ground",
    (0, 0, 0.08),
    (14, 10, 0.16),
    SAND,
    bevel_size=0.02
)

# =====================================================
# الإضاءة
# =====================================================

bpy.ops.object.light_add(
    type="AREA",
    location=(5, -5, 7)
)

key = bpy.context.object
key.name = "Warm Sun Light"
key.data.energy = 1400
key.data.size = 5
key.data.color = (1.0, 0.55, 0.30)

bpy.ops.object.light_add(
    type="AREA",
    location=(-4, 3, 5)
)

fill = bpy.context.object
fill.name = "Cool Fill Light"
fill.data.energy = 600
fill.data.size = 4
fill.data.color = (0.30, 0.45, 1.0)

bpy.ops.object.light_add(
    type="SUN",
    location=(0, 0, 6)
)

sun = bpy.context.object
sun.name = "Desert Sun"
sun.rotation_euler = (
    math.radians(25),
    math.radians(-25),
    math.radians(-30)
)
sun.data.energy = 2.0
sun.data.angle = math.radians(10)

# =====================================================
# الكاميرا
# =====================================================

bpy.ops.object.camera_add(
    location=(8.2, -8.2, 5.0)
)

camera = bpy.context.object
camera.name = "Pickup Camera"

direction = Vector((0, 0, 1.45)) - camera.location
camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
camera.data.lens = 55

bpy.context.scene.camera = camera

# =====================================================
# إعداد التصيير
# =====================================================

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 1100
scene.render.resolution_y = 750
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = "//pickup_render.png"

scene.world.use_nodes = True
background = scene.world.node_tree.nodes.get("Background")
background.inputs["Color"].default_value = (0.025, 0.012, 0.006, 1)
background.inputs["Strength"].default_value = 0.3

# حفظ الملف
bpy.ops.wm.save_as_mainfile(
    filepath="//realistic_pickup.blend"
)

print("تم إنشاء شاحنة Pickup كاملة بنجاح")
