from uuid import UUID

from entity.follow_relationship import FollowRelationship
from exception.service_errors import FollowRelationshipError
from repository import user_profile_repository, follow_relationship_repository, block_relationship_repository


def get_all_follow_requests(profile_id: UUID) -> list[FollowRelationship]:
    return follow_relationship_repository.get_all_pending(profile_id)


def follow_user_profile(source_profile_id: UUID, target_profile_id: UUID):
    source_profile, target_profile = __validate_and_get_profiles(source_profile_id, target_profile_id)

    has_blocked_target = block_relationship_repository.exists_by_profile(
        blocker_profile_id=source_profile_id,
        blocked_profile_id=target_profile_id
    )
    if has_blocked_target:
        raise FollowRelationshipError(f"User profile {target_profile.display_name} ({target_profile.id}) is blocked.")

    is_blocked_by_target = block_relationship_repository.exists_by_profile(
        blocker_profile_id=target_profile_id,
        blocked_profile_id=source_profile_id
    )
    if is_blocked_by_target:
        raise FollowRelationshipError(
            f"Your user profile has been blocked by the user {target_profile.display_name} ({target_profile.id})."
        )

    existing_follow_relationship = follow_relationship_repository.get_by_profile(source_profile.id, target_profile.id)
    if existing_follow_relationship is not None:
        if existing_follow_relationship.is_accepted:
            raise FollowRelationshipError(
                f"Already following user profile {target_profile.display_name} ({target_profile.id})."
            )
        else:
            raise FollowRelationshipError(
                f"Already sent follow request to user profile {target_profile.display_name} ({target_profile.id})."
            )

    follow_relationship = FollowRelationship(source_profile.id, target_profile.id)
    if target_profile.is_private:
        follow_relationship.is_accepted = False

    persisted_entity = follow_relationship_repository.create_new(follow_relationship)

    return persisted_entity


def unfollow_user_profile(source_profile_id: UUID, target_profile_id: UUID):
    existing_follow_relationship = __validate_and_get_relationship(source_profile_id, target_profile_id)

    follow_relationship_repository.delete(existing_follow_relationship)
    if existing_follow_relationship.source_profile.is_private or existing_follow_relationship.target_profile.is_private:
        follow_back_relationship = follow_relationship_repository.get_by_profile(target_profile_id, source_profile_id)
        if follow_back_relationship:
            follow_relationship_repository.delete(follow_back_relationship)

    return existing_follow_relationship


def update_follow_relationship(source_profile_id: UUID, target_profile_id: UUID, is_muted: bool):
    existing_follow_relationship = __validate_and_get_relationship(source_profile_id, target_profile_id)
    if existing_follow_relationship.is_muted == is_muted:
        raise ValueError(f"Invalid action: user profile {target_profile_id} {'already' if is_muted else 'not'} muted.")

    existing_follow_relationship.is_muted = is_muted
    follow_relationship_repository.update(existing_follow_relationship)

    return existing_follow_relationship


def update_follow_request(follow_relationship_id: UUID, current_user_profile_id: UUID, is_accepted: bool):
    existing_follow_relationship = follow_relationship_repository.get_by_id(follow_relationship_id)
    if not existing_follow_relationship:
        raise FollowRelationshipError(f"Follow request {follow_relationship_id} not found.")
    if existing_follow_relationship.target_profile_id != current_user_profile_id:
        raise FollowRelationshipError(f"Follow request {follow_relationship_id} not found.")
    if existing_follow_relationship.is_accepted:
        raise FollowRelationshipError(f"Follow request {follow_relationship_id} already accepted.")

    if not is_accepted:
        follow_relationship_repository.delete(existing_follow_relationship)
        return existing_follow_relationship

    existing_follow_relationship.is_accepted = True
    source_profile, target_profile = __validate_and_get_profiles(
        existing_follow_relationship.source_profile_id, existing_follow_relationship.target_profile_id
    )
    follow_relationship_repository.update(existing_follow_relationship)

    if existing_follow_relationship.source_profile.is_private or existing_follow_relationship.target_profile.is_private:
        followback_relationship = FollowRelationship(target_profile.id, source_profile.id)
        persisted_entity = follow_relationship_repository.create_new(followback_relationship)

        return persisted_entity


def __validate_and_get_relationship(source_profile_id: UUID, target_profile_id: UUID):
    source_profile, target_profile = __validate_and_get_profiles(source_profile_id, target_profile_id)

    existing_follow_relationship = follow_relationship_repository.get_by_profile(
        source_profile_id=source_profile.id,
        target_profile_id=target_profile.id
    )

    if existing_follow_relationship is None:
        raise FollowRelationshipError(
            f"Invalid user profile ID: not following user profile {target_profile.display_name} ({target_profile.id})."
        )

    return existing_follow_relationship


def __validate_and_get_profiles(source_profile_id: UUID, target_profile_id: UUID):
    if source_profile_id == target_profile_id:
        raise FollowRelationshipError("Invalid user profile ID: action not permitted on own user profile.")

    source_profile = user_profile_repository.get_by_id(source_profile_id)
    if source_profile is None:
        raise FollowRelationshipError(f"Invalid user profile ID: user profile {source_profile_id} not found.")
    target_profile = user_profile_repository.get_by_id(target_profile_id)
    if target_profile is None:
        raise FollowRelationshipError(f"Invalid user profile ID: user profile {target_profile_id} not found.")

    return source_profile, target_profile
