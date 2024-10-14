import requests
from audioop import avg
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import render
from .models import FootfallData, FootstepData, PowerGeneration
import json
import random
from django.utils import timezone
from .models import *
from django.db.models import Sum, Avg, Value
from django.db.models.functions import Cast
from django.db.models import Sum, FloatField, IntegerField, F
from django.http import StreamingHttpResponse
from threading import Thread
import requests
from django.shortcuts import render


# Global variable to store foot traffic counts (for simulation purposes)
hotspot_footstep_counts = {
    'Railway': 0,
    'Airport': 0,
    'Park': 0,
    'Theater': 0,
    'Mall': 0,
}



def Home(request):
    return render(request, 'Home.html')
def About_us(request):
    return render(request, 'About_us.html')
def Contact(request):
    return render(request, 'Contact.html')
def Services(request):
    return render(request, 'Services.html')

def home(request):
    # Sample data, this would come from your real API in a live system
    total_footfall = 4530  # Example total footfall
    peak_hours = 18  # Peak hour (18:00)
    average_dwell_time = 12.5  # Average dwell time in minutes

    # Simulated footfall distribution (last 7 days)
    footfall_distribution = [
        {'date_recorded__date': '2024-09-28', 'total_footsteps': 750},
        {'date_recorded__date': '2024-09-29', 'total_footsteps': 670},
        {'date_recorded__date': '2024-09-30', 'total_footsteps': 900},
        {'date_recorded__date': '2024-10-01', 'total_footsteps': 1020},
        {'date_recorded__date': '2024-10-02', 'total_footsteps': 980},
        {'date_recorded__date': '2024-10-03', 'total_footsteps': 820},
        {'date_recorded__date': '2024-10-04', 'total_footsteps': 390},
    ]

    # Simulated footfall trends (last 30 days)
    footfall_trends = [
        {'date_recorded__date': '2024-09-05', 'total_footsteps': 500},
        {'date_recorded__date': '2024-09-06', 'total_footsteps': 520},
        {'date_recorded__date': '2024-09-07', 'total_footsteps': 490},
        {'date_recorded__date': '2024-09-08', 'total_footsteps': 510},
        # More entries for the last 30 days
        {'date_recorded__date': '2024-10-04', 'total_footsteps': 390},
    ]

    context = {
        'total_footfall': total_footfall,
        'peak_hours': peak_hours,
        'average_dwell_time': average_dwell_time,
        'footfall_distribution': footfall_distribution,
        'footfall_trends': footfall_trends
    }

    return render(request, 'foot/home.html', context)

def realtime(request):
    return render(request, 'foot/realtime.html')


def traffic(request):
    return render(request, 'traffic.html') 


# Helper functions to calculate distribution, trends, etc.
def calculate_average_dwell_time(data):
    # Implement logic to calculate average dwell time
    return 0  # Placeholder value

def get_footfall_distribution(data):
    # Implement logic for footfall distribution (grouping data by date, etc.)
    return []

def get_footfall_trends(data):
    # Implement logic for footfall trends over time (last 30 days)
    return []

def historical_data(request):
    data = FootstepData.objects.all().values('location_name', 'footsteps', 'energy_generated', 'date_recorded')
    return JsonResponse(list(data), safe=False)

def real_time_data(request):
    regions = PowerGeneration.objects.values_list('region', flat=True).distinct()
    latest_data = []
    for region in regions:
        power_generated = random.uniform(0, 10)
        latest_data.append({
            'region': region,
            'power_generated': power_generated,
            'timestamp': timezone.now(),
        })
    return JsonResponse(latest_data, safe=False)

def add_footstep_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        location_name = data.get('location_name')
        footsteps = data.get('footsteps')
        energy_generated = data.get('energy_generated')

        FootstepData.objects.create(
            location_name=location_name,
            footsteps=footsteps,
            energy_generated=energy_generated,
        )
        return JsonResponse({'message': 'Data added successfully'}, status=201)

def hotspot_footstep_data(request):
    """Fetch current footstep counts for all hotspots and increment on click."""
    global hotspot_footstep_counts

    # Simulate the increment of footstep counts
    for hotspot in hotspot_footstep_counts:
        hotspot_footstep_counts[hotspot] += random.randint(1, 10)  # Random increment for simulation

    # Prepare data for response
    response_data = [{'location_name': name, 'total_footsteps': count} for name, count in hotspot_footstep_counts.items()]
    return JsonResponse(response_data, safe=False)

def hotspot_footstep_data_detail(request, location_name):
    # Fetch the footstep data for the specified location
    data = FootstepData.objects.filter(location_name=location_name).values('footsteps', 'date_recorded')
    return JsonResponse(list(data), safe=False)\
    


def footfall_metrics(request):
    # Calculate total footfall
    total_footfall = FootfallData.objects.aggregate(total=Sum('footsteps'))['total'] or 0

    # Calculate peak hours
    peak_hours = FootfallData.objects.annotate(
        hour=models.functions.ExtractHour('date_recorded')
    ).values('hour').annotate(
        total=Sum('footsteps')
    ).order_by('-total')[:1]

    # Calculate average dwell time
    average_dwell_time = FootfallData.objects.aggregate(avg_time=Avg('dwell_time'))['avg_time'] or 0

    # Calculate footfall distribution
    footfall_distribution = FootfallData.objects.values('date_recorded__date').annotate(total=Sum('footsteps'))

    # Calculate footfall trends
    now = timezone.now()
    last_month = now - timedelta(days=30)
    footfall_trends = FootfallData.objects.filter(date_recorded__gte=last_month).values('date_recorded__date').annotate(total=Sum('footsteps'))

    context = {
        'total_footfall': total_footfall,
        'peak_hours': peak_hours,
        'average_dwell_time': average_dwell_time,
        'footfall_distribution': footfall_distribution,
        'footfall_trends': footfall_trends,
    }
    
    return render(request, 'foot/home.html', context)

def vehicle_counting(request):
    return render(request, 'traffic/vehicle_counting.html')  # Ensure you create this template

def gen_frames():  
    cap = cv2.VideoCapture(0)  # Use 0 for webcam, or 'video.mp4' for a video file
    vehicle_count = 0
    line_position = 300  # Adjust this position based on your requirement
    counted_vehicles = []

    backSub = cv2.createBackgroundSubtractorMOG2()

    while True:
        success, frame = cap.read()
        if not success:
            break

        fg_mask = backSub.apply(frame)
        blurred_mask = cv2.GaussianBlur(fg_mask, (5, 5), 0)
        _, thresh = cv2.threshold(blurred_mask, 200, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 500:  # Adjust this value to filter noise
                continue

            x, y, w, h = cv2.boundingRect(contour)
            center_y = y + h // 2

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Count vehicles crossing the line
            if center_y > line_position and center_y not in counted_vehicles:
                vehicle_count += 1
                counted_vehicles.append(center_y)

        cv2.line(frame, (0, line_position), (frame.shape[1], line_position), (255, 0, 0), 2)
        cv2.putText(frame, f"Vehicles Counted: {vehicle_count}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Convert the frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Create a view to stream video
def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
