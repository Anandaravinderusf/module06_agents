# contact_change_queue.py
# Author: Ananda Ravinder


class ContactChangeQueue:
    """Store contact preference changes until staff approves them."""

    def __init__(self, customers):
        """Store mock customers and start an empty request list."""
        self.customers = customers
        self.requests = []

    def request_contact_change(self, customer_id, new_method):
        """Ask staff to update a customer's contact preference.

        Args:
            customer_id: The customer ID, like C100.
            new_method: The requested contact method, email or phone.
        """
        customer_id = customer_id.upper()
        new_method = new_method.lower()

        if customer_id not in self.customers:
            return "That customer ID was not found."

        if new_method not in ["email", "phone"]:
            return "The contact method must be email or phone."

        number = len(self.requests) + 1
        request = {
            "number": number,
            "customer_id": customer_id,
            "new_method": new_method,
            "status": "waiting",
        }

        self.requests.append(request)
        return f"Request {number} was sent to staff. No changes have been made yet."

    def waiting(self):
        """Return requests that still need staff approval."""
        result = []
        for request in self.requests:
            if request["status"] == "waiting":
                result.append(request)
        return result

    def find(self, number):
        """Find a request using its number."""
        for request in self.requests:
            if request["number"] == number:
                return request
        return None

    def approve(self, number):
        """Approve one request and update the contact preference."""
        request = self.find(number)

        if request is None:
            return f"There is no request {number}."

        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."

        request["status"] = "approved"
        customer_id = request["customer_id"]
        self.customers[customer_id]["contact_method"] = request["new_method"]

        return f"Request {number} approved."

    def reject(self, number):
        """Reject a request without changing anything."""
        request = self.find(number)

        if request is None:
            return f"There is no request {number}."

        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."

        request["status"] = "rejected"
        return f"Request {number} rejected."
