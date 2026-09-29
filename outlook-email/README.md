# Send Outlook Email

Sends mail from Python through the Outlook desktop client, using whichever account
is already signed in.

## Why not SMTP

The usual answer is `smtplib`, which needs a server address, a port, TLS settings,
and credentials — and on a corporate tenant that increasingly means an app password
or an OAuth app registration, neither of which you can just decide to create.

Driving the installed Outlook client over COM sidesteps all of it. Outlook is
already authenticated as you; this asks it to send a message. No credentials appear
anywhere in the script, so there's nothing to leak into source control, and mail
goes out from the real account with the real signature and lands in Sent Items.

The trade-off: Windows only, and Outlook has to be installed. For a scheduled report
off a work machine, that's usually already true.

## Usage

```bash
pip install pywin32
python send_outlook_email.py
```

`CreateItem(0)` is `olMailItem` — the Outlook enum value for a mail message. Setting
`HTMLBody` gives formatted mail; `Body` gives plain text, and if both are set the
HTML one wins.

`.Send()` sends immediately. Swap it for `.Display()` while you're developing — that
opens the composed message in Outlook so you can check it before it goes anywhere.
Worth doing on the first run of anything that emails a list.

Attachments take absolute paths, added one call at a time.
