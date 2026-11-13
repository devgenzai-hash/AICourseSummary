// ===== System Design Course - JavaScript =====

document.addEventListener('DOMContentLoaded', function () {
    initTheme();
    initSidebar();
    initActiveNav();
    initCodeCopy();
    initCollapsibles();
    initProgress();
});

// ===== Theme Toggle =====
function initTheme() {
    const toggle = document.querySelector('.theme-toggle');
    const saved = localStorage.getItem('sd-course-theme');

    if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (toggle) toggle.textContent = '☀️';
    }

    if (toggle) {
        toggle.addEventListener('click', function () {
            const current = document.documentElement.getAttribute('data-theme');
            if (current === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('sd-course-theme', 'light');
                toggle.textContent = '🌙';
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('sd-course-theme', 'dark');
                toggle.textContent = '☀️';
            }
        });
    }
}

// ===== Sidebar Toggle (Mobile) =====
function initSidebar() {
    const hamburger = document.querySelector('.hamburger');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');

    if (hamburger && sidebar) {
        hamburger.addEventListener('click', function () {
            sidebar.classList.toggle('open');
            if (overlay) overlay.classList.toggle('active');
        });
    }

    if (overlay) {
        overlay.addEventListener('click', function () {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        });
    }
}

// ===== Active Navigation =====
function initActiveNav() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.sidebar-nav a');

    navLinks.forEach(function (link) {
        const href = link.getAttribute('href');
        if (href === currentPage) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// ===== Code Block Copy Button =====
function initCodeCopy() {
    const codeBlocks = document.querySelectorAll('pre');

    codeBlocks.forEach(function (block) {
        const btn = document.createElement('button');
        btn.className = 'copy-btn';
        btn.textContent = 'Copy';
        btn.addEventListener('click', function () {
            const code = block.querySelector('code');
            const text = code ? code.textContent : block.textContent;
            navigator.clipboard.writeText(text).then(function () {
                btn.textContent = 'Copied!';
                setTimeout(function () {
                    btn.textContent = 'Copy';
                }, 2000);
            });
        });
        block.style.position = 'relative';
        block.appendChild(btn);
    });
}

// ===== Collapsible Sections =====
function initCollapsibles() {
    const headers = document.querySelectorAll('.collapsible-header');

    headers.forEach(function (header) {
        header.addEventListener('click', function () {
            const parent = header.closest('.collapsible');
            parent.classList.toggle('open');
        });
    });
}

// ===== Progress Tracking =====
function initProgress() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const progress = JSON.parse(localStorage.getItem('sd-course-progress') || '{}');

    // Mark current page as visited
    if (currentPage !== 'index.html') {
        progress[currentPage] = true;
        localStorage.setItem('sd-course-progress', JSON.stringify(progress));
    }

    // Update progress bar
    const progressFill = document.querySelector('.progress-bar-fill');
    if (progressFill) {
        const visited = Object.keys(progress).length;
        const total = 68; // 68 topic pages
        const percent = Math.round((visited / total) * 100);
        progressFill.style.width = percent + '%';

        const label = document.querySelector('.progress-label');
        if (label) {
            label.textContent = 'Progress: ' + visited + '/' + total + ' topics completed';
        }
    }
}
