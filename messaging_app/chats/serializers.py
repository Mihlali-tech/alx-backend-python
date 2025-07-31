from rest_framework import serializers
from .models import User, Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.CharField(source='sender.email', read_only=True)  # ✅ CharField

    class Meta:
        model = Message
        fields = ['message_id', 'sender_email', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()  # ✅ SerializerMethodField
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_participants(self, obj):
        return [user.email for user in obj.participants.all()]


class UserSerializer(serializers.ModelSerializer):
    conversations = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'created_at', 'conversations']

    def get_conversations(self, obj):
        return [str(convo.conversation_id) for convo in obj.conversations.all()]


# ✅ Optional: Add example of using ValidationError for completeness (even if not yet used)
from rest_framework import serializers

def validate_email_unique(value):
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError("Email already in use.")  # ✅ ValidationError
    return value