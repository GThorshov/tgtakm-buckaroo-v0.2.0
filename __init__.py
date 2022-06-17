# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "TGTAKM - Renderlad",
    "author" : "Grant Thorshov",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

from operator import truediv
import bpy
import os

# And now we can use this list everywhere in Blender. Here is a small example panel.
class UIListPanelExample(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "RENDERLAD"
    bl_idname = "RENDERLAD_UI_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        # Create a simple row.
        layout.label(text=" Render Range:")

        row = layout.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Set Cycles Settings
        layout.label(text="Set Render Settings")
        row = layout.row()
        row.scale_y = 2
        row.operator("object.set_cycles_settings")
        row.operator("object.set_workbench_settings")

        layout.label(text="Render Shot CLI:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.render_cycles")
        row.operator("object.render_workbench")

class SetCyclesSettings(bpy.types.Operator):
    bl_idname = "object.set_cycles_settings"
    bl_label = "Set Cycles Settings"

    @classmethod
    def poll(cls,context):
        return True

    def execute(self,context):
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.device = 'GPU'
        bpy.context.scene.cycles.time_limit = 15
        bpy.context.scene.render.use_persistent_data = True
        bpy.context.scene.view_settings.view_transform = 'Filmic'
        bpy.context.scene.view_settings.look = 'High Contrast'
        bpy.context.scene.render.resolution_x = 2048
        bpy.context.scene.render.resolution_y = 1024
        bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR'
        bpy.context.scene.render.image_settings.color_depth = '16'

        return {'FINISHED'}

class SetWorkbenchSettings(bpy.types.Operator):
    bl_idname = "object.set_workbench_settings"
    bl_label = "Set Workbench Settings"

    @classmethod
    def poll(cls,context):
        return True

    def execute(self,context):

        bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
        bpy.context.scene.render.resolution_x = 2048
        bpy.context.scene.render.resolution_y = 1024
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = 'QUICKTIME'
        bpy.context.scene.render.ffmpeg.codec = 'H264'
        bpy.context.scene.render.ffmpeg.audio_codec = 'MP3'

        return {'FINISHED'}


class RenderCycles(bpy.types.Operator):
    bl_idname = "object.render_cycles"
    bl_label = "Cycles Render"

    @classmethod
    def poll(cls,context):
        if bpy.data.is_saved: 

            return True

    
    def execute(self,context):

        os.chdir(bpy.path.abspath('//'))
        os.chdir('../')
        if "CYCLES" not in os.listdir(os.getcwd()):
            path = os.path.join(os.getcwd(), "CYCLES")
            os.mkdir(path)
            os.chdir('CYCLES')
        
        print(os.getcwd())

        # Update Render Settings
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.device = 'GPU'
        bpy.context.scene.cycles.time_limit = 15
        bpy.context.scene.render.use_persistent_data = True
        bpy.context.scene.view_settings.view_transform = 'Filmic'
        bpy.context.scene.view_settings.look = 'High Contrast'
        bpy.context.scene.render.resolution_x = 2048
        bpy.context.scene.render.resolution_y = 1024
        bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR'
        bpy.context.scene.render.image_settings.color_depth = '16'

        return {'FINISHED'}

class RenderWorkbench(bpy.types.Operator):
    bl_idname = "object.render_workbench"
    bl_label = "Workbench Render"
    
    @classmethod
    def poll(cls,context):
        if bpy.data.is_saved:
            return True
    
    def execute(self,context):
        print('bloop')
        return {'FINISHED'}

def register(): 
    bpy.utils.register_class(UIListPanelExample)
    bpy.utils.register_class(RenderCycles)
    bpy.utils.register_class(SetCyclesSettings)
    bpy.utils.register_class(SetWorkbenchSettings)
    bpy.utils.register_class(RenderWorkbench)


def unregister():
    bpy.utils.unregister_class(UIListPanelExample)
    bpy.utils.unregister_class(RenderCycles)
    bpy.utils.unregister_class(SetCyclesSettings)
    bpy.utils.unregister_class(SetWorkbenchSettings)
    bpy.utils.unregister_class(RenderWorkbench)


if __name__ == "__main__":
    register()

