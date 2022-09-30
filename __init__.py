import bpy
from .ui import *
from .arithmetic_animations import *

classes = [PanelVIEW3D, AA_Addon_Props, AA_Addon_Difference, AA_Addon_Average]


bl_info = {
    "name": "Arithmetic Animations",
    "description": "Create animations by taking the difference, and average of existing ones",
    "author": "Natsu Dev",
    "version": (0, 1, 0),
    "blender": (3, 3, 0),
    "location": "3D View > Toolbox",
    "category": "Animation",
    "tracker_url": "https://github.com/natsu-anon/ArithmeticAnimations/issues"
}

# module_names = ['arithmetic_animations', 'ui']
# module_names = ['ui']

# module_full_names = {}
# for module_name in module_names:
#     module_full_names[module_name] = ('{}.{}'.format(__name__, module_name))

# import sys
# import importlib

# for full_name in module_full_names.values():
#     if full_name in sys.modules:
#         importlib.reload(sys.modules[full_name])
#     else:
#         globals()[full_name] = importlib.import_module(full_name)
#         setattr(globals()[full_name], 'modulesNames', module_full_names)


# def register():
#     for full_name in module_full_names.values():
#         if full_name in sys.modules:
#             if hasattr(sys.modules[full_name], 'register'):
#                 sys.modules[full_name].register()


# def unregister():
#     for full_name in module_full_names.values():
#         if full_name in sys.modules:
#             if hasattr(sys.modules[full_name], 'unregister'):
#                 sys.modules[full_name].unregister()

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.arithmetic_animations = bpy.props.PointerProperty(type=AA_Addon_Props)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.arithmetic_animations
