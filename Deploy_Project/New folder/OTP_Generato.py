import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_otp(length=6):
    """Generate a random OTP of specified length"""
    digits = "0123456789"
    otp = ""
    for _ in range(length):
        otp += random.choice(digits)
    return otp

def send_otp_email(receiver_email, otp):
    """Send OTP via email"""
    # Email configuration
    sender_email = "sumitmaheshwq@gmail.com"  # Replace with your email
    sender_password = "Sumit#22032002"   # Replace with your app password
    
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Your OTP Code"
    
    # Email body
    body = f"""
    Your OTP code is: {otp}
    
    This code will expire in 10 minutes.
    Do not share this code with anyone.
    """
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Create SMTP session
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        # Login to sender email
        server.login(sender_email, sender_password)
        
        # Send email
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return True
    
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def main():
    # Example usage
    receiver_email = "sumitmahesh12@gmail.com"  # Replace with recipient's email
    
    # Generate OTP
    otp = generate_otp()
    print(f"Generated OTP: {otp}")
    
    # Send OTP via email
    if send_otp_email(receiver_email, otp):
        print("OTP sent successfully!")
    else:
        print("Failed to send OTP")

if __name__ == "__main__":
    main()