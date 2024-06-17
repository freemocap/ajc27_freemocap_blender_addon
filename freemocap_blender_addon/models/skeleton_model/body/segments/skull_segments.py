from enum import Enum

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import SkullKeypoints
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.segments_abc import SimpleSegmentABC, \
    CompoundSegmentABC
from freemocap_blender_addon.utilities.blenderize_name import blenderize_name


class SkullSegment(CompoundSegmentABC):
    parent = SkullKeypoints.SKULL_CENTER_ATLAS_C1
    children = [SkullKeypoints.NOSE_TIP,
                # SkullKeypoints.SKULL_TOP_BREGMA,
                SkullKeypoints.RIGHT_EYE_INNER,
                SkullKeypoints.RIGHT_EYE_CENTER,
                SkullKeypoints.RIGHT_EYE_OUTER,
                SkullKeypoints.RIGHT_EAR_TRAGUS,
                SkullKeypoints.RIGHT_MOUTH,
                SkullKeypoints.LEFT_EYE_INNER,
                SkullKeypoints.LEFT_EYE_CENTER,
                SkullKeypoints.LEFT_EYE_OUTER,
                SkullKeypoints.LEFT_EAR_TRAGUS,
                SkullKeypoints.LEFT_MOUTH]

    shared_keypoint = SkullKeypoints.SKULL_CENTER_ATLAS_C1
    positive_x = SkullKeypoints.NOSE_TIP
    approximate_positive_y = SkullKeypoints.LEFT_EAR_TRAGUS


class SkullNoseSegment(SimpleSegmentABC):
    parent = SkullKeypoints.SKULL_CENTER_ATLAS_C1
    child = SkullKeypoints.NOSE_TIP


# class SkullTopSegment(SimpleSegmentABC):
#     parent = SkullKeypoints.SKULL_CENTER_C1
#     child = SkullKeypoints.SKULL_TOP_BREGMA


class SkullRightEyeInnerSegment(SimpleSegmentABC):
    parent = SkullKeypoints.SKULL_CENTER_ATLAS_C1
    child = SkullKeypoints.RIGHT_EYE_INNER


class SkullRightEyeCenterSegment(SimpleSegmentABC):
    parent = SkullKeypoints.SKULL_CENTER_ATLAS_C1
    child = SkullKeypoints.RIGHT_EYE_CENTER


class SkullRightEyeOuterSegment(SimpleSegmentABC):
    parent = SkullKeypoints.SKULL_CENTER_ATLAS_C1
    child = SkullKeypoints.RIGHT_EYE_OUTER


class SkullRightEarTragusSegment(SimpleSegmentABC):
    parent = SkullKeypoints.SKULL_CENTER_ATLAS_C1
    child = SkullKeypoints.RIGHT_EAR_TRAGUS


class SkullRightMouthSegment(SimpleSegmentABC):
    parent = SkullKeypoints.SKULL_CENTER_ATLAS_C1
    child = SkullKeypoints.RIGHT_MOUTH


class SkullLeftEyeInnerSegment(SimpleSegmentABC):
    parent = SkullKeypoints.SKULL_CENTER_ATLAS_C1
    child = SkullKeypoints.LEFT_EYE_INNER


class SkullLeftEyeCenterSegment(SimpleSegmentABC):
    parent = SkullKeypoints.SKULL_CENTER_ATLAS_C1
    child = SkullKeypoints.LEFT_EYE_CENTER


class SkullLeftEyeOuterSegment(SimpleSegmentABC):
    parent = SkullKeypoints.SKULL_CENTER_ATLAS_C1
    child = SkullKeypoints.LEFT_EYE_OUTER


class SkullLeftEarTragusSegment(SimpleSegmentABC):
    parent = SkullKeypoints.SKULL_CENTER_ATLAS_C1
    child = SkullKeypoints.LEFT_EAR_TRAGUS


class SkullLeftMouthSegment(SimpleSegmentABC):
    parent = SkullKeypoints.SKULL_CENTER_ATLAS_C1
    child = SkullKeypoints.LEFT_MOUTH


class SkullSegments(Enum):
    # TODO - go even harder on the naming convention - https://www.sciencedirect.com/science/article/pii/S0169260721004545
    # COMPOUND: CompoundSegmentABC = SkullSegment
    NOSE: SimpleSegmentABC = SkullNoseSegment
    # TOP: SimpleSegmentABC = SkullTopSegment
    RIGHT_EYE_INNER: SimpleSegmentABC = SkullRightEyeInnerSegment
    RIGHT_EYE_CENTER: SimpleSegmentABC = SkullRightEyeCenterSegment
    RIGHT_EYE_OUTER: SimpleSegmentABC = SkullRightEyeOuterSegment
    RIGHT_EAR_TRAGUS: SimpleSegmentABC = SkullRightEarTragusSegment
    RIGHT_MOUTH: SimpleSegmentABC = SkullRightMouthSegment
    LEFT_EYE_INNER: SimpleSegmentABC = SkullLeftEyeInnerSegment
    LEFT_EYE_CENTER: SimpleSegmentABC = SkullLeftEyeCenterSegment
    LEFT_EYE_OUTER: SimpleSegmentABC = SkullLeftEyeOuterSegment
    LEFT_EAR_TRAGUS: SimpleSegmentABC = SkullLeftEarTragusSegment
    LEFT_MOUTH: SimpleSegmentABC = SkullLeftMouthSegment


BlenderizedSkullSegments = Enum("BlenderizedSkullSegments",
                                {name: blenderize_name(name) for name in list(SkullSegments.__members__.keys())})

# Example usage
if __name__ == "__main__":
    print("\n".join([f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}" for rb in
                     list(SkullSegments)]))

    print("Blenderized Skull Segments:")
    print("\n".join([f"{sk.name}: {sk.value}" for sk in list(BlenderizedSkullSegments)]))
