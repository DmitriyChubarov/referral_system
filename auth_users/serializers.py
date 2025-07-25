from rest_framework import serializers
from users.models import User

class ProfileSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'invited_code', 'invited_users']

    def get_invited_users(self, obj):
        if not obj.invite_code:
            return []
        invited = User.objects.filter(invited_code=obj.invite_code)
        return [u.phone_number for u in invited]
