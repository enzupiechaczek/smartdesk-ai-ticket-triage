// Placeholder until the ticket dashboard is built in the next task.
async function loadTickets() {}

document.addEventListener('DOMContentLoaded', () => {
    const ticketForm = document.getElementById('ticket-form');
    const statusElement = document.getElementById('status');

    if (ticketForm) {
        ticketForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const subject = document.getElementById('subject').value;
            const description = document.getElementById('description').value;

            try {
                const response = await fetch('/api/tickets', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ subject, description })
                });
                const data = await response.json();

                if (!response.ok) {
                    statusElement.textContent = data.error;
                    return;
                }

                statusElement.textContent = `Ticket saved. Category: ${data.category}, priority: ${data.priority}.`;
                ticketForm.reset();
                loadTickets();
            } catch (error) {
                statusElement.textContent = 'Could not reach the server. Please try again.';
            }
        });
    }
});
