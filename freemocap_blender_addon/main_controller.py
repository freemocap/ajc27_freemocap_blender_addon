import traceback
from pathlib import Path
from typing import List, Optional

import numpy as np
from freemocap_blender_addon.freemocap_data_handler.utilities.load_data import load_freemocap_data

from freemocap_blender_addon.core_functions.create_video.create_video import create_video
from freemocap_blender_addon.core_functions.empties.creation.create_freemocap_empties import create_freemocap_empties
from freemocap_blender_addon.core_functions.load_videos.load_videos import load_videos
from freemocap_blender_addon.core_functions.meshes.attach_mesh_to_rig import attach_mesh_to_rig
from freemocap_blender_addon.core_functions.meshes.center_of_mass.center_of_mass_mesh import create_center_of_mass_mesh
from freemocap_blender_addon.core_functions.meshes.center_of_mass.center_of_mass_trails import \
    create_center_of_mass_trails
from freemocap_blender_addon.core_functions.meshes.skelly_mesh.attach_skelly_mesh import attach_skelly_mesh_to_rig
from freemocap_blender_addon.core_functions.rig.add_rig import generate_rig, AddRigMethods
from freemocap_blender_addon.core_functions.rig.save_bone_and_joint_angles_from_rig import \
    save_bone_and_joint_angles_from_rig
from freemocap_blender_addon.core_functions.setup_scene.make_parent_empties import create_parent_empty
from freemocap_blender_addon.core_functions.setup_scene.set_start_end_frame import set_start_end_frame
from freemocap_blender_addon.freemocap_data_handler.handler import FreemocapDataHandler
from freemocap_blender_addon.freemocap_data_handler.helpers.saver import FreemocapDataSaver
from freemocap_blender_addon.freemocap_data_handler.operations.fix_hand_data import fix_hand_data
from freemocap_blender_addon.freemocap_data_handler.operations.put_skeleton_on_ground import put_skeleton_on_ground
from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
    calculate_rigid_body_trajectories
from freemocap_blender_addon.pipelines.pipeline_parameters.pipeline_parameters import PipelineConfig
from freemocap_blender_addon.utilities.singleton_metaclass import SingletonMetaClass


class MainController(metaclass=SingletonMetaClass):
    def __init__(self,
                 recording_path: str,
                 blend_file_path_str: str,
                 pipeline_config: PipelineConfig):
        self.pipeline_config: PipelineConfig = pipeline_config

        #blender stuff
        self.rig = None
        self.empties = None
        self._data_parent_object = None
        self._empty_parent_object = None
        self._rigid_body_meshes_parent_object = None
        self._video_parent_object = None
        self.blend_file_path_str: str = blend_file_path_str
        self.origin_name = f"{self.recording_name}_origin"
        self.rig_name = f"{self.recording_name}_rig"
        self._create_parent_empties()

        # Core freemocap processing stuff
        self.recording_path_str: str = recording_path
        self.recording_name = Path(self.recording_path_str).stem
        self._output_video_path = str(Path(self.blend_file_path_str).parent / f"{self.recording_name}_video_output.mp4")
        self.freemocap_data_handler: Optional[FreemocapDataHandler] = None


    @property
    def data_parent_object(self):
        return self._data_parent_object

    @property
    def empty_names(self) -> List[str]:
        if self.empties is None:
            raise ValueError("Empties have not been created yet!")
        empty_names = []

        def get_empty_names_from_dict(dictionary):
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    get_empty_names_from_dict(value)  # recursion, baby!
                else:
                    empty_names.append(key)

        get_empty_names_from_dict(self.empties)

        return empty_names

    @property
    def center_of_mass_empty(self):
        if self.empties is None:
            raise ValueError("Empties have not been created yet!")
        return list(self.empties["other"]["center_of_mass"].values())[0]

    def _create_parent_empties(self):
        self._data_parent_object = create_parent_empty(name=self.origin_name,
                                                       display_scale=1.0,
                                                       type="ARROWS")
        self._empty_parent_object = create_parent_empty(
            name="empties_parent",
            parent_object=self._data_parent_object,
            type="PLAIN_AXES",
            display_scale=0.3,
        )
        self._rigid_body_meshes_parent_object = create_parent_empty(
            name="rigid_body_meshes_parent",
            parent_object=self._data_parent_object,
            type="CUBE",
            display_scale=0.2,
        )
        self._video_parent_object = create_parent_empty(
            name="videos_parent",
            parent_object=self._data_parent_object,
            type="IMAGE",
            display_scale=0.1,
        )
        self._center_of_mass_parent_object = create_parent_empty(
            name="center_of_mass_data_parent",
            parent_object=self._data_parent_object,
            type="SPHERE",
            display_scale=0.1,
        )

    def load_freemocap_data(self):
        try:
            print("Loading freemocap data....")
            self.freemocap_data_handler = load_freemocap_data(
                recording_path=self.recording_path_str
            )
            set_start_end_frame(
                number_of_frames=self.freemocap_data_handler.number_of_frames
            )
        except Exception as e:
            print(f"Failed to load freemocap data: {e}")
            raise e

    def calculate_virtual_trajectories(self):
        try:
            print("Calculating virtual trajectories....")
            self.freemocap_data_handler.calculate_virtual_trajectories()
            self.freemocap_data_handler.mark_processing_stage(
                "add_virtual_trajectories"
            )
        except Exception as e:
            print(f"Failed to calculate virtual trajectories: {e}")
            print(e)
            raise e

    def put_data_in_inertial_reference_frame(self):
        try:
            print("Putting freemocap data in inertial reference frame....")
            put_skeleton_on_ground(handler=self.freemocap_data_handler)
        except Exception as e:
            print(
                f"Failed when trying to put freemocap data in inertial reference frame: {e}"
            )
            print(traceback.format_exc())
            raise e

    def enforce_rigid_bones(self):
        print("Enforcing rigid bones...")
        try:
            self.freemocap_data_handler = calculate_rigid_body_trajectories(
                handler=self.freemocap_data_handler
            )

        except Exception as e:
            print(f"Failed during `enforce rigid bones`, error: `{e}`")
            print(e)
            raise e

    def fix_hand_data(self):
        try:
            print("Fixing hand data...")
            self.freemocap_data_handler = fix_hand_data(
                handler=self.freemocap_data_handler
            )
        except Exception as e:
            print(f"Failed during `fix hand data`, error: `{e}`")
            print(e)
            raise e

    def save_data_to_disk(self):
        try:
            print("Saving data to disk...")
            FreemocapDataSaver(handler=self.freemocap_data_handler).save(
                recording_path=self.recording_path_str
            )
        except Exception as e:
            print(f"Failed to save data to disk: {e}")
            print(e)
            raise e

    def create_empties(self):
        try:
            print("Creating keyframed empties....")

            self.empties = create_freemocap_empties(
                handler=self.freemocap_data_handler,
                parent_object=self._empty_parent_object,
                center_of_mass_data_parent=self._center_of_mass_parent_object,
            )
            print(f"Finished creating keyframed empties: {self.empties.keys()}")
        except Exception as e:
            print(f"Failed to create keyframed empties: {e}")

    def add_rig(self):
        try:
            print("Adding rig...")
            self.rig = generate_rig(
                bone_data=self.freemocap_data_handler.metadata["bone_data"],
                rig_name=self.rig_name,
                parent_object=self._data_parent_object,
                add_rig_method=AddRigMethods.BY_BONE,
                keep_symmetry=self.pipeline_config.add_rig.keep_symmetry,
                add_fingers_constraints=self.pipeline_config.add_rig.add_fingers_constraints,
                use_limit_rotation=self.pipeline_config.add_rig.use_limit_rotation,
            )
        except Exception as e:
            print(f"Failed to add rig: {e}")
            print(e)
            raise e

    def save_bone_and_joint_data_from_rig(self):
        if self.rig is None:
            raise ValueError("Rig is None!")
        try:
            print("Saving joint angles...")
            csv_file_path = str(
                Path(self.blend_file_path_str).parent / "saved_data" / f"{self.recording_name}_bone_and_joint_data.csv")
            save_bone_and_joint_angles_from_rig(
                rig=self.rig,
                csv_save_path=csv_file_path,
                start_frame=0,
                end_frame=self.freemocap_data_handler.number_of_frames,
            )
        except Exception as e:
            print(f"Failed to save joint angles: {e}")
            print(e)
            raise e

    def attach_rigid_body_mesh_to_rig(self):
        if self.rig is None:
            raise ValueError("Rig is None!")

        if self.empties is None:
            raise ValueError("Empties have not been created yet!")

        try:
            print("Adding rigid_body_bone_meshes...")
            attach_mesh_to_rig(
                body_mesh_mode=self.pipeline_config.add_body_mesh.body_mesh_mode,
                bone_data=self.freemocap_data_handler.metadata["bone_data"],
                rig=self.rig,
                empties=self.empties,
                parent_object=self._rigid_body_meshes_parent_object,
            )
        except Exception as e:
            print(f"Failed to attach mesh to rig: {e}")
            print(e)
            raise e

    def attach_skelly_mesh_to_rig(self):
        if self.rig is None:
            raise ValueError("Rig is None!")
        try:
            print("Adding Skelly mesh!!! :D")
            body_dimensions = self.freemocap_data_handler.get_body_dimensions()
            attach_skelly_mesh_to_rig(
                rig=self.rig,
                body_dimensions=body_dimensions,
            )
        except Exception as e:
            print(f"Failed to attach mesh to rig: {e}")
            print(e)
            raise e

    def create_center_of_mass_mesh(self):

        try:
            print("Adding Center of Mass Mesh")
            create_center_of_mass_mesh(
                parent_object=self._center_of_mass_parent_object,
                center_of_mass_empty=self.center_of_mass_empty,
            )
        except Exception as e:
            print(f"Failed to attach mesh to rig: {e}")
            print(e)
            raise e

    def create_center_of_mass_trails(self):
        try:
            print("Adding Center of Mass trail meshes")

            create_center_of_mass_trails(
                center_of_mass_trajectory=np.squeeze(self.freemocap_data_handler.center_of_mass_trajectory),
                parent_empty=self._center_of_mass_parent_object,
                tail_past_frames=30,
                trail_future_frames=30,
                trail_starting_width=0.045,
                trail_minimum_width=0.01,
                trail_size_decay_rate=0.8,
                trail_color=(1.0, 0.0, 1.0, 1.0),
            )

        except Exception as e:
            print(f"Failed to attach mesh to rig: {e}")
            print(e)
            raise e

    def add_videos(self):
        try:
            print("Loading videos as planes...")
            load_videos(
                recording_path=self.recording_path_str,
                parent_object=self._video_parent_object,
            )
        except Exception as e:
            print(e)
            print(e)
            raise e

    def setup_scene(self):
        import bpy

        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:  # iterate through areas in current screen
                if area.type == "VIEW_3D":
                    for (
                            space
                    ) in area.spaces:  # iterate through spaces in current VIEW_3D area
                        if space.type == "VIEW_3D":  # check if space is a 3D view
                            space.shading.type = "MATERIAL"

        # self.data_parent_object.hide_set(True)
        self._empty_parent_object.hide_set(True)
        self._rigid_body_meshes_parent_object.hide_set(True)
        self._video_parent_object.hide_set(True)
        self._center_of_mass_parent_object.hide_set(True)

        # remove default cube
        if "Cube" in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects["Cube"])

        # create_scene_objects(scene=bpy.context.scene)

    def create_video(self):
        print("Creating export video...")
        import bpy
        create_video(
            scene=bpy.context.scene,
            recording_folder=self.recording_path_str,
            start_frame=bpy.context.scene.frame_start,
            end_frame=bpy.context.scene.frame_end,
        )

    def save_blender_file(self):
        print("Saving blender file...")
        import bpy

        bpy.ops.wm.save_as_mainfile(filepath=str(self.blend_file_path_str))
        print(f"Saved .blend file to: {self.blend_file_path_str}")

    def run_all(self):
        print("Running all stages...")

        # Pure python stuff
        self.load_freemocap_data()
        self.calculate_virtual_trajectories()
        self.put_data_in_inertial_reference_frame()
        self.enforce_rigid_bones()
        self.fix_hand_data()
        self.save_data_to_disk()

        # Blender stuff
        self.create_empties()
        self.add_rig()
        self.save_bone_and_joint_data_from_rig()
        self.attach_rigid_body_mesh_to_rig()
        self.attach_skelly_mesh_to_rig()
        self.create_center_of_mass_mesh()
        # self.create_center_of_mass_trails()
        self.add_videos()
        self.setup_scene()
        # self.create_video()
        self.save_blender_file()
        # export_fbx(recording_path=recording_path)
