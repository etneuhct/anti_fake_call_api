class UserVirtualPhoneNumberStatus:
    pending = 0
    is_inactive = 1
    is_active = 2


class ConversationHistoryCallingStatus:
    pending = 0
    on_call = 1
    forwarded = 2
    bot_hang_up = 3
    contact_hang_up = 4


class ConversationHistoryAnalysisStatus:
    pending = 0
    is_ok = 1
    scam = 2
