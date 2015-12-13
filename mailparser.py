#!/usr/bin/env python

import getpass, imaplib
import sys
import email
import email.header
import datetime
import collections
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

DEFAULT_IMAP_SERVER = "mail.stillroot.org"
DEFAULT_IMAP_USER   = "oleg@hobbykeller.org"
DEFAULT_IMAP_FOLDER = "ML/riot/internal-notifications"

imaphost = DEFAULT_IMAP_SERVER
imapuser = DEFAULT_IMAP_USER

per_month = dict()

M = imaplib.IMAP4_SSL(imaphost)
M.login(imapuser, getpass.getpass())
M.select(DEFAULT_IMAP_FOLDER)
typ, data_sub = M.search(None, 'SUBJECT', '"%s subscription notification"' % sys.argv[1])
typ, data_unsub = M.search(None, 'SUBJECT', '"%s unsubscribe notification"' % sys.argv[1])
for num in data_sub[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    msg = email.message_from_string(data[0][1])
    decode = email.header.decode_header(msg['Subject'])[0]
    subject = unicode(decode[0])
    #print('Message %s: %s' % (num, subject))
    date_tuple = email.utils.parsedate_tz(msg['Date'])
    try:
        per_month[(date_tuple[0], date_tuple[1])] += 1
    except KeyError:
        per_month[(date_tuple[0], date_tuple[1])] = 1
for num in data_unsub[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    msg = email.message_from_string(data[0][1])
    decode = email.header.decode_header(msg['Subject'])[0]
    subject = unicode(decode[0])
    #print('Message %s: %s' % (num, subject))
    date_tuple = email.utils.parsedate_tz(msg['Date'])
    try:
        per_month[(date_tuple[0], date_tuple[1])] -= 1
    except KeyError:
        per_month[(date_tuple[0], date_tuple[1])] = -1
M.close()
M.logout()

od = collections.OrderedDict(sorted(per_month.items()))

fig = figure()
ylabel("subscriptions per month")
xlabel("Month")

months = [] 
month_labels = []
for k in od.keys():
    months.append(k)
    month_labels.append("%s-%02i" % (k[0], k[1]))
subs = []
subs_all = []
last_subs = 0
for v in od.values():
    subs.append(v)
    subs_all.append(last_subs + v)
    last_subs = last_subs + v
print(months)
print(subs)
xticks(np.arange(len(months)), month_labels, rotation='vertical', size='x-small')

p = []
p.append(plt.plot(np.arange(len(months)), subs, label="Monthly", marker='o'))
p.append(plt.plot(np.arange(len(months)), subs_all, label="Overall", marker='+'))

plt.legend(loc='upper left')

matplotlib.pyplot.savefig("%s-subs.pdf" % sys.argv[1], format='pdf', pad_inches=2)
