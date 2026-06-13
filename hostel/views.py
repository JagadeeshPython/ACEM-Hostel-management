from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
import csv
from hostel.models import Complaint, Contact, Student, RentPaymentHistory
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import time
from .models import Attendance

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Student, LeaveRequest
from .forms import LeaveRequestForm
from .models import Student, HostelIncharge
from .models import Outpass



@login_required(login_url='student_login')
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Session expired or profile missing. Please login again.")
        logout(request)
        return redirect('login')

    return render(request, 'student_dashboard.html', {'student': student})

# Create your views here.

#  for csv files
def export_stud_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    
    # Write header row
    writer.writerow(['Name', 'Room No', 'Mobile', 'Email', 'Gender', 'Address', 'Join Date'])

    # Write data rows
    students = Student.objects.all()
    for student in students:
        writer.writerow([student.name, student.room_no, student.phone, student.email, student.gender, student.address, student.join_date])

    return response


def landing(request):
    return render(request, "landing_page.html")

def home(request):
    return render(request, "index.html")

def rent(request):
    return render(request, "room&facilities.html")

def services(request):
    return render(request, "services.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        num = request.POST.get("number")
        mail = request.POST.get("email")
        msg = request.POST.get("msg")

        Contact.objects.create(
            name=name,
            mobile_number=num,
            visitor_email=mail,
            msg=msg
        )
        messages.success(request, "Thanks for Contacting us. We'll be in touch soon.")
        return redirect("contact")
    return render(request, "contact.html")

# def student_login(request):
#     if request.user.is_authenticated:
#         return redirect('student_dashboard')

#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request,user) # Logs the user in (creates session)
#             messages.success(request, "Login Successful!")
#             return redirect("student_dashboard")
#         else:
#             messages.error(request, "Invalid username or password")

#     return render(request, "student_login.html")  # if request is GET it shows login form again.

def student_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('student_login')

def student_profile(request):
    # student = get_object_or_404(Student, user=request.user)
    # student_rent = get_object_or_404(RentPaymentHistory, student=student)

    # return render(request, "templates/student_profile.html", {'student': student})
    try:
        student = Student.objects.get(user=request.user)
        return render(request, "student_profile.html", {'student': student})
    except Student.DoesNotExist:
        messages.error(request, "Session expired or profile missing. Please login again.")
        logout(request)
        return redirect('student_login')

    return render(request, 'student_dashboard.html', {'student': student})

# def rent_history(request):
#     student_rent = get_object_or_404(RentPaymentHistory, use=request.user)
#     return render(request, "")

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)  # Prevent logout after password change
            messages.success(request, "Your password was successfully updated.")
            return redirect('student_dashboard')
        else:
            messages.error(request, "Sorry, there is an error.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})

@login_required(login_url='student_login')
def rent_status(request):
    try:
        rent = Student.objects.get(user=request.user)
        rent_history = RentPaymentHistory.objects.filter(student=rent).order_by('-date_paid')

        amount_payable = None
        latest_rent = rent_history.first()  # get most recent rent record

        if latest_rent:
            if latest_rent.remaining_amount > 0:
                amount_payable = latest_rent.remaining_amount
            else:
                amount_payable = 0

    except Student.DoesNotExist:
        messages.error(request, "Student profile not found. Login again. If problem persists Please contact admin.")
        return redirect('student_dashboard')

    rent_s = "Paid" if rent.rent_status else "Not paid"
    return render(request, "rent_status.html", {
        'rent': rent,
        'rent_s': rent_s,
        'rent_history': rent_history,
        'amount_payable': amount_payable,
        'latest_rent': latest_rent
    })

@login_required(login_url='student_login')
def room_info(request):
    return render(request, "room_info.html")

from django.contrib.auth.decorators import login_required

@login_required(login_url='student_login')
def complaint(request):

    if request.method == "POST":

        sub = request.POST.get("sub")
        msg = request.POST.get("msg")

        student = get_object_or_404(
            Student,
            user=request.user
        )

        Complaint.objects.create(
            student=student,
            subject=sub,
            msg=msg,
        )

        messages.success(
            request,
            "Your Complaint has been raised."
        )

        return redirect("student_dashboard")

    return render(
        request,
        "complaint.html"
    )
@login_required(login_url='student_login')
def complaint_history(request):
    student = get_object_or_404(Student, user=request.user)
    complaints = Complaint.objects.filter(student=student).order_by('-date')
    return render(request, 'complaint_history.html', {'complaints': complaints})


def mark_attendance(request):
    
    # Current local time
    now = timezone.localtime()

    # Current hour
    current_hour = now.hour

    print("Current Server Time:", now)
    print("Current Hour:", current_hour)

    session = None

    # Morning Attendance (8 AM - 11 AM)
    if 8 <= current_hour < 10:
        session = 'Morning'

    # Evening Attendance (5 PM - 6 PM)
    elif 17 <= current_hour < 18:
        session = 'Evening'

    # Night Attendance (9 PM - 10 PM)
    elif 21 <= current_hour < 22:
        session = 'Night'

    else:
        messages.error(
            request,
            f"Attendance marking is closed. Current time: {now.strftime('%I:%M %p')}"
        )
        return redirect('student_dashboard')

    # Check if already marked
    attendance_exists = Attendance.objects.filter(
        student=request.user,
        session=session,
        date=now.date()
    ).exists()

    if attendance_exists:

        messages.warning(
            request,
            f"{session} attendance already marked."
        )

    else:

        Attendance.objects.create(
            student=request.user,
            session=session,
            date=now.date(),
            status='Present'
        )

        messages.success(
            request,
            f"{session} attendance marked successfully."
        )

    return redirect('student_dashboard')

from django.shortcuts import get_object_or_404, redirect

def resolve_complaint(request, complaint_id):

    complaint = get_object_or_404(
        Complaint,
        id=complaint_id
    )

    complaint.status = "Resolved"

    complaint.save()

    return redirect('manage_complaints')


@login_required
def apply_leave(request):

    student = Student.objects.get(user=request.user)

    if request.method == 'POST':

        form = LeaveRequestForm(request.POST)

        if form.is_valid():

            leave = form.save(commit=False)

            leave.student = student

            leave.save()

            return redirect('leave_history')

    else:
        form = LeaveRequestForm()

    return render(
        request,
        'apply_leave.html',
        {'form': form}
    )


@login_required
def leave_history(request):

    student = Student.objects.get(user=request.user)

    leaves = LeaveRequest.objects.filter(
        student=student
    ).order_by('-applied_on')

    return render(
        request,
        'leave_history.html',
        {'leaves': leaves}
    )
    

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Student, HostelIncharge

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')

            elif HostelIncharge.objects.filter(user=user).exists():
                return redirect('hostel_dashboard')

            elif Student.objects.filter(user=user).exists():
                return redirect('student_dashboard')

        else:
            from django.contrib import messages
            messages.error(
                request,
                "Invalid Username or Password"
            )

from django.utils import timezone
from .models import Attendance, Student


@login_required(login_url='hostel_login')
def hostel_dashboard(request):

    try:
        incharge = HostelIncharge.objects.get(
            user=request.user
        )

    except HostelIncharge.DoesNotExist:

        messages.error(
            request,
            "You are not authorized."
        )

        return redirect('hostel_login')

    pending_leaves = LeaveRequest.objects.filter(
        status='Pending'
    ).count()

    complaints = Complaint.objects.filter(
        status='Pending'
    ).count()

    today = timezone.localdate()

    boys_present = Attendance.objects.filter(
        date=today,
        status='Present',
        student__student__gender='Male'
    ).count()

    girls_present = Attendance.objects.filter(
        date=today,
        status='Present',
        student__student__gender='Female'
    ).count()

    total_present = boys_present + girls_present

    total_boys = Student.objects.filter(
        gender='Male'
    ).count()

    total_girls = Student.objects.filter(
        gender='Female'
    ).count()

    boys_absent = total_boys - boys_present
    girls_absent = total_girls - girls_present

    context = {

        'incharge': incharge,

        'pending_leaves': pending_leaves,

        'complaints': complaints,

        'boys_present': boys_present,

        'girls_present': girls_present,

        'boys_absent': boys_absent,

        'girls_absent': girls_absent,

        'total_present': total_present
    }

    return render(
        request,
        'hostel_dashboard.html',
        context
    )
    
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student


def student_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user and Student.objects.filter(user=user).exists():

            login(request, user)

            return redirect(
                'student_dashboard'
            )

        messages.error(
            request,
            "Invalid Student Login Credentials"
        )

    return render(
        request,
        'student_login.html'
    )
    
from .models import HostelIncharge


from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import HostelIncharge

def hostel_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user and HostelIncharge.objects.filter(user=user).exists():

            login(request, user)

            return redirect('hostel_dashboard')

        messages.error(
            request,
            "Invalid Hostel Incharge Credentials"
        )

    return render(
        request,
        'hostel_login.html'
    )
    

@login_required(login_url='hostel_login')
def manage_leaves(request):

    leaves = LeaveRequest.objects.all().order_by(
        '-applied_on'
    )

    return render(
        request,
        'manage_leaves.html',
        {'leaves': leaves}
    )
    
@login_required(login_url='hostel_login')
def manage_complaints(request):

    complaints = Complaint.objects.all().order_by(
        '-date'
    )

    return render(
        request,
        'manage_complaints.html',
        {
            'complaints': complaints
        }
    )
    
@login_required(login_url='hostel_login')
def view_students(request):

    students = Student.objects.all()

    return render(
        request,
        'view_students.html',
        {'students': students}
    )
@login_required(login_url='hostel_login')
def view_attendance(request):

    attendance_records = Attendance.objects.all().order_by(
        '-date'
    )

    return render(
        request,
        'view_attendance.html',
        {
            'attendance_records': attendance_records
        }
    )
    
from django.contrib.auth import logout

def hostel_logout(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect('hostel_login')

# @login_required(login_url='hostel_login')
# def approve_leave(request, leave_id):

#     leave = LeaveRequest.objects.get(
#         id=leave_id
#     )

#     leave.status = "Approved"

#     leave.approved_by = request.user.username

#     leave.save()

#     messages.success(
#         request,
#         "Leave Approved Successfully"
#     )

#     return redirect('manage_leaves')

# @login_required(login_url='hostel_login')
# def reject_leave(request, leave_id):

#     leave = LeaveRequest.objects.get(
#         id=leave_id
#     )

#     leave.status = "Rejected"

#     leave.approved_by = request.user.username

#     leave.save()

#     messages.success(
#         request,
#         "Leave Rejected Successfully"
#     )

#     return redirect('manage_leaves')

# @login_required
# def apply_outpass(request):

#     student = Student.objects.get(
#         user=request.user
#     )

#     if request.method == "POST":

#         Outpass.objects.create(
#             student=student,
#             destination=request.POST.get(
#                 "destination"
#             ),
#             reason=request.POST.get(
#                 "reason"
#             ),
#             out_time=request.POST.get(
#                 "out_time"
#             ),
#             return_time=request.POST.get(
#                 "return_time"
#             ),
#             emergency_contact=request.POST.get(
#                 "contact"
#             )
#         )

#         messages.success(
#             request,
#             "Outpass request submitted."
#         )

#         return redirect(
#             'outpass_history'
#         )

#     return render(
#         request,
#         'apply_outpass.html'
#     )
    
# @login_required(login_url='hostel_login')
# def approve_outpass(request, outpass_id):

#     outpass = Outpass.objects.get(
#         id=outpass_id
#     )

#     outpass.status = "Approved"

#     outpass.approved_by = (
#         request.user.username
#     )

#     outpass.approved_on = timezone.now()

#     outpass.save()

#     messages.success(
#         request,
#         "Outpass Approved"
#     )

#     return redirect(
#         'manage_outpasses'
#     )
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Student, Outpass

@login_required(login_url='student_login')
def outpass_history(request):

    student = Student.objects.get(
        user=request.user
    )

    outpasses = Outpass.objects.filter(
        student=student
    ).order_by('-applied_on')

    return render(
        request,
        'outpass_history.html',
        {'outpasses': outpasses}
    )
    
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Outpass

@login_required(login_url='student_login')
def view_outpass(request, outpass_id):

    outpass = get_object_or_404(
        Outpass,
        id=outpass_id
    )

    return render(
        request,
        'view_outpass.html',
        {'outpass': outpass}
    )
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Outpass

@login_required(login_url='hostel_login')
def manage_outpasses(request):

    outpasses = Outpass.objects.all().order_by(
        '-applied_on'
    )

    return render(
        request,
        'manage_outpasses.html',
        {'outpasses': outpasses}
    )
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

@login_required(login_url='hostel_login')
def approve_outpass(request, outpass_id):

    outpass = get_object_or_404(
        Outpass,
        id=outpass_id
    )

    outpass.status = 'Approved'
    outpass.approved_by = request.user.username
    outpass.approved_on = timezone.now()

    outpass.save()

    messages.success(
        request,
        "Outpass approved successfully."
    )

    return redirect(
        'manage_outpasses'
    )


@login_required(login_url='hostel_login')
def reject_outpass(request, outpass_id):

    outpass = get_object_or_404(
        Outpass,
        id=outpass_id
    )

    outpass.status = 'Rejected'
    outpass.approved_by = request.user.username
    outpass.approved_on = timezone.now()

    outpass.save()

    messages.success(
        request,
        "Outpass rejected successfully."
    )

    return redirect(
        'manage_outpasses'
    )
    
@login_required
def verify_outpass(request, outpass_code):

    outpass = get_object_or_404(
        Outpass,
        outpass_id=outpass_code
    )

    return render(
        request,
        'verify_outpass.html',
        {'outpass': outpass}
    )
    

from .forms import OutpassForm

@login_required
def apply_outpass(request):

    student = Student.objects.get(user=request.user)

    if request.method == 'POST':

        form = OutpassForm(request.POST)

        if form.is_valid():

            outpass = form.save(commit=False)
            outpass.student = student
            outpass.save()

            return redirect('outpass_history')

    else:
        form = OutpassForm()

    return render(
        request,
        'apply_outpass.html',
        {'form': form}
    )
    
@login_required
def leave_management(request):

    student = Student.objects.get(user=request.user)

    if request.method == 'POST':

        form = LeaveRequestForm(request.POST)

        if form.is_valid():

            leave = form.save(commit=False)
            leave.student = student
            leave.save()

            messages.success(
                request,
                "Leave request submitted successfully."
            )

            return redirect('leave_management')

    else:
        form = LeaveRequestForm()

    leaves = LeaveRequest.objects.filter(
        student=student
    ).order_by('-applied_on')

    return render(
        request,
        'leave_management.html',
        {
            'form': form,
            'leaves': leaves
        }
    )
    
@login_required
def view_leave(request, leave_id):

    leave = get_object_or_404(
        LeaveRequest,
        id=leave_id
    )

    return render(
        request,
        'view_leave.html',
        {'leave': leave}
    )
    
from django.shortcuts import render
from .models import Holiday
from django.utils import timezone

def holiday_list(request):
    holidays = Holiday.objects.filter(
        end_date__gte=timezone.now().date()
    ).order_by('start_date')

    return render(
        request,
        'holidays_list.html',
        {'holidays': holidays}
    )
    
from django.shortcuts import render, redirect
from .models import Holiday
from .forms import HolidayForm

def holiday_create(request):
    if request.method == 'POST':
        form = HolidayForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('holiday_list')
    else:
        form = HolidayForm()

    return render(request, 'holiday_create.html', {
        'form': form
    })

from django.shortcuts import get_object_or_404, redirect
from .models import LeaveRequest

def approve_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = "Approved"
    leave.save()
    return redirect("manage_leaves")


def reject_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = "Rejected"
    leave.save()
    return redirect("manage_leaves")


from django.contrib.auth.models import User
from django.http import HttpResponse

def user_count(request):
    return HttpResponse(f"Users: {User.objects.count()}")

from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="Admin@123"
        )
        return HttpResponse("Superuser created")

    return HttpResponse("Superuser already exists")