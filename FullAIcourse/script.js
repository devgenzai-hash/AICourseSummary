/* ============================================
   FULL AI/LLM ENGINEERING COURSE - SCRIPTS
   Navigation, Theme, Progress, Interactivity
   ============================================ */

// Theme Toggle
function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('ai-course-theme', next);
    updateThemeButton(next);
}

function updateThemeButton(theme) {
    const btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// Initialize theme
(function initTheme() {
    const saved = localStorage.getItem('ai-course-theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    document.addEventListener('DOMContentLoaded', () => updateThemeButton(saved));
})();

// Active page detection
document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const links = document.querySelectorAll('.sidebar nav a');
    links.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage) {
            link.classList.add('active');
            // Scroll sidebar to active item
            setTimeout(() => {
                link.scrollIntoView({ block: 'center', behavior: 'smooth' });
            }, 100);
        }
    });

    // Hamburger menu toggle
    const hamburger = document.querySelector('.hamburger');
    const sidebar = document.querySelector('.sidebar');
    if (hamburger && sidebar) {
        hamburger.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
        // Close sidebar on link click (mobile)
        links.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('open');
                }
            });
        });
    }

    // Copy buttons for code blocks
    document.querySelectorAll('pre').forEach(block => {
        const btn = document.createElement('button');
        btn.className = 'copy-btn';
        btn.textContent = 'Copy';
        btn.addEventListener('click', () => {
            const code = block.querySelector('code');
            const text = code ? code.textContent : block.textContent;
            navigator.clipboard.writeText(text).then(() => {
                btn.textContent = 'Copied!';
                btn.classList.add('copied');
                setTimeout(() => {
                    btn.textContent = 'Copy';
                    btn.classList.remove('copied');
                }, 2000);
            });
        });
        block.appendChild(btn);
    });

    // Collapsible sections
    document.querySelectorAll('.collapsible-header').forEach(header => {
        header.addEventListener('click', () => {
            const parent = header.parentElement;
            parent.classList.toggle('open');
        });
    });

    // Progress tracking
    initProgress();
});

// Progress System
function initProgress() {
    const checks = document.querySelectorAll('.progress-check');
    if (checks.length === 0) return;

    // Load saved progress
    const saved = JSON.parse(localStorage.getItem('ai-course-progress') || '{}');
    checks.forEach(check => {
        const id = check.getAttribute('data-id');
        if (saved[id]) check.checked = true;
    });

    updateProgressBar();

    // Listen for changes
    checks.forEach(check => {
        check.addEventListener('change', () => {
            const id = check.getAttribute('data-id');
            const progress = JSON.parse(localStorage.getItem('ai-course-progress') || '{}');
            if (check.checked) {
                progress[id] = true;
            } else {
                delete progress[id];
            }
            localStorage.setItem('ai-course-progress', JSON.stringify(progress));
            updateProgressBar();
        });
    });
}

function updateProgressBar() {
    const checks = document.querySelectorAll('.progress-check');
    const total = checks.length;
    const completed = document.querySelectorAll('.progress-check:checked').length;
    const pct = total > 0 ? Math.round((completed / total) * 100) : 0;

    const fill = document.querySelector('.progress-fill');
    const label = document.querySelector('.progress-label');
    if (fill) fill.style.width = pct + '%';
    if (label) label.textContent = `${completed}/${total} completed (${pct}%)`;
}

// Smooth scroll for anchor links
document.addEventListener('click', function(e) {
    const target = e.target.closest('a[href^="#"]');
    if (target) {
        e.preventDefault();
        const id = target.getAttribute('href').slice(1);
        const el = document.getElementById(id);
        if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            history.pushState(null, '', '#' + id);
        }
    }
});
