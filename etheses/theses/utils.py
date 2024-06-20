from django.core.mail import send_mail, EmailMessage
from django.conf import settings


def send_reviewer_email(lecturer_email, council):
    subject = 'Bạn đã được chỉ định làm giảng viên phản biện'
    message = f'Bạn đã được phân công làm giảng viên phản biện của hội đồng: {council}.'
    from_email = 'Thesis Management <{}>'.format(settings.DEFAULT_FROM_EMAIL)
    email = EmailMessage(subject, message, from_email, to=[lecturer_email])
    email.send()

# def send_reviewer_email(self, council, lecturer):
#     lecturer_email = lecturer.user.email
#     lecturer_name = lecturer.full_name
#     council_name = council.name
#     subject = f'Bạn đã được giao làm phản biện cho hội đồng "{council_name}"'
#     message = (
#         f'Chào {lecturer_name}\nBạn đã được giao vai trò phản biện cho hội đồng "{council_name}".\n'
#         'Vui lòng chuẩn bị và liên hệ với các thành viên khác trong hội đồng để hoàn thành nhiệm vụ của mình.\n'
#         '__Giáo vụ__'
#     )
#
#     from_email = 'Thesis Management <{}>'.format(settings.DEFAULT_FROM_EMAIL)
#
#     email = EmailMessage(subject, message, from_email, to=[lecturer_email])
#     email.send()
