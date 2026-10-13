from uuid import UUID
from typing import Optional
from app.database import get_db
from app.models.preferences import NotificationPreferences


def get_preferences_by_user(user_id: UUID, tenant_id: str) -> Optional[NotificationPreferences]:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT user_id, tenant_id, email_enabled, sms_enabled, push_enabled, frequency, version "
                "FROM notification_preferences WHERE user_id = %s and tenant_id = %s",
                (str(user_id),tenant_id),
            )
            row = cur.fetchone()
            if not row:
                return None
            return NotificationPreferences(**row)


def update_preferences(user_id: UUID, updates: dict, tenant_id:str) -> Optional[NotificationPreferences]:
    if not len(updates):
        return get_preferences_by_user(user_id, tenant_id)

    set_clauses = ", ".join([f"{key} = %s" for key in updates])
    values = list(updates.values())

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE notification_preferences SET {set_clauses}, updated_at = NOW() "
                f"WHERE user_id = %s and tenant_id = %s""
                f"RETURNING user_id, tenant_id, email_enabled, sms_enabled, push_enabled, frequency, version",
                (str(user_id),tenant_id),
            )
            row = cur.fetchone()
            if not row:
                return None
            return NotificationPreferences(**row)
