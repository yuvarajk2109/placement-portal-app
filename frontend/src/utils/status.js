export function companyStatusClass(status) {
    return {
        Pending: 'is-warning',
        Approved: 'is-success',
        Rejected: 'is-error',
    } [status] ||'is-info'
};

export function driveStatusClass(status) {
    return {
        Pending: 'is-warning',
        Approved: 'is-success',
        Rejected: 'is-error',
        Closed: 'is-secondary'
    } [status] || 'is-info';
}

export function applicationStatusClass(status) {
    return {
        Applied: 'is-info', 
        Shortlisted: 'is-warning', 
        Interview: 'is-warning',
        Selected: 'is-success',
        Rejected: 'is-error',
        Inactive: 'is-warning'
    } [status] || 'is-neutral';
}

export function interviewStatusClass(status) {
    return {
        Pending: 'is-warning',
        Approved: 'is-success',
        Rejected: 'is-error',
        Closed: 'is-secondary'
    } [status] || 'is-info'
}