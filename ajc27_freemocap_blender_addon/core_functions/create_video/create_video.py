import time
from pathlib import Path

from ajc27_freemocap_blender_addon.core_functions.setup_scene.scene_objects.cameras.create_cameras import create_cameras
from ajc27_freemocap_blender_addon.core_functions.setup_scene.scene_objects.lights.create_lights import create_lights

import bpy 

def create_video(scene: bpy.types.Scene,
                 recording_folder: str,
                 export_profile: str = 'debug',
                 start_frame: int = 1,
                 end_frame: int = 250) -> None:

    # Set the output file name
    video_file_name = Path(recording_folder).name + '.mp4'
    # Set the output file
    video_render_path = str(Path(recording_folder) / video_file_name)
    bpy.context.scene.render.filepath = video_render_path
    print(f"Exporting video to: {video_render_path} ...")

    # Set the output format to MPEG4
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'

    # Set the codec
    bpy.context.scene.render.ffmpeg.codec = 'H264'

    # Set the start and end frames
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    # Get start time
    start = time.time()

    # Place the required cameras
    cameras_positions = create_cameras(scene, export_profile)

    # Place the required lights
    create_lights(scene, cameras_positions)

    # Rearrange the background videos

    # Render the animation
    bpy.ops.render.render(animation=True)



    if  Path(video_render_path).exists():
        print(f"Video file successfully created at: {video_render_path}")
    else:
        print("ERROR - Video file was not created!! Nothing found at:  {video_render_path} ")
    