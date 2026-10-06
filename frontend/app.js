document.addEventListener('DOMContentLoaded', () => {
    const ticketForm = document.getElementById('ticket-form');
    const statusElement = document.getElementById('status');

    if (ticketForm) {
        ticketForm.addEventListener('submit', (event) => {
            event.preventDefault();
            statusElement.textContent = 'Ticket submission will be connected on Day 3.';
        });
    }
});