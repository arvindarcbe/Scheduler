from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Interview
from datetime import datetime, date
import re


def parse_interview_data(text_data):
    """Parse the text input to extract interview information - handles all edge cases"""
    interviews = []
    
    # Month mapping
    month_map = {
        'jan': 1, 'january': 1,
        'feb': 2, 'february': 2,
        'mar': 3, 'march': 3,
        'apr': 4, 'april': 4,
        'may': 5,
        'jun': 6, 'june': 6,
        'jul': 7, 'july': 7,
        'aug': 8, 'august': 8,
        'sep': 9, 'september': 9,
        'oct': 10, 'october': 10,
        'nov': 11, 'november': 11,
        'dec': 12, 'december': 12
    }
    
    # First, merge lines that are split (e.g., candidate on one line, time on next)
    lines = text_data.strip().split('\n')
    merged_lines = []
    current_line = ""
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            if current_line:
                merged_lines.append(current_line)
                current_line = ""
            continue
        
        # Check if line starts with date pattern (handles "24Nov", "24 Nov", "24th nov", etc.)
        date_pattern = r'^\d{1,2}(?:st|nd|rd|th)?\s*(?:nov|november|dec|december|jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october)|^\d{1,2}(?:nov|november|dec|december|jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october)'
        if re.search(date_pattern, line, re.IGNORECASE):
            if current_line:
                merged_lines.append(current_line)
            current_line = line
        else:
            # This is a continuation line (e.g., "From 2pm to 3pm" or "with L&T")
            if current_line:
                current_line += " " + line
            else:
                current_line = line
    
    if current_line:
        merged_lines.append(current_line)
    
    # Now parse each merged line
    for line in merged_lines:
        if not line or len(line) < 10:
            continue
        
        # Normalize the line
        line_normalized = line
        
        # Fix common typos and variations
        line_normalized = re.sub(r'\bform\b', 'from', line_normalized, flags=re.IGNORECASE)  # "form" -> "from"
        line_normalized = re.sub(r'\bFrom\b', 'from', line_normalized)  # Capital "From" -> "from"
        line_normalized = line_normalized.rstrip('.')  # Remove trailing periods
        
        # Replace periods with colons in time (11.30 -> 11:30, 12.00pm -> 12:00pm)
        line_normalized = re.sub(r'(\d{1,2})\.(\d{2})', r'\1:\2', line_normalized)
        
        # Handle "noon" at end
        line_normalized = re.sub(r'\bnoon\b', '12:00pm', line_normalized, flags=re.IGNORECASE)
        
        # Fix dates without spaces (24Nov -> 24 Nov)
        line_normalized = re.sub(r'(\d{1,2})(nov|november|dec|december|jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october)', r'\1 \2', line_normalized, flags=re.IGNORECASE)
        
        # Fix spaces in dates (24 th -> 24th)
        line_normalized = re.sub(r'(\d{1,2})\s+(st|nd|rd|th)', r'\1\2', line_normalized, flags=re.IGNORECASE)
        line_normalized = re.sub(r'(\d{1,2})\s+(nov|november|dec|december|jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october)', r'\1 \2', line_normalized, flags=re.IGNORECASE)
        
        # Try multiple patterns (order matters - more specific patterns first)
        patterns = [
            # Pattern 1c: Handle entries WITHOUT "with" keyword - "30 nov AAA Dell from 3pm to 4 pm"
            # This handles cases where candidate and company are directly adjacent
            r'(\d{1,2})(?:st|nd|rd|th)?\s+(nov|november|dec|december|jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october)\s+([A-Za-z]{1,20})\s+([A-Za-z]{1,20})\s+from\s+(\d{1,2}(?::\d{2})?(?:\s*\.\s*\d{2})?\s*(?:am|pm|AM|PM|noon))\s+to\s+(\d{1,2}(?::\d{2})?(?:\s*\.\s*\d{2})?\s*(?:am|pm|AM|PM|noon))',
            
            # Pattern 1b: Handle short candidate names (like "AAA") with short company names (like "Del")
            # This pattern specifically handles cases where both candidate and company are short (1-15 chars)
            # Try this FIRST because it's more specific
            r'(\d{1,2})(?:st|nd|rd|th)?\s+(nov|november|dec|december|jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october)\s+([A-Za-z]{1,15})\s+with\s+([A-Za-z]{1,15})\s+from\s+(\d{1,2}(?::\d{2})?(?:\s*\.\s*\d{2})?\s*(?:am|pm|AM|PM|noon))\s+to\s+(\d{1,2}(?::\d{2})?(?:\s*\.\s*\d{2})?\s*(?:am|pm|AM|PM|noon))',
            
            # Pattern 1: Standard with "from" - "24th nov priyanka with Deloitte from 11am to 12pm"
            # Updated to handle short company names like "Del" - use negative lookahead to stop at "with"
            r'(\d{1,2})(?:st|nd|rd|th)?\s+(nov|november|dec|december|jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october)\s+([A-Za-z]+(?:\s+[A-Za-z]+)*?)\s+with\s+([A-Za-z0-9&\s]+?)\s+from\s+(\d{1,2}(?::\d{2})?(?:\s*\.\s*\d{2})?\s*(?:am|pm|AM|PM|noon))\s+to\s+(\d{1,2}(?::\d{2})?(?:\s*\.\s*\d{2})?\s*(?:am|pm|AM|PM|noon))',
            
            # Pattern 2: Without "from" - "24 th Nov Murugaboopathy with infolab 12.00pm to 01.00pm"
            r'(\d{1,2})(?:st|nd|rd|th)?\s+(nov|november|dec|december|jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october)\s+([A-Za-z]+(?:\s+[A-Za-z]+)*?)\s+with\s+([A-Za-z0-9&\s]+?)\s+(\d{1,2}(?::\d{2})?(?:\s*\.\s*\d{2})?\s*(?:am|pm|AM|PM))\s+to\s+(\d{1,2}(?::\d{2})?(?:\s*\.\s*\d{2})?\s*(?:am|pm|AM|PM))',
            
            # Pattern 3: Times without am/pm - "24th Nov Arockia charles A with UTS form 3 to 3.30"
            r'(\d{1,2})(?:st|nd|rd|th)?\s+(nov|november|dec|december|jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october)\s+([A-Za-z]+(?:\s+[A-Za-z]+)*?)\s+with\s+([A-Za-z0-9&\s]+?)\s+(?:from|form)\s+(\d{1,2}(?::\d{2})?)\s+to\s+(\d{1,2}(?::\d{2})?)',
            
            # Pattern 4: Handle "From" at start of continuation line
            r'(\d{1,2})(?:st|nd|rd|th)?\s+(nov|november|dec|december|jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october)\s+([A-Za-z]+(?:\s+[A-Za-z]+)*?)\s+with\s+([A-Za-z0-9&\s]+?)\s+From\s+(\d{1,2}(?::\d{2})?(?:\s*\.\s*\d{2})?\s*(?:am|pm|AM|PM))\s+to\s+(\d{1,2}(?::\d{2})?(?:\s*\.\s*\d{2})?\s*(?:am|pm|AM|PM))',
        ]
        
        match = None
        for pattern in patterns:
            match = re.search(pattern, line_normalized, re.IGNORECASE)
            if match:
                break
        
        if match:
            try:
                day = int(match.group(1))
                month_str = match.group(2).lower()
                candidate = match.group(3).strip()
                company = match.group(4).strip()
                start_time_str = match.group(5).strip()
                end_time_str = match.group(6).strip()
                
                # Get month number
                month = month_map.get(month_str[:3])
                if not month:
                    for key, value in month_map.items():
                        if month_str.startswith(key):
                            month = value
                            break
                
                if not month:
                    continue
                
                year = 2024
                
                # Try to create date
                try:
                    interview_date = date(year, month, day)
                except ValueError:
                    continue
                
                # Parse time strings - handle times without am/pm
                try:
                    # If no am/pm, infer from hour (assume 1-11 is pm if no am/pm, 12 is pm)
                    start_has_ampm = bool(re.search(r'(am|pm)', start_time_str, re.IGNORECASE))
                    end_has_ampm = bool(re.search(r'(am|pm)', end_time_str, re.IGNORECASE))
                    
                    if not start_has_ampm:
                        # Infer am/pm - if hour is 1-11, likely pm. If 12, likely pm
                        hour_match = re.search(r'(\d{1,2})', start_time_str)
                        if hour_match:
                            hour = int(hour_match.group(1))
                            if hour >= 1 and hour <= 11:
                                start_time_str += 'pm'
                            elif hour == 12:
                                start_time_str += 'pm'
                            else:
                                start_time_str += 'am'
                    
                    if not end_has_ampm:
                        hour_match = re.search(r'(\d{1,2})', end_time_str)
                        if hour_match:
                            hour = int(hour_match.group(1))
                            if hour >= 1 and hour <= 11:
                                end_time_str += 'pm'
                            elif hour == 12:
                                end_time_str += 'pm'
                            else:
                                end_time_str += 'am'
                    
                    start_time = parse_time_string(start_time_str)
                    end_time = parse_time_string(end_time_str)
                except (ValueError, AttributeError):
                    continue
                
                # Validate times
                if start_time >= end_time:
                    continue
                
                interviews.append({
                    'candidate_name': candidate,
                    'company_name': company,
                    'interview_date': interview_date,
                    'start_time': start_time,
                    'end_time': end_time
                })
            except (ValueError, AttributeError, IndexError) as e:
                continue
    
    return interviews


def parse_time_string(time_str):
    """Parse time string - handles various formats like '11am', '11:30am', '2pm', '2:00pm', '11.30 am', '11.00am', '12.00 noon'"""
    if not time_str:
        raise ValueError("Empty time string")
    
    time_str = time_str.strip().lower()
    
    # Handle "noon" (standalone or at end like "12.00 noon")
    if 'noon' in time_str:
        return datetime.strptime("12:00", "%H:%M").time()
    
    # Replace periods with colons (handle 11.30, 11.00, 12.00 formats)
    time_str = re.sub(r'(\d{1,2})\.(\d{2})', r'\1:\2', time_str)
    time_str = re.sub(r'(\d{1,2})\.(\d{1})', r'\1:0\2', time_str)  # Handle 11.5 -> 11:05
    
    # Remove all spaces
    time_str = re.sub(r'\s+', '', time_str)
    
    # Extract AM/PM
    is_pm = 'pm' in time_str
    time_str = re.sub(r'(am|pm)', '', time_str, flags=re.IGNORECASE)
    
    # Parse hour and minute
    if ':' in time_str:
        parts = time_str.split(':')
        hour = int(parts[0])
        minute = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    else:
        # Just hour, no minutes
        hour = int(time_str)
        minute = 0
    
    # Validate hour
    if hour < 1 or hour > 12:
        raise ValueError(f"Invalid hour: {hour}")
    
    # Validate minute
    if minute < 0 or minute > 59:
        raise ValueError(f"Invalid minute: {minute}")
    
    # Convert to 24-hour format
    if is_pm and hour != 12:
        hour += 12
    elif not is_pm and hour == 12:
        hour = 0
    
    return datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time()


def assign_panels(interviews):
    """Assign interviews to panels based on time conflicts. Returns (scheduled, unscheduled)"""
    # Sort by date and time
    sorted_interviews = sorted(interviews, key=lambda x: (x['interview_date'], x['start_time']))
    
    panel_assignments = []
    unscheduled = []
    panel1_schedule = []  # List of (date, start_time, end_time) tuples
    panel2_schedule = []  # List of (date, start_time, end_time) tuples
    
    for interview in sorted_interviews:
        date_obj = interview['interview_date']
        start = interview['start_time']
        end = interview['end_time']
        
        # Check if it conflicts with panel 1 (same date and overlapping time OR same start_time)
        conflicts_panel1 = any(
            date_obj == sched_date and (
                start == sched_start or  # Exact same start time
                not (end <= sched_start or start >= sched_end)  # Overlapping time ranges
            )
            for sched_date, sched_start, sched_end in panel1_schedule
        )
        
        # Check if it conflicts with panel 2 (same date and overlapping time OR same start_time)
        conflicts_panel2 = any(
            date_obj == sched_date and (
                start == sched_start or  # Exact same start time
                not (end <= sched_start or start >= sched_end)  # Overlapping time ranges
            )
            for sched_date, sched_start, sched_end in panel2_schedule
        )
        
        # Assign to panel with no conflict, prefer panel 1
        if not conflicts_panel1:
            panel = 1
            panel1_schedule.append((date_obj, start, end))
            interview['panel'] = panel
            panel_assignments.append(interview)
        elif not conflicts_panel2:
            panel = 2
            panel2_schedule.append((date_obj, start, end))
            interview['panel'] = panel
            panel_assignments.append(interview)
        else:
            # If both have conflicts, mark as unscheduled (Panel 3)
            interview['panel'] = 3
            unscheduled.append(interview)
    
    return panel_assignments, unscheduled


def add_interviews(request):
    """View to add single or multiple interviews"""
    if request.method == 'POST':
        text_data = request.POST.get('interview_data', '')
        
        if text_data:
            # Parse the text data
            interviews = parse_interview_data(text_data)
            
            if interviews:
                # Clear existing interviews
                Interview.objects.all().delete()
                
                # Remove duplicates based on candidate, company, date, and start_time
                seen = set()
                unique_interviews = []
                for interview in interviews:
                    key = (
                        interview['candidate_name'].lower(),
                        interview['company_name'].lower(),
                        interview['interview_date'],
                        interview['start_time']
                    )
                    if key not in seen:
                        seen.add(key)
                        unique_interviews.append(interview)
                
                # Assign panels
                assigned_interviews, unscheduled_interviews = assign_panels(unique_interviews)
                
                # Create Interview objects with duplicate handling
                created_count = 0
                skipped_count = 0
                errors = []
                
                # Add scheduled interviews
                for interview_data in assigned_interviews:
                    try:
                        # Use get_or_create to handle duplicates gracefully
                        interview, created = Interview.objects.get_or_create(
                            interview_date=interview_data['interview_date'],
                            start_time=interview_data['start_time'],
                            panel=interview_data['panel'],
                            defaults={
                                'candidate_name': interview_data['candidate_name'],
                                'company_name': interview_data['company_name'],
                                'end_time': interview_data['end_time'],
                            }
                        )
                        if created:
                            created_count += 1
                        else:
                            # Update existing interview
                            interview.candidate_name = interview_data['candidate_name']
                            interview.company_name = interview_data['company_name']
                            interview.end_time = interview_data['end_time']
                            interview.save()
                            created_count += 1
                    except Exception as e:
                        skipped_count += 1
                        errors.append(f"{interview_data['candidate_name']} - {str(e)}")
                
                # Add unscheduled interviews (Panel 3)
                # Store requested time in start_time, use sequential seconds for uniqueness
                for idx, interview_data in enumerate(unscheduled_interviews):
                    try:
                        # Store the requested start_time, use seconds offset for uniqueness
                        requested_start = interview_data['start_time']
                        # Add seconds offset to make each entry unique (0, 1, 2, ... seconds)
                        hour = requested_start.hour
                        minute = requested_start.minute
                        second = min(idx % 60, 59)  # Cycle through 0-59 seconds
                        unique_start_time = datetime.strptime(f"{hour:02d}:{minute:02d}:{second:02d}", "%H:%M:%S").time()
                        
                        Interview.objects.create(
                            candidate_name=interview_data['candidate_name'],
                            company_name=interview_data['company_name'],
                            interview_date=interview_data['interview_date'],
                            start_time=unique_start_time,  # Unique time for constraint
                            end_time=interview_data['end_time'],  # Store requested end time
                            panel=3
                        )
                        created_count += 1
                    except Exception as e:
                        skipped_count += 1
                        errors.append(f"{interview_data['candidate_name']} - {str(e)}")
                
                if errors:
                    messages.warning(request, f'Added {created_count} interview(s). {skipped_count} skipped due to errors.')
                else:
                    messages.success(request, f'Successfully added {created_count} interview(s) to the schedule.')
                
                return redirect('schedule_view')
            else:
                messages.error(request, 'Could not parse any valid interview data. Please check the format.')
        else:
            messages.error(request, 'Please provide interview data.')
    
    return render(request, 'scheduler/add_interviews.html')


def get_time_slots():
    """Generate time slots from 9 AM to 7 PM in 30-minute intervals"""
    slots = []
    for hour in range(9, 20):  # 9 AM to 7 PM
        for minute in [0, 30]:
            time_obj = datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time()
            slots.append(time_obj)
    return slots


def check_time_available(date_obj, start_time, end_time, panel_schedule):
    """Check if a time slot is available for a given panel"""
    for sched_date, sched_start, sched_end in panel_schedule:
        if date_obj == sched_date:
            # Check if times overlap
            if not (end_time <= sched_start or start_time >= sched_end):
                return False
    return True


def schedule_view(request):
    """View to display the interview schedule in tabulated format for 2 panels + Panel 3"""
    interviews = Interview.objects.all().order_by('interview_date', 'start_time', 'panel')
    
    # Generate time slots
    time_slots = get_time_slots()
    
    # Group by date and panel
    schedule_data = {}
    panel1_schedules = {}  # Track scheduled times per date for Panel 1
    panel2_schedules = {}  # Track scheduled times per date for Panel 2
    
    for interview in interviews:
        date_key = interview.interview_date.strftime('%Y-%m-%d')
        day = interview.interview_date.day
        # Format day with proper suffix (1st, 2nd, 3rd, 4th, etc.)
        if 10 <= day % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        date_display = f"{day}{suffix} {interview.interview_date.strftime('%B %Y')}"
        
        if date_key not in schedule_data:
            schedule_data[date_key] = {
                'date_display': date_display,
                'date_obj': interview.interview_date,
                'panel1': [],
                'panel2': [],
                'panel3': []
            }
            panel1_schedules[date_key] = []
            panel2_schedules[date_key] = []
        
        if interview.panel == 1:
            schedule_data[date_key]['panel1'].append({
                'candidate': interview.candidate_name,
                'company': interview.company_name,
                'start_time': interview.start_time.strftime('%I:%M %p'),
                'end_time': interview.end_time.strftime('%I:%M %p'),
            })
            panel1_schedules[date_key].append((interview.interview_date, interview.start_time, interview.end_time))
        elif interview.panel == 2:
            schedule_data[date_key]['panel2'].append({
                'candidate': interview.candidate_name,
                'company': interview.company_name,
                'start_time': interview.start_time.strftime('%I:%M %p'),
                'end_time': interview.end_time.strftime('%I:%M %p'),
            })
            panel2_schedules[date_key].append((interview.interview_date, interview.start_time, interview.end_time))
        elif interview.panel == 3:
            # For Panel 3, show the requested time
            # The start_time has a seconds offset, but we display it without seconds
            # The end_time contains the requested end time
            start_display = interview.start_time.strftime('%I:%M %p')  # This will show the requested time
            schedule_data[date_key]['panel3'].append({
                'candidate': interview.candidate_name,
                'company': interview.company_name,
                'start_time': start_display,
                'end_time': interview.end_time.strftime('%I:%M %p'),
                'requested_time': f"{start_display} - {interview.end_time.strftime('%I:%M %p')}"
            })
    
    # Calculate time slot availability for each date
    for date_key, date_info in schedule_data.items():
        date_obj = date_info['date_obj']
        available_slots_p1 = []
        available_slots_p2 = []
        
        for i, slot_start in enumerate(time_slots):
            if i + 1 < len(time_slots):
                slot_end = time_slots[i + 1]
                
                # Check Panel 1 availability
                is_available_p1 = check_time_available(date_obj, slot_start, slot_end, panel1_schedules[date_key])
                available_slots_p1.append({
                    'time': slot_start.strftime('%I:%M %p'),
                    'available': is_available_p1
                })
                
                # Check Panel 2 availability
                is_available_p2 = check_time_available(date_obj, slot_start, slot_end, panel2_schedules[date_key])
                available_slots_p2.append({
                    'time': slot_start.strftime('%I:%M %p'),
                    'available': is_available_p2
                })
        
        date_info['time_slots_p1'] = available_slots_p1
        date_info['time_slots_p2'] = available_slots_p2
    
    context = {
        'schedule_data': schedule_data,
        'has_interviews': interviews.exists()
    }
    
    return render(request, 'scheduler/schedule.html', context)

