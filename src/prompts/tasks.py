MESSAGE_CATEGORIZER_TASK = """
Instructions:
    1. Review the provided message content thoroughly.
    2. Assign one or more of the following categories. Assign multiple only when the message clearly contains distinct intents (e.g. asking about an order AND a product in the same message):
      - **order_inquiry**: The user wants any information about orders — checking order status, tracking a shipment, listing all orders, or retrieving a specific order by ID.
      - **product_inquiry**: The user wants information about products — browsing the catalog, checking availability, specs, pricing, or retrieving a specific product by ID.
      - **complaint**: The user expresses dissatisfaction, reports a problem, or files a complaint about the store or a product.
      - **policy_question**: The user asks about store policies such as returns, warranties, shipping, or payment terms.
      - **other**: The message does not clearly fit any of the above categories.

MESSAGE CONTENT:
{message}

Notes:
    - Use the exact category names listed above.
    - Base your categorization strictly on the message content; avoid assumptions.
    - When the user mentions an order ID or asks "what are my orders", always use order_inquiry.
    - When the user mentions a product ID or asks "what products do you have", always use product_inquiry.
"""

