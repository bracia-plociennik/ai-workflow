# Interaction And Recovery

For every meaningful action define:

- initial state;
- pending/loading state;
- success state;
- validation or blocked state;
- failure state;
- recovery action and retry behavior;
- permission or confirmation boundary;
- stale or concurrent state when data can change remotely.

Never present an optimistic success state when the backend, wallet, payment provider, or external service has not confirmed the operation. Recovery should preserve user input where safe and explain what can be retried.
