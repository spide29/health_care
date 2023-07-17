import datetime
from rest_framework import serializers
from .models import DoctorInfo, Leave
from datetime import datetime

class DoctorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorInfo
        fields = ['id', 'dob', 'specialization', 'degree', 'experience','description','address','state','phone_no']
        # read_only=[' user']

class DoctorInfoGetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = DoctorInfo
        fields = ['id', 'username', 'dob', 'specialization', 'degree', 'experience', 'description', 'address','state','phone_no']

class LeaveSerializer(serializers.ModelSerializer):
    doctor_info = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Leave
        fields = ['id', 'doctor_info', 'starting_date', 'ending_date']

from .models import Booking

class TimeSlotSerializer(serializers.Serializer):
    date = serializers.DateField()
    time_slots = serializers.ListField(child=serializers.TimeField())



class TwelveHourTimeField(serializers.Field):
    def to_internal_value(self, value):
        try:
            return datetime.strptime(value, "%I:%M %p").time()
        except ValueError:
            raise serializers.ValidationError("Invalid time format. Please use the format 'HH:MM AM/PM'.")

    def to_representation(self, value):
        return value.strftime("%I:%M %p")

class BookingSerializer(serializers.ModelSerializer):
    doctor_first_name = serializers.ReadOnlyField(source='doctor_info.user.first_name')
    doctor_last_name = serializers.ReadOnlyField(source='doctor_info.user.last_name')
    doctor_info = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    time_slots = serializers.SerializerMethodField()
    starting_time = TwelveHourTimeField()  # Use custom field for starting_time
    ending_time = TwelveHourTimeField()  # Use custom field for ending_time

    class Meta:
        model = Booking
        fields = ['id', 'start_date', 'end_date', 'starting_time', 'ending_time', 'time_slot_duration', 'doctor_info', 'doctor_first_name', 'doctor_last_name', 'time_slots']
    
    def get_time_slots(self, obj):
        time_slots = obj.generate_time_slots()
        formatted_time_slots = []
        for date, slots in time_slots.items():
            formatted_slots = []
            for slot in slots:
                formatted_slots.append(datetime.strptime(slot, '%H:%M:%S').strftime('%I:%M %p'))
            formatted_time_slots.append({'date': date, 'time_slots': formatted_slots})
        return formatted_time_slots

    def get_start_time(self, obj):
        return obj.starting_time.strftime('%I:%M %p')

    def get_end_time(self, obj):
        return obj.ending_time.strftime('%I:%M %p')

# class BookingSerializer(serializers.ModelSerializer):
#     doctor_first_name = serializers.ReadOnlyField(source='doctor_info.user.first_name')
#     doctor_last_name = serializers.ReadOnlyField(source='doctor_info.user.last_name')
#     doctor_info = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
#     time_slots = serializers.SerializerMethodField()

#     class Meta:
#         model = Booking
#         fields = ['id', 'start_date', 'end_date', 'starting_time', 'ending_time', 'time_slot_duration', 'doctor_info', 'doctor_first_name', 'doctor_last_name', 'time_slots']

    def get_time_slots(self, obj):
        time_slots = obj.generate_time_slots()
        serialized_time_slots = []
        for date, slots in time_slots.items():
            serialized_time_slots.append({
                'date': date,
                'time_slots': slots,
            })
        return serialized_time_slots
    
class BookingUpdateSerializer(serializers.ModelSerializer):
    doctor_first_name = serializers.ReadOnlyField(source='doctor_info.user.first_name')
    doctor_last_name = serializers.ReadOnlyField(source='doctor_info.user.last_name')
    doctor_info = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    time_slots = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'starting_time', 'ending_time', 'time_slot_duration','doctor_info' ,'doctor_first_name', 'doctor_last_name', 'time_slots']

    def get_time_slots(self, obj):
        time_slots = obj.generate_time_slots()
        serialized_time_slots = []
        for date, slots in time_slots.items():
            serialized_time_slots.append({
                'date': date,
                'time_slots': slots,
            })
        return serialized_time_slots