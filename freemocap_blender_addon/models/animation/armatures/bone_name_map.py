"""
Dictionary to map the default armature bone names with the different
armatures bone names.
"""

bone_name_map = {
    "armature_ue_metahuman_simple": {
        "pelvis": "pelvis",
        "pelvis.R": "pelvis_r",
        "pelvis.L": "pelvis_l",
        "spine": "spine_01",
        "spine.001": "spine_04",
        "neck": "neck_01",
        "face": "face",
        "shoulder.R": "clavicle_r",
        "shoulder.L": "clavicle_l",
        "upper_arm.R": "upperarm_r",
        "upper_arm.L": "upperarm_l",
        "forearm.R": "lowerarm_r",
        "forearm.L": "lowerarm_l",
        "hand.R": "hand_r",
        "hand.L": "hand_l",
        "thumb.carpal.R": "thumb_metacarpal_r",
        "palm.01.R": "index_metacarpal_r",
        "palm.02.R": "middle_metacarpal_r",
        "palm.03.R": "ring_metacarpal_r",
        "palm.04.R": "pinky_metacarpal_r",
        "thumb.carpal.L": "thumb_metacarpal_l",
        "palm.01.L": "index_metacarpal_l",
        "palm.02.L": "middle_metacarpal_l",
        "palm.03.L": "ring_metacarpal_l",
        "palm.04.L": "pinky_metacarpal_l",
        "thumb.01.R": "thumb_01_r",
        "thumb.01.L": "thumb_01_l",
        "thumb.02.R": "thumb_02_r",
        "thumb.02.L": "thumb_02_l",
        "thumb.03.R": "thumb_03_r",
        "thumb.03.L": "thumb_03_l",
        "f_index.01.R": "index_01_r",
        "f_index.01.L": "index_01_l",
        "f_index.02.R": "index_02_r",
        "f_index.02.L": "index_02_l",
        "f_index.03.R": "index_03_r",
        "f_index.03.L": "index_03_l",
        "f_middle.01.R": "middle_01_r",
        "f_middle.01.L": "middle_01_l",
        "f_middle.02.R": "middle_02_r",
        "f_middle.02.L": "middle_02_l",
        "f_middle.03.R": "middle_03_r",
        "f_middle.03.L": "middle_03_l",
        "f_ring.01.R": "ring_01_r",
        "f_ring.01.L": "ring_01_l",
        "f_ring.02.R": "ring_02_r",
        "f_ring.02.L": "ring_02_l",
        "f_ring.03.R": "ring_03_r",
        "f_ring.03.L": "ring_03_l",
        "f_pinky.01.R": "pinky_01_r",
        "f_pinky.01.L": "pinky_01_l",
        "f_pinky.02.R": "pinky_02_r",
        "f_pinky.02.L": "pinky_02_l",
        "f_pinky.03.R": "pinky_03_r",
        "f_pinky.03.L": "pinky_03_l",
        "thigh.R": "thigh_r",
        "thigh.L": "thigh_l",
        "shin.R": "calf_r",
        "shin.L": "calf_l",
        "foot.R": "foot_r",
        "foot.L": "foot_l",
        "heel.02.R": "heel_r",
        "heel.02.L": "heel_l",
        "hand.IK.R": "hand.IK.R",
        "hand.IK.L": "hand.IK.L",
        "foot.IK.R": "foot.IK.R",
        "foot.IK.L": "foot.IK.L",
        "arm_pole_target.R": "arm_pole_target.R",
        "arm_pole_target.L": "arm_pole_target.L",
        "leg_pole_target.R": "leg_pole_target.R",
        "leg_pole_target.L": "leg_pole_target.L",
    },
    "armature_freemocap": {
        "pelvis": "pelvis",
        "pelvis.R": "pelvis.R",
        "pelvis.L": "pelvis.L",
        "spine": "spine",
        "spine.001": "spine.001",
        "neck": "neck",
        "face": "face",
        "shoulder.R": "shoulder.R",
        "shoulder.L": "shoulder.L",
        "upper_arm.R": "upper_arm.R",
        "upper_arm.L": "upper_arm.L",
        "forearm.R": "forearm.R",
        "forearm.L": "forearm.L",
        "hand.R": "hand.R",
        "hand.L": "hand.L",
        "thumb.carpal.R": "thumb.carpal.R",
        "palm.01.R": "palm.01.R",
        "palm.02.R": "palm.02.R",
        "palm.03.R": "palm.03.R",
        "palm.04.R": "palm.04.R",
        "thumb.carpal.L": "thumb.carpal.L",
        "palm.01.L": "palm.01.L",
        "palm.02.L": "palm.02.L",
        "palm.03.L": "palm.03.L",
        "palm.04.L": "palm.04.L",
        "thumb.01.R": "thumb.01.R",
        "thumb.01.L": "thumb.01.L",
        "thumb.02.R": "thumb.02.R",
        "thumb.02.L": "thumb.02.L",
        "thumb.03.R": "thumb.03.R",
        "thumb.03.L": "thumb.03.L",
        "f_index.01.R": "f_index.01.R",
        "f_index.01.L": "f_index.01.L",
        "f_index.02.R": "f_index.02.R",
        "f_index.02.L": "f_index.02.L",
        "f_index.03.R": "f_index.03.R",
        "f_index.03.L": "f_index.03.L",
        "f_middle.01.R": "f_middle.01.R",
        "f_middle.01.L": "f_middle.01.L",
        "f_middle.02.R": "f_middle.02.R",
        "f_middle.02.L": "f_middle.02.L",
        "f_middle.03.R": "f_middle.03.R",
        "f_middle.03.L": "f_middle.03.L",
        "f_ring.01.R": "f_ring.01.R",
        "f_ring.01.L": "f_ring.01.L",
        "f_ring.02.R": "f_ring.02.R",
        "f_ring.02.L": "f_ring.02.L",
        "f_ring.03.R": "f_ring.03.R",
        "f_ring.03.L": "f_ring.03.L",
        "f_pinky.01.R": "f_pinky.01.R",
        "f_pinky.01.L": "f_pinky.01.L",
        "f_pinky.02.R": "f_pinky.02.R",
        "f_pinky.02.L": "f_pinky.02.L",
        "f_pinky.03.R": "f_pinky.03.R",
        "f_pinky.03.L": "f_pinky.03.L",
        "thigh.R": "thigh.R",
        "thigh.L": "thigh.L",
        "shin.R": "shin.R",
        "shin.L": "shin.L",
        "foot.R": "foot.R",
        "foot.L": "foot.L",
        "heel.02.R": "heel.02.R",
        "heel.02.L": "heel.02.L",
        "hand.IK.R": "hand.IK.R",
        "hand.IK.L": "hand.IK.L",
        "foot.IK.R": "foot.IK.R",
        "foot.IK.L": "foot.IK.L",
        "arm_pole_target.R": "arm_pole_target.R",
        "arm_pole_target.L": "arm_pole_target.L",
        "leg_pole_target.R": "leg_pole_target.R",
        "leg_pole_target.L": "leg_pole_target.L",
    },
}
