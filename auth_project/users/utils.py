from django.core.mail import send_mail

def notify_user(user, approved: bool):
    subject = 'Account Approval Status'
    message = (
        'Your account has been approved! You may now log in.'
        if approved else
        'Unfortunately, your account request has been rejected.'
    )
    send_mail(
        subject,
        message,
        'minthwayhtut568@gmail.com',
        [user.email],
        fail_silently=False
    )