from conversation.constants import ConversationHistoryCallingStatus, \
    ConversationHistoryAnalysisStatus
from conversation.models import ConversationHistory, Contact, \
    UserVirtualPhoneNumber


class TwilioConversationService:

    @staticmethod
    def create_conversation_history(conversation_uid, twilio_phone_number: str, contact_phone_number: str):
        """
        Permet de creer une conversation a partir du numero de twilio & du numero de l'appelant
        """

        user_virtual_phone_number: UserVirtualPhoneNumber = UserVirtualPhoneNumber.get_by_virtual_phone_number(
            twilio_phone_number)

        contact, _ = Contact.objects.get_or_create(
            phone_number=contact_phone_number,
            user=user_virtual_phone_number.user_phone_number.user
        )

        conversation_history, _ = ConversationHistory.objects.get_or_create(
            id=conversation_uid,
            user_virtual_phone_number=user_virtual_phone_number,
            contact=contact
        )
        return conversation_history

    @staticmethod
    def get_user_phone_number(twilio_phone_number):
        """
        Recupere le numero de l'utilisateur a partir d'un numero twilio - use case: redirection
        """
        user_virtual_phone_number: UserVirtualPhoneNumber = UserVirtualPhoneNumber.get_by_virtual_phone_number(
            twilio_phone_number)
        return user_virtual_phone_number.user_phone_number.phone_number
    
    @staticmethod
    def get_user_phone_number_from_conversation(conversation_uuid):
        """
        Recupere le numero de l'utilisateur a partir d'une conversation
        """
        user_virtual_phone_number: UserVirtualPhoneNumber = ConversationHistory.objects.get(id=conversation_uuid).user_virtual_phone_number
        return user_virtual_phone_number.user_phone_number.phone_number

    @staticmethod
    def set_conversation_calling_status(conversation_uuid, conversation_status: ConversationHistoryCallingStatus):
        conversation = ConversationHistory(id=conversation_uuid)
        conversation.calling_status = conversation_status
        conversation.save()

    @staticmethod
    def set_conversation_analysis_status(conversation_uuid, analysis_status: ConversationHistoryAnalysisStatus):
        conversation = ConversationHistory(id=conversation_uuid)
        conversation.analysis_status = analysis_status
        conversation.save()

    @staticmethod
    def set_conversation_insights(conversation_uuid, insights_data: dict):
        conversation = ConversationHistory(id=conversation_uuid)
        conversation.insights = insights_data
        conversation.save()

    @staticmethod
    def set_conversation_transcription(conversation_uuid, transcription_data: dict):
        conversation = ConversationHistory(id=conversation_uuid)
        conversation.conversations = transcription_data
        conversation.save()
    
    @staticmethod
    def update_conversation(conversation_uuid,
                              calling_status: ConversationHistoryCallingStatus = None,
                              analysis_status: ConversationHistoryAnalysisStatus = None,
                              insights_data: dict = None,
                              transcription_data: dict = None):
        
        updated_count = ConversationHistory.objects.filter(id=conversation_uuid).update(
            calling_status = calling_status,
            analysis_status = analysis_status,
            insights = insights_data,
            conversations = transcription_data
        )
        assert updated_count == 1
