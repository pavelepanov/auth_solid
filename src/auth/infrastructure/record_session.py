from dataclasses import dataclass
from datetime import datetime

from auth.domain.user.value_objects import UserId


@dataclass(eq=False, kw_only=True)
class SessionRecord:
    id_: str
    user_id: UserId
    expiration: datetime
    