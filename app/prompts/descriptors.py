TOOL_DESCRIPTOR = """

Here are the supported filter types and their operators:

Date, DateTime:
  - Operators: equals, not_equal, greater_equal, greater_than, less_equal, less_than, between, in

Integer, Currency, Decimal, BigInt, Percent:
  - Operators: equals, not_equal, greater_equal, greater_than, less_equal, less_than, between, in

Boolean:
  - Operators: equals, not_equal

Textarea:
  - Operators: equals, not_equal, starts_with

Lookup(user/owner), Picklist, Autonumber:
  - Operators: equals, not_equal, in

Text, Email, Phone, Website:
  - Operators: equals, not_equal, starts_with, in

MultiselectPicklist:
  - Operators: equals, not_equal, in, starts_with

Formula:
  - Operators depend on return type

Rules:
- You can only use a maximum of 10 filters.
- When data_type is "date" use YYYY-MM-DD format without time.
- Choose filters that logically match the user’s intent.
- Only use the allowed fields listed above.
- You must include both key and value (with operator) for each filter.

"""


FORMAT_INSTRUCTIONS = """
For Example, return ONLY valid JSON in the following format:
{
  "filters": [
    {
      "key": "Amount",
      "value": {
        "operator": "greater_than",
        "value": 10000
      }
    },
    {
      "key": "Country",
      "value": {
        "operator": "equals",
        "value": "India"
      }
    },
    {
      "key": "Time_Contacted",
      "value": {
        "operator": "equals",
        "value": "YYYY-MM-DD"
      }
    },
    {
      "key": "Created_Time",
      "value": {
        "operator": "between",
        "value": [
          "YYYY-MM-DDTHH:MM:SS+00:00",
          "YYYY-MM-DDTHH:MM:SS+00:00"
        ]
      }
    }
  ]
}
"""