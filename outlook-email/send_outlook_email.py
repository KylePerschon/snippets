# Author: Kyle Perschon
# Purpose: Send mail through the Outlook desktop client via COM, using the
#          signed-in profile — no SMTP server, credentials or app password.
import win32com.client

outlook = win32com.client.Dispatch('outlook.application')

mail = outlook.CreateItem(0)          # 0 = olMailItem
mail.To = 'recipient@example.com'
mail.CC = 'someone.else@example.com'
mail.Subject = 'Sample Email'

# Set HTMLBody for formatted mail, or Body for plain text. Setting both means
# HTMLBody wins.
mail.HTMLBody = '<h3>This is the HTML body</h3>'
# mail.Body = 'This is the plain text body'

# mail.Attachments.Add(r'C:\path\to\report.xlsx')

mail.Send()                           # .Display() opens it for review instead
