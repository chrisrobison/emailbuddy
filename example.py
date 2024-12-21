from emailbuddy import EmailBuddy

processor = EmailBuddy(email_address, password, imap_server)
results = processor.process_emails(limit=5)  # Process last 5 emails
