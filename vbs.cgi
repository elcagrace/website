#! /home/elcagrace/opt/python-3.7.1/bin/python3

import os
import socket
import pickle

from server import load_skips, load_content, load_form, serve
from server.forms import get_parameters, save_to_csv
from server.send_email import send_email_to_one_recipient


# PATH = '/home/elcagrace/responses/vbs-2019.csv'

# KEYS = (
#     'vbs-name',
#     'vbs-grade',
#     'vbs-date-of-birth',
#     'vbs-pictures',
#     'vbs-health',
#     'vbs-accommodations',
#     'vbs-contact',
#     'vbs-contact-phone',
#     'vbs-contact-e-mail',
#     'vbs-emergency-contact',
#     'vbs-emergency-contact-phone',
#     'vbs-additional-ride-1',
#     'vbs-additional-ride-2',
#     'vbs-supper',
# )

# SUCCESS = 'Your enrollment of {vbs-name} has been submitted successfully, ' \
#           'and a confirmation e-mail has been sent to {vbs-contact-e-mail}.  ' \
#           'You can continue to enroll additional students.'

# FAILURE = 'Your enrollment of {vbs-name} has been submitted successfully, but ' \
#           'we were unable to send a confirmation e-mail to ' \
#           '{vbs-contact-e-mail}.  You can resubmit or continue to enroll ' \
#           'additional students.'

# ADDRESS = '{vbs-contact-e-mail}'
# SUBJECT = 'VBS 2019 Enrollment'
# BODY = '''{vbs-contact},

# This e-mail is to confirm that you have enrolled

#   {vbs-name}

# for "VBS 2019: Who is my Neighbor?" at Grace Lutheran Church (2225
# Washington St., Lincoln, NE) from 6:00 PM to 8:00 PM on July 29
# through August 2 with supper served from 5:30 to 6:00.  If you need to
# cancel or modify this enrollment, please contact office@egrace.org.

# This enrollment request came from:

#   "{inviter}"

# If you did not make this enrollment, or if you believe you have
# received this message in error, please contact office@egrace.org so
# that we can prevent similar messages from being sent in the future.

# Thank you!
# The egrace.org Enrollment Management Bot
# '''


# parameters = get_parameters(KEYS, False)
# substitutions = get_parameters(KEYS, True)
# try:
#     substitutions['inviter'] = socket.gethostbyaddr(os.environ.get('REMOTE_ADDR', ''))[0]
# except:
#     substitutions['inviter'] = os.environ.get('REMOTE_ADDR', '')


# def send_confirmation_email():
#     with open('/home/elcagrace/no_reply.pickle', 'rb') as no_reply_credentials_file:
#         no_reply_credentials = pickle.load(no_reply_credentials_file)
#         send_email_to_one_recipient(
#             no_reply_credentials['server'],
#             no_reply_credentials['account'],
#             no_reply_credentials['password'],
#             ADDRESS.format(**substitutions),
#             SUBJECT.format(**substitutions),
#             BODY.format(**substitutions),
#         )


# if parameters['vbs-name'] is None:
#     serve(
#         origin=__file__,
#         title='VBS Enrollment – Grace Lutheran Church, Lincoln, Nebraska',
#         skips=load_skips(origin=__file__),
#         content=load_content(origin=__file__),
#         scripts=(
#             'vbs.js',
#         ),
#     )
# else:
#     save_to_csv(PATH, KEYS)
#     try:
#         send_confirmation_email()
#         substitutions['message'] = SUCCESS.format(**substitutions)
#     except:
#         substitutions['message'] = FAILURE.format(**substitutions)
#     serve(
#         origin=__file__,
#         title='VBS Enrollment – Grace Lutheran Church, Lincoln, Nebraska',
#         skips=load_skips(origin=__file__),
#         content=load_form(origin=__file__, substitutions=substitutions),
#         scripts=(
#             'vbs.js',
#         ),
#     )

serve(
	origin=__file__,
	title='VBS Enrollment – Grace Lutheran Church, Lincoln, Nebraska',
	skips=load_skips(origin=__file__),
	content=load_content(origin=__file__),
	scripts=(
		'vbs.js',
	),
)
