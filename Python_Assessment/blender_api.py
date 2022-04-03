# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 08:09:28 2022

Blender Integration

Automatic loading the downloaded video clips & the transcripts into blender timeline.

   Duration  Number of Frames based from (30fps)
    #1: 3sec   1 -  90 (30fps)
    #2: 5sec  91 - 151 (30fps)
    #3: 4sec 152 - 272 (30fps)
    #4: 4sec 273 - 393 (30fps)
    #5: 4sec 394 - 514 (30fps)
    #6: 3sec 515 - 605 (30fps)
    #7: 4sec 606 - 726 (30fps)

@author: Jeremy G. Olanda

"""

import os
import bpy
    
    
def blender_api():
        
    current_path = "/Python_Assessment/videos/"            
    video_files = [ f for f in os.listdir(current_path) if os.path.isfile(os.path.join(current_path,f)) ]        
    frame_pos1 = [1, 91, 152, 273, 394, 515, 606]
    frame_pos2 = [90, 151, 272, 393, 514, 605, 726]
    subtitles = ["Yes. There's still time.",
                  "It's still part of the fundamental laws of nature even in that part of the universe.",
                  "It's just that events that happen in that empty universe",
                  "don't have casuality",
                  "don't have memory",
                  "don't have progress",
                  "and don't have aging or metabolism or anything like"
                  ]
    
    bpy.context.preferences.view.show_splash = False    
    bpy.ops.wm.read_homefile(app_template='Video_Editing')    
    bpy.data.screens['Video Editing'].areas[3].type = 'PROPERTIES'
    
    scene = bpy.context.scene
    if not scene.sequence_editor:
        scene.sequence_editor_create()
    
    wm = bpy.context.window_manager
    wm.progress_begin(0, 100.0)    
    bpy.ops.sequencer.select_all(action='DESELECT')
    
    ch1 = 1
    ch2 = 2
    for vid,sub,fp1,fp2 in zip(video_files, subtitles, frame_pos1, frame_pos2):
        scene.sequence_editor.sequences.new_movie(
            name="Video", 
            filepath=current_path+vid, 
            channel=ch1,
            frame_start=fp1)
        
        text_strip = scene.sequence_editor.sequences.new_effect(
            name='Subtitle',
            type="TEXT",
            channel=ch2,
            frame_start=fp1,
            frame_end=fp2
            )
        text_strip.font_size = 38
        text_strip.text = sub 
        text_strip.use_shadow = True
        text_strip.wrap_width = 0.0
        text_strip.select = True
        text_strip.location[1] = 0.1
        text_strip.blend_type = 'ALPHA_OVER'

if __name__ == "__main__":
    blender_api()   
