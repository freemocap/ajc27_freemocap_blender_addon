import numpy as np

from freemocap_blender_addon.models.skeleton_model import SkeletonTypes
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.tracked_point_keypoint_types import \
    KeypointTrajectories, SegmentStats
from freemocap_blender_addon.utilities.print_table_from_dicts import print_table
from freemocap_blender_addon.utilities.sample_statistics import DescriptiveStatistics


def calculate_segment_lengths(keypoint_trajectories: KeypointTrajectories,
                              skeleton_definition: SkeletonTypes) -> SegmentStats:
    segment_stats = {}
    for segment in skeleton_definition.value.get_segments():
        length_stats = calculate_distance_between_trajectories(
            trajectory_1=keypoint_trajectories[segment.value.parent.name.lower()].data,
            trajectory_2=keypoint_trajectories[segment.value.child.name.lower()].data
        )

        segment_stats[segment.name.lower()] = DescriptiveStatistics.from_samples(length_stats)

    return segment_stats


def calculate_distance_between_trajectories(trajectory_1: np.ndarray,
                                            trajectory_2: np.ndarray) -> np.ndarray:
    """
    Compute the Euclidean distances between corresponding entries of two 3D trajectories.

    Parameters
    ----------
    trajecotry_1 : np.ndarray
        The first trajectory, a 2D array of shape (n, 3) where n is the number of points.
    trajecotry_2 : np.ndarray
        The second trajectory, a 2D array of shape (n, 3) where n is the number of points.

    Returns
    -------
    np.ndarray
        A 1D array of length n containing the distances between corresponding points in the two trajectories.

    Raises
    ------
    ValueError
        If the input arrays do not have the same shape.

    Examples
    --------
    >>> trajecotry_1 = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    >>> trajecotry_2 = np.array([[1, 0, 0], [0, 1, 1], [2, 3, 2]])
    >>> compute_trajectory_distances(trajecotry_1, trajecotry_2)
    array([1.        , 1.41421356, 1.        ])
    """
    if trajectory_1.shape != trajectory_2.shape:
        raise ValueError(
            f"Both trajectories must have the same shape, Trajectory 1 shape: {trajectory_1.shape}, Trajectory 2 shape: {trajectory_2.shape}")

    return np.linalg.norm(trajectory_1 - trajectory_2, axis=1)


def print_length_stats(segment_lengths: SegmentStats):
    stats = []
    for name, segment in segment_lengths.items():
        segment_dict = {'segment': name}
        segment_dict.update(segment.to_dict())
        stats.append(segment_dict)
    print_table(stats)


if __name__ == "__main__":
    from freemocap_blender_addon.freemocap_data.freemocap_recording_data import load_freemocap_rest_recording

    recording_data = load_freemocap_rest_recording()
    keypoint_trajectories_outer = recording_data.body.map_to_keypoints()
    segment_lengths = calculate_segment_lengths(keypoint_trajectories=keypoint_trajectories_outer, skeleton_definition=SkeletonTypes.BODY_ONLY)

    print_length_stats(segment_lengths)

