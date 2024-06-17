from freemocap_blender_addon.models.skeleton_model.body.linkages.left_body_linkages import LeftShoulderLinkage, \
    LeftElbowLinkage, LeftAnkleLinkage, LeftKneeLinkage, LeftHipLinkage, LeftWristLinkage
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.chain_abc import ChainABC


class LeftArmChain(ChainABC):
    parent = LeftShoulderLinkage
    children = [LeftElbowLinkage,
                LeftWristLinkage,
                ]


class LeftLegChain(ChainABC):
    parent = LeftHipLinkage
    children = [LeftKneeLinkage,
                LeftAnkleLinkage,
                ]
