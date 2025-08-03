from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email']

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()

    def get_queryset(self):
        # Limit conversations to those the user participates in
        return Conversation.objects.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        if not conversation_id:
            return Message.objects.none()  # No conversation_id -> no messages
        conversation = get_object_or_404(Conversation, id=conversation_id)

        # Check if user is participant - if not, forbid
        if self.request.user not in conversation.participants.all():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(detail="You do not have permission to view messages in this conversation.")

        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation_id')
        conversation = get_object_or_404(Conversation, id=conversation_id)

        # Check user is participant before sending
        if self.request.user not in conversation.participants.all():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(detail="You cannot send messages to a conversation you are not part of.")

        serializer.save(sender=self.request.user, conversation=conversation)
