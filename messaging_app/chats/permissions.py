from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants of the conversation.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for participants
        if request.method in permissions.SAFE_METHODS:
            # For messages, check if user in conversation participants
            if hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
            # For conversations
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()

        # For unsafe methods (PUT, PATCH, DELETE) check user participation strictly
        if request.method in ("PUT", "PATCH", "DELETE"):
            if hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()

        # Deny by default
        return False
