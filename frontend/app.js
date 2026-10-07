function formatLocalTime(iso) {
    const date = new Date(iso);
    if (Number.isNaN(date.getTime())) {
        return iso;
    }
    return date.toLocaleString();
}

async function loadTickets() {
    const container = document.getElementById('tickets');
    const response = await fetch('/api/tickets');
    const tickets = await response.json();
    container.textContent = '';
    if (tickets.length === 0) {
        container.textContent = 'No tickets yet.';
        return;
    }
    for (const t of tickets) {
        const card = document.createElement('div');
        card.className = 'card ' + t.priority;
        const title = document.createElement('h3');
        title.textContent = t.subject;
        const desc = document.createElement('p');
        desc.textContent = t.description;
        const meta = document.createElement('p');
        meta.className = 'meta';
        meta.textContent = 'Category: ' + t.category + ' (' + Math.round(t.confidence * 100) + '%) | Priority: ' + t.priority + ' | ' + formatLocalTime(t.created_at);
        card.append(title, desc, meta);
        if (t.confidence < 0.5) {
            const flag = document.createElement('p');
            flag.className = 'low-confidence';
            flag.textContent = '⚠️ Low confidence ⚠️';
            card.appendChild(flag);
        }
        container.appendChild(card);

    }
}

loadTickets();

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
                const { created_at } = data;
                console.log(formatLocalTime(created_at));
                data.created_at = formatLocalTime(created_at);


                statusElement.textContent = `Ticket saved. Category: ${data.category}, priority: ${data.priority}.`;
                ticketForm.reset();
                loadTickets();
            } catch (error) {
                statusElement.textContent = 'Could not reach the server. Please try again.';
            }
        });
    }
});
