def extract_messages(request):
    """
    Extracts messages from the request object and returns them as a list of dictionaries.
    Each dictionary contains the message level tag and the message text.

    Args:
        request: The HTTP request object containing the messages

    Returns:
        list: A list of dictionaries, where each dictionary has:
            - level (str): The message level tag (e.g. 'info', 'error')
            - message (str): The message text
   """
    from django.contrib.messages import get_messages
   
    return [
        {"level": message.level_tag, "message": message.message}
        for message in get_messages(request)
    ]


def get_rate_type_label(multiplier):
    """
    Converts a pay rate multiplier to its corresponding label.

    Args:
        multiplier (float or str): The pay rate multiplier value (0.0, 1.0, 1.5, or 2.0)

    Returns:
        str: The label corresponding to the multiplier:
            - 'Unpaid' for 0.0
            - 'Ord' (Ordinary) for 1.0 
            - 'Ovt' (Overtime) for 1.5
            - 'Dt' (Double Time) for 2.0
            - 'Ord' as default for any other value

    Examples:
        >>> get_rate_type_label(1.5)
        'Ovt'
        >>> get_rate_type_label(0.0) 
        'Unpaid'
    """

    rate_map = {
        0.0: 'Unpaid',
        1.0: 'Ord',
        1.5: 'Ovt',
        2.0: 'Dt'
    }
    
    return rate_map.get(float(multiplier), 'Ord')  # Default to 'Ord' if not found

def get_jobs_data(related_jobs):
    """
    Retrieves and formats job data for the given related jobs.

    Args:
        related_jobs (set): A set of Job objects

    Returns:
        list: A list of dictionaries, where each dictionary contains job data:
            - id (str): The job ID
            - job_number (str): The job number
            - name (str): The job name
            - job_display_name (str): The job display name
            - client_name (str): The client name
            - charge_out_rate (float): The charge out rate
    """
    from workflow.models import Job

    return [
        {
            "id": str(job_id),
            "job_number": Job.objects.get(id=job_id).job_number,
            "name": Job.objects.get(id=job_id).name,
            "job_display_name": str(Job.objects.get(id=job_id)),
            "client_name": Job.objects.get(id=job_id).client.name if Job.objects.get(id=job_id).client else "NO CLIENT!?",
            "charge_out_rate": float(Job.objects.get(id=job_id).charge_out_rate),
        }
        for job_id in related_jobs
    ]
