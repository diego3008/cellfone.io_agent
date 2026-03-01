MESSAGE_CATEGORIZER_TASK = """
Instructions:
    1. Review the provided message content thoroughly.
    2. Use the following rules to assign the correct category:
      - **product_enquiry**: When the message seeks information about a product feature, benefit, service, or pricing.
      - **customer_complaint**: When the message communicates dissatisfaction or a complaint.
      - **customer_feedback**: When the message provides feedback or suggestions regarding a product or service.
      - **operations_request**: When the message content is related to perform operations on store data.
      - **unrelated**: When the message content does not match any of the above categories.

MESSAGE CONTENT:
{message}

Notes:
    Base your categorization strictly on the message content provided; avoid making assumptions or overgeneralizing.
"""

