// ===== Spring Boot Mastery Course - Script =====

// Theme Toggle
const themeToggle = document.querySelector('.theme-toggle');
const html = document.documentElement;

function setTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem('sb-theme', theme);
    if (themeToggle) themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
}

themeToggle?.addEventListener('click', () => {
    const current = html.getAttribute('data-theme');
    setTheme(current === 'dark' ? 'light' : 'dark');
});

// Load saved theme
const savedTheme = localStorage.getItem('sb-theme') || 'light';
setTheme(savedTheme);

// Sidebar Toggle (Mobile)
const hamburger = document.querySelector('.hamburger');
const sidebar = document.querySelector('.sidebar');
const overlay = document.querySelector('.sidebar-overlay');

hamburger?.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    overlay.classList.toggle('active');
});

overlay?.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
});

// Active sidebar link
const currentPage = window.location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.sidebar-nav a').forEach(link => {
    if (link.getAttribute('href') === currentPage) {
        link.classList.add('active');
        link.scrollIntoView({ block: 'center', behavior: 'instant' });
    }
});

// Progress tracking
function updateProgress() {
    const completed = JSON.parse(localStorage.getItem('sb-completed') || '[]');
    const total = 72;
    const pct = Math.round((completed.length / total) * 100);
    const label = document.querySelector('.progress-label');
    const fill = document.querySelector('.progress-bar-fill');
    if (label) label.textContent = `Progress: ${completed.length}/${total} topics completed`;
    if (fill) fill.style.width = `${pct}%`;
}

updateProgress();

// Mark topic as complete
function markComplete(topicNum) {
    const completed = JSON.parse(localStorage.getItem('sb-completed') || '[]');
    if (!completed.includes(topicNum)) {
        completed.push(topicNum);
        localStorage.setItem('sb-completed', JSON.stringify(completed));
    }
    updateProgress();
}
