# 📧 Intelligent Email Job Request Processor

A Python application that automates the processing of job request emails using AI analysis. This tool connects to your email inbox via IMAP, analyzes incoming messages using the Claude AI API, and converts relevant job requests into structured JSON data.

## ✨ Features

- 🔒 Secure IMAP email server connection and authentication
- 📨 Automated email content extraction and preprocessing
- 🤖 Intelligent message analysis using Claude AI
- 🔄 Structured JSON output for job request details
- 📝 Support for multiple email formats and encodings
- ⚙️ Configurable processing limits and folder selection
- 📦 Automatic handling of multipart messages

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/chrisrobison/emailbuddy.git
cd emailbuddy
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```
or 
```bash
pip install imaplib-ssl anthropic
```

3. Set up environment variables:
```bash
# Linux/Mac 🐧 🍎
export EMAIL_ADDRESS="your.email@domain.com"
export EMAIL_PASSWORD="your_password"
export IMAP_SERVER="imap.your-server.com"
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Windows 🪟
set EMAIL_ADDRESS=your.email@domain.com
set EMAIL_PASSWORD=your_password
set IMAP_SERVER=imap.your-server.com
set ANTHROPIC_API_KEY=your-anthropic-api-key
```

## 💻 Usage

1. Basic usage:
```python
// example.py
from emailbuddy import EmailBuddy

processor = EmailBuddy(email_address, password, imap_server)
results = processor.process_emails(limit=5)  # Process last 5 emails
```

2. Run the main script:
```bash
python example.py
```

The script will:
- 🔌 Connect to your email server
- 📥 Process the specified number of recent emails
- 📊 Generate a JSON file containing any identified job requests
- 💾 Save the results with a timestamp in the filename

## 📄 Output Format

Job requests are converted to JSON with the following structure:
```json
{
    "type": "job_request",
    "timestamp": "2024-12-21 10:30:00",
    "subject": "New Project Request - Website Redesign",
    "requestor": "John Smith",
    "project": "Website Redesign",
    "description": "Complete overhaul of company website",
    "priority": "high",
    "deadline": "2025-01-15",
    "requirements": [
        "React expertise",
        "Mobile-first design",
        "SEO optimization"
    ],
    "additional_notes": "Budget approval pending"
}
```

## ⚙️ Configuration

You can customize the following parameters in the `EmailProcessor` class:
- 🔌 IMAP port (default: 993)
- 📁 Email folder (default: "INBOX")
- 🔢 Processing limit (default: 10 messages)
- 🎯 AI model parameters (temperature, max tokens)

## 🔒 Security Notes

- 🔑 Store sensitive credentials in environment variables or a secure configuration manager
- 🔐 Use SSL/TLS for email connections (default port 993)
- ⏱️ Consider implementing rate limiting for API calls
- 🔄 Regularly rotate API keys and credentials

## 🤝 Contributing

1. 🍴 Fork the repository
2. 🌿 Create a feature branch
3. 💾 Commit your changes
4. 🚀 Push to the branch
5. 📬 Create a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- 🤖 Uses the Anthropic Claude API for message analysis
- 🐍 Built with Python's imaplib for email processing
