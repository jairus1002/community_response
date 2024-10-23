from flask import Flask, request
import africastalking

app = Flask(__name__)

# Initialize Africa's Talking
username = "Sandbox"  # Use 'sandbox' if using the sandbox environment
api_key = "atsk_7ab5eb7344b16d5b8bb583e8eb49d0d2a18e7b91ff86389f0887366b4dea08ac587b9eae"  # Your Africa's Talking API key

africastalking.initialize(username, api_key)
ussd_service = africastalking.USSD

# Store temporary session data (in production, use proper storage like Redis or a database)
user_sessions = {}

# First menu prompt
def first_menu():
    response = "CON Welcome to University Community Service\n"
    response += "1. Request Information\n"
    response += "2. Report an Issue\n"
    response += "3. Request a Service\n"
    return response

# Request Information menu
def request_information_menu():
    response = "CON What information would you like to request?\n"
    response += "1. Campus Security Contacts\n"
    response += "2. Health Services Contacts\n"
    response += "3. Class Schedules\n"
    return response

# Report an Issue menu
def report_issue_menu():
    response = "CON What issue would you like to report?\n"
    response += "1. Security concern\n"
    response += "2. Health emergency\n"
    response += "3. Teaching venue problem\n"
    response += "4. Infrastructure problem\n"
    return response

# Request a Service menu
def request_service_menu():
    response = "CON What service would you like to request?\n"
    response += "1. Maintenance Service\n"
    response += "2. Cleaning Service\n"
    response += "3. IT Support\n"
    return response

# Function to handle USSD requests
@app.route('/ussd', methods=['POST'])
def ussd():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    # Get the current user's session data, if any
    session = user_sessions.get(phone_number, {})
    step = session.get('step', 0)
    user_response = text.split("*")

    # USSD logic
    if text == "":
        # Display first menu
        response = first_menu()
        session['step'] = 1  # Update step
    elif text == "1" and step == 1:
        # User chooses to Request Information
        response = request_information_menu()
        session['step'] = 2
    elif text == "2" and step == 1:
        # User chooses to Report an Issue
        response = report_issue_menu()
        session['step'] = 2
    elif text == "3" and step == 1:
        # User chooses to Request a Service
        response = request_service_menu()
        session['step'] = 2

    # Request Information Pathway
    elif step == 2 and user_response[0] == "1":
        # User wants information
        if user_response[-1] == "1":
            response = "END Campus Security Contacts: 0712 345 678"
        elif user_response[-1] == "2":
            response = "END Health Services Contacts: 0722 111 222"
        elif user_response[-1] == "3":
            response = "END Class Schedules: Visit class schedule portal at http://university.edu/schedule"
        else:
            response = "END Invalid selection."
    
    # Report an Issue Pathway
    elif step == 2 and user_response[0] == "2":
        # User selects issue type
        issue_type = user_response[-1]
        if issue_type in ["1", "2", "3", "4"]:
            response = "CON Please describe the issue briefly:"
            session['step'] = 3
            session['issue_type'] = issue_type  # Save issue type
        else:
            response = "END Invalid selection."
    
    elif step == 3 and session.get('issue_type'):
        # User describes the issue
        issue_description = text
        response = f"CON Confirm your report:\n"
        response += f"Issue: {session['issue_type']} \nDescription: {issue_description}\n"
        response += "1. Submit\n"
        response += "2. Cancel"
        session['issue_description'] = issue_description
        session['step'] = 4

    elif step == 4 and session.get('issue_type') and session.get('issue_description'):
        if user_response[-1] == "1":
            # Confirm and submit the issue report
            response = "END Your issue report has been submitted successfully."
            session.clear()  # Clear session after completion
        elif user_response[-1] == "2":
            # Cancel the report
            response = "END Your issue report has been canceled."
            session.clear()  # Clear session after cancellation
        else:
            response = "END Invalid selection."
    
    # Request a Service Pathway
    elif step == 2 and user_response[0] == "3":
        service_type = user_response[-1]
        if service_type in ["1", "2", "3"]:
            response = f"CON Confirm your service request:\nService: {service_type}\n"
            response += "1. Submit\n"
            response += "2. Cancel"
            session['service_type'] = service_type
            session['step'] = 3
        else:
            response = "END Invalid selection."

    elif step == 3 and session.get('service_type'):
        if user_response[-1] == "1":
            # Confirm and submit the service request
            response = "END Your service request has been submitted successfully."
            session.clear()  # Clear session after submission
        elif user_response[-1] == "2":
            # Cancel the request
            response = "END Your service request has been canceled."
            session.clear()  # Clear session after cancellation
        else:
            response = "END Invalid selection."
    
    # Save or update the session
    user_sessions[phone_number] = session
    return response

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
