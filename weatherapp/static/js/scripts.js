// static/js/loading.js

function showLoading() {
    // Create the loading overlay
    const loadingOverlay = document.createElement('div');
    loadingOverlay.className = 'loading-overlay';
    
    // Create the semi-transparent overlay
    const overlay = document.createElement('div');
    overlay.className = 'overlay';
    loadingOverlay.appendChild(overlay);

    // Create the spinner
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border text-light';
    spinner.setAttribute('role', 'status');

    // Create the "Loading..." text
    const srOnly = document.createElement('span');
    srOnly.className = 'sr-only';
    srOnly.textContent = 'Loading...';

    spinner.appendChild(srOnly);
    loadingOverlay.appendChild(spinner);

    document.body.appendChild(loadingOverlay);
}

function hideLoading() {
    const loadingOverlay = document.querySelector('.loading-overlay');
    if (loadingOverlay) {
        document.body.removeChild(loadingOverlay);
    }
}
