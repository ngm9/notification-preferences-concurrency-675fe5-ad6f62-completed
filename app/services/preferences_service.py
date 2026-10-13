from uuid import UUID
from typing import Optional
from app.models.preferences import NotificationPreferences, PreferencesUpdateRequest
from app.repositories.preferences_repository import get_preferences_by_user, update_preferences


def fetch_user_preferences(user_id: UUID, tenant_id: str) -> Optional[NotificationPreferences]:
    return get_preferences_by_user(user_id, tenant_id)


def apply_preference_updates(
    user_id: UUID,
    request: PreferencesUpdateRequest,
    tenant_id: str
) -> Optional[NotificationPreferences]:
    updates = request.model_dump(exclude_none=True)
    return update_preferences(user_id, updates, tenant_id)
