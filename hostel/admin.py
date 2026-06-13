from django.contrib import admin
from .models import Contact, Student, Complaint, Payment, RentPaymentHistory,Attendance
import csv
from django.http import HttpResponse
from .models import LeaveRequest
from .models import HostelIncharge


# Register your models here.

# admin.site.register(Student)
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user','name', 'room_no', 'phone', 'email', 'join_date')
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=students.csv'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Room No', 'Mobile', 'Email', 'Gender', 'Address', 'Join Date'])
        
        for student in queryset:
            writer.writerow([student.name, 
                             student.room_no, 
                             student.phone, 
                             student.email, 
                             student.gender, 
                             student.address, 
                             student.join_date])

        return response

    export_as_csv.short_description = "Export Selected Students to CSV"

admin.site.register(Complaint)
admin.site.register(Payment)
admin.site.register(RentPaymentHistory)
admin.site.register(Contact)
admin.site.register(Attendance)
admin.site.register(LeaveRequest)
admin.site.register(HostelIncharge)


from django.contrib import admin
from .models import Holiday

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'holiday_type',
        'start_date',
        'end_date'
    )
    list_filter = ('holiday_type',)
    search_fields = ('title',)
    
    
from .models import AttendanceNotification

admin.site.register(AttendanceNotification)