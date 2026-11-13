/* ============================================
   GEMMA FINE-TUNING GUIDE - SHARED JAVASCRIPT
   ============================================ */

// Theme Toggle
function initTheme() {
    const saved = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    updateThemeIcon(saved);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateThemeIcon(next);
}

function updateThemeIcon(theme) {
    const btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// Code Copy Buttons
function initCopyButtons() {
    document.querySelectorAll('pre').forEach(block => {
        if (block.querySelector('.copy-btn')) return;
        const btn = document.createElement('button');
        btn.className = 'copy-btn';
        btn.textContent = 'Copy';
        btn.addEventListener('click', () => {
            const code = block.querySelector('code')?.textContent || block.textContent;
            navigator.clipboard.writeText(code).then(() => {
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
}

// Collapsible Sections
function initCollapsibles() {
    document.querySelectorAll('.collapsible-header').forEach(header => {
        header.addEventListener('click', () => {
            const parent = header.parentElement;
            parent.classList.toggle('open');
        });
    });
}

// Active Nav Link
function initActiveNav() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.sidebar nav a').forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage) {
            link.classList.add('active');
        }
    });
}

// Mobile Sidebar
function initMobileNav() {
    const hamburger = document.querySelector('.hamburger');
    const sidebar = document.querySelector('.sidebar');
    if (hamburger && sidebar) {
        hamburger.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
        // Close sidebar when clicking outside
        document.addEventListener('click', (e) => {
            if (!sidebar.contains(e.target) && !hamburger.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }
}

// Progress Tracker (index page)
function initProgress() {
    const checkboxes = document.querySelectorAll('.progress-check');
    const saved = JSON.parse(localStorage.getItem('progress') || '{}');
    
    checkboxes.forEach(cb => {
        const id = cb.getAttribute('data-id');
        if (saved[id]) cb.checked = true;
        cb.addEventListener('change', () => {
            const progress = JSON.parse(localStorage.getItem('progress') || '{}');
            progress[id] = cb.checked;
            localStorage.setItem('progress', JSON.stringify(progress));
            updateProgressBar();
        });
    });
    updateProgressBar();
}

function updateProgressBar() {
    const bar = document.querySelector('.progress-fill');
    const label = document.querySelector('.progress-label');
    const checkboxes = document.querySelectorAll('.progress-check');
    if (!bar || !checkboxes.length) return;
    
    const total = checkboxes.length;
    const checked = document.querySelectorAll('.progress-check:checked').length;
    const pct = Math.round((checked / total) * 100);
    bar.style.width = pct + '%';
    if (label) label.textContent = `${checked}/${total} completed (${pct}%)`;
}

// Smooth scroll for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// Initialize all
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initCopyButtons();
    initCollapsibles();
    initActiveNav();
    initMobileNav();
    initProgress();
    initSmoothScroll();
});
