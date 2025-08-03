# chats/permissions.py

from rest_framework import permissions


class IsParticipantOfConversation(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True  # placeholder logic for now
