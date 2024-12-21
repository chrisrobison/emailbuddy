import imaplib
import email
from email.header import decode_header
import json
import os
from anthropic import Anthropic
from datetime import datetime

class EmailBuddy:
    def __init__(self, email_address, password, imap_server, imap_port=993):
        """Initialize the email processor with connection details."""
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    def connect(self):
        """Establish connection to the IMAP server."""
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.mail.login(self.email_address, self.password)
            return True
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False

    def get_email_content(self, email_message):
        """Extract the content from an email message."""
        content = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        content += part.get_payload(decode=True).decode()
                    except:
                        continue
        else:
            try:
                content = email_message.get_payload(decode=True).decode()
            except:
                content = email_message.get_payload()
        return content

    def decode_email_subject(self, email_message):
        """Decode email subject with proper character encoding."""
        subject = email_message["subject"]
        if subject is None:
            return ""
        decoded_header = decode_header(subject)
        decoded_subject = ""
        for content, encoding in decoded_header:
            if isinstance(content, bytes):
                try:
                    decoded_subject += content.decode(encoding if encoding else 'utf-8')
                except:
                    decoded_subject += content.decode('utf-8', 'ignore')
            else:
                decoded_subject += content
        return decoded_subject

    def analyze_message(self, subject, content):
        """Send message content to Claude for analysis."""
        prompt = f"""Analyze this email with subject: "{subject}" and content:
        
        {content}
        
        If this is a job request email, create a JSON object with the following structure:
        {{
            "type": "job_request",
            "timestamp": "YYYY-MM-DD HH:MM:SS",
            "subject": "original email subject",
            "requestor": "extracted name of person making request",
            "project": "extracted project name or identifier",
            "description": "extracted job description",
            "priority": "extracted priority level (high/medium/low)",
            "deadline": "extracted deadline if any (YYYY-MM-DD format)",
            "requirements": ["extracted", "list", "of", "requirements"],
            "additional_notes": "any other relevant information"
        }}
        
        If this is not a job request email, return null.
        
        Return only the JSON object or null, with no additional text."""

        response = self.anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0,
            system="You are a helpful assistant that analyzes emails and extracts job request information into JSON format. Only output valid JSON or null.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            result = json.loads(response.content)
            return result
        except json.JSONDecodeError:
            return None

    def process_emails(self, folder="INBOX", limit=10):
        """Process emails from specified folder and return analysis results."""
        if not self.connect():
            return []

        self.mail.select(folder)
        _, message_numbers = self.mail.search(None, "ALL")
        
        results = []
        for num in message_numbers[0].split()[-limit:]:  # Process last 'limit' messages
            _, msg_data = self.mail.fetch(num, "(RFC822)")
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            subject = self.decode_email_subject(email_message)
            content = self.get_email_content(email_message)
            
            analysis = self.analyze_message(subject, content)
            if analysis:  # Only append if it's a job request
                results.append(analysis)

        self.mail.logout()
        return results

def main():
    # Load environment variables
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    imap_server = os.getenv("IMAP_SERVER")
    
    if not all([email_address, email_password, imap_server]):
        print("Please set all required environment variables")
        return
    
    processor = EmailProcessor(email_address, email_password, imap_server)
    results = processor.process_emails(limit=5)  # Process last 5 emails
    
    # Save results to JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"job_requests_{timestamp}.json"
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Processed results saved to {output_file}")

if __name__ == "__main__":
    main()
