from rest_framework import serializers
from .models import DoctorInfo, Leave

class DoctorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorInfo
        fields = ['id', 'dob', 'specialization', 'degree', 'experience','description','address','phone_no']
        # read_only=[' user']

class DoctorInfoGetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = DoctorInfo
        fields = ['id', 'username', 'dob', 'specialization', 'degree', 'experience', 'description', 'address', 'phone_no']

class LeaveSerializer(serializers.ModelSerializer):
    doctor_info = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Leave
        fields = ['id', 'doctor_info', 'starting_date', 'ending_date', 'phone_no']

from .models import Booking

class TimeSlotSerializer(serializers.Serializer):
    date = serializers.DateField()
    time_slots = serializers.ListField(child=serializers.TimeField())

class BookingSerializer(serializers.ModelSerializer):
    doctor_info = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    time_slots = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'start_date', 'end_date', 'starting_time', 'ending_time', 'time_slot_duration', 'doctor_info', 'time_slots']

    def get_time_slots(self, obj):
        time_slots = obj.generate_time_slots()
        serialized_time_slots = []
        for date, slots in time_slots.items():
            serialized_time_slots.append({
                'date': date,
                'time_slots': slots,
            })
        return serialized_time_slots