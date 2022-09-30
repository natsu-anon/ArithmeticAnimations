import bpy
import mathutils

EPSILON = 0.001


def lerp(A, B, frac):
    return frac * (B - A) + A


def average(A_frame, B_frame, A_curve, B_curve):
    print("A: {}\tB: {}".format(A_frame, B_frame))
    return 0.5 * (A_curve.evaluate(A_frame) + B_curve.evaluate(B_frame))


def difference(A_frame, B_frame, A_curve, B_curve):
    return A_curve.evaluate(A_frame) - B_curve.evaluate(B_frame)


def check_name(self, context):
    if self.new_name in bpy.data.actions.keys():
        self.new_name = "AA_" + self.new_name


def new_action(name):
    res = bpy.data.actions.new(name)
    return res


def get_eval_range(A, B):
    (A0, A1) = A.frame_range
    (B0, B1) = B.frame_range
    start = A0 if A0 < B0 else B0
    end = A1 if A1 > B1 else B1
    return (start, end)


def mix_curves(frame, frame_range, A_curve, B_curve, A_range, B_range, mix_func):
    perc = (frame - frame_range[0]) / (frame_range[1] - frame_range[0])
    A_frame = lerp(A_range[0], A_range[1], perc)
    B_frame = lerp(B_range[0], B_range[1], perc)
    print("mix percentage: {}%".format(perc))
    return mix_func(A_frame, B_frame, A_curve, B_curve)

def get_eval_frames(frame, frame_range, A_range, B_range):
    perc = (frame - frame_range[0]) / (frame_range[1] - frame_range[0])
    return lerp(A_range[0], A_range[1], perc), lerp(B_range[0], B_range[1], perc)


class AA_Addon_Props(bpy.types.PropertyGroup):
    new_name: bpy.props.StringProperty(name='', default='', description="name of the action to create", update=check_name)
    mix_enum: bpy.props.EnumProperty(name='', default=0, items=[
        ('DIFF', 'Difference', 'Create a new action using the difference between two existing actions'),
        ('AVG', 'Average', 'Create a new action using the averge of two existing action')
    ])
    action_A: bpy.props.PointerProperty(type=bpy.types.Action, description="first argument action")
    action_B: bpy.props.PointerProperty(type=bpy.types.Action, description="second argument action")

class AA_Addon_Difference(bpy.types.Operator):
    bl_idname = 'arithmetic_animations.diff'
    bl_label = 'Action Difference'
    bl_description = 'Create a new action by taking the difference of two argument actions'
    EPSILON = 0.001

    def execute(self, context):
        aa = context.scene.arithmetic_animations
        A = aa.action_A
        B = aa.action_B
        action = new_action(aa.new_name)
        A_data = [(curve.data_path, curve.array_index) for curve in A.fcurves]
        B_data = [(curve.data_path, curve.array_index) for curve in B.fcurves]
        shared_data = [data for data in A_data if data in B_data]
        data = {path: [] for (path, _) in shared_data}
        for (path, i) in shared_data:
            data[path].append(i)
        frame_range = get_eval_range(A, B)
        frame_args = (A.frame_range, B.frame_range)
        for path, indices in data.items():
            new_curves = [action.fcurves.new(path, index=i) for i in indices]
            curves = [[A.fcurves.find(path, index=i) for i in indices], [B.fcurves.find(path, index=i) for i in indices]]
            for frame in range(int(frame_range[0]), int(frame_range[1])):
                fl_frame = float(frame)
                A_frame, B_frame = get_eval_frames(fl_frame, frame_range, *frame_args)
                # it's a quaternion BABEEEEEEEEEEEEEEEE
                if len(indices) == 4:
                    A_q = mathutils.Quaternion([curves[0][i].evaluate(A_frame) for i in range(0, 4)])
                    B_q = mathutils.Quaternion([curves[1][i].evaluate(B_frame) for i in range(0, 4)])
                    res = A_q.rotation_difference(B_q)
                    for i in indices:
                        new_curves[i].keyframe_points.insert(fl_frame, res[i])
                        new_curves[i].update()
                else:
                    # just diff it whatever fam
                    for i in indices:
                        print(i)
                        val = curves[0][i].evaluate(A_frame) - curves[1][i].evaluate(B_frame)
                        # if abs(val) > EPSILON:
                        #     new_curves[i].keyframe_points.insert(fl_frame, val)
                        if path.endswith('.scale'):
                            new_curves[i].keyframe_points.insert(fl_frame, val + 1.0)
                        else:
                            new_curves[i].keyframe_points.insert(fl_frame, val)
            for i in indices:
                new_curves[i].update()
        self.report({"INFO"}, "Created \"{}\"!".format(aa.new_name))
        aa.new_name = ""
        return {'FINISHED'}


# curve.keyframe.insert
class AA_Addon_Average(bpy.types.Operator):
    bl_idname = 'arithmetic_animations.avg'
    bl_label = 'Action Average'
    bl_description = 'Create a new action by averaging two argument actions'

    def execute(self, context):
        aa = context.scene.arithmetic_animations
        A = aa.action_A
        B = aa.action_B
        # TODO average
        action = new_action(aa.new_name)
        A_data = [(curve.data_path, curve.array_index) for curve in A.fcurves]
        B_data = [(curve.data_path, curve.array_index) for curve in B.fcurves]
        shared_data = [data for data in A_data if data in B_data]
        data = {path: [] for (path, _) in shared_data}
        for (path, i) in shared_data:
            data[path].append(i)
        frame_range = get_eval_range(A, B)
        frame_args = (A.frame_range, B.frame_range)
        for path, indices in data.items():
            new_curves = [action.fcurves.new(path, index=i) for i in indices]
            curves = [[A.fcurves.find(path, index=i) for i in indices], [B.fcurves.find(path, index=i) for i in indices]]
            for frame in range(int(frame_range[0]), int(frame_range[1])):
                fl_frame = float(frame)
                A_frame, B_frame = get_eval_frames(fl_frame, frame_range, *frame_args)
                # it's a quaternion BABEEEEEEEEEEEEEEEE
                if len(indices) == 4:
                    A_q = mathutils.Quaternion([curves[0][i].evaluate(A_frame) for i in range(0, 4)])
                    B_q = mathutils.Quaternion([curves[1][i].evaluate(B_frame) for i in range(0, 4)])
                    res = A_q.slerp(B_q, 0.5)
                    for i in indices:
                        new_curves[i].keyframe_points.insert(fl_frame, res[i])
                else:
                    # just average it whatever fam
                    for i in indices:
                        val = 0.5 * (curves[0][i].evaluate(A_frame) + curves[1][i].evaluate(B_frame))
                        new_curves[i].keyframe_points.insert(fl_frame, val)
            for i in indices:
                new_curves[i].update()
        # just copy the unique stuff ezpz
        unique_data = [data for data in A_data if data not in B_data]
        for (path, i) in unique_data:
            curve = action.fcurves.new(path, index=i)
            curve.keyframe_points = A.fcurves.find(path, index=i).keyframe_points
            curve.update()
        unique_data = [data for data in B_data if data not in A_data]
        for (path, i) in unique_data:
            curve = action.fcurves.new(path, index=i)
            curve.keyframe_points = B.fcurves.find(path, index=i).keyframe_points
            curve.update()
        self.report({"INFO"}, "Created \"{}\"!".format(aa.new_name))
        aa.new_name = ""
        return {'FINISHED'}
