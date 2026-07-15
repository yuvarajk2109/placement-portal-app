export function formatDateTime(value) {
    if (!value) return '';

    return new Date(value).toLocaleString('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    });
}

export function formatDate(value) {
    if (!value) return '';

    return new Date(value).toLocaleDateString('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

export function formatSalary(value) {
    if (!value && value !== 0) return '—';
    return (value / 100000).toFixed(2);
}
