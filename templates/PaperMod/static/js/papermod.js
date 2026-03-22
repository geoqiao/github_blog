// theme toggle and simple TOC builder
(function () {
    const themeBtn = document.querySelector('.theme-toggle');
    const applyTheme = (t) => { document.documentElement.setAttribute('data-theme', t); themeBtn.textContent = t === 'dark' ? '☀️' : '🌙'; localStorage.setItem('theme', t) };
    const saved = localStorage.getItem('theme');
    if (saved) applyTheme(saved); else { const prefers = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches; applyTheme(prefers ? 'dark' : 'light') }
    if (themeBtn) themeBtn.addEventListener('click', () => { const cur = document.documentElement.getAttribute('data-theme') || 'light'; applyTheme(cur === 'dark' ? 'light' : 'dark') });

    // TOC builder + active highlight
    const toc = document.getElementById('toc');
    if (toc) {
        const content = document.querySelector('.post-content');
        if (content) {
            const headings = content.querySelectorAll('h2,h3');
            if (headings.length) {
                const ul = document.createElement('ul');
                ul.className = 'toc-list';
                const tocLinks = [];
                headings.forEach((h, index) => {
                    if (!h.id) {
                        const base = h.textContent.trim().toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-+|-+$/g, '');
                        h.id = base || `section-${index + 1}`;
                    }
                    const li = document.createElement('li');
                    const levelClass = h.tagName === 'H3' ? 'toc-level-2' : 'toc-level-1';
                    li.className = 'toc-item ' + levelClass;
                    const a = document.createElement('a');
                    a.className = 'toc-link';
                    a.href = '#' + h.id;
                    a.textContent = h.textContent;
                    li.appendChild(a);
                    ul.appendChild(li);
                    tocLinks.push({ heading: h, link: a });
                });
                toc.appendChild(ul);

                // Active highlight via IntersectionObserver
                let activeLink = null;
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const match = tocLinks.find(t => t.heading === entry.target);
                            if (match) {
                                if (activeLink) activeLink.classList.remove('toc-active');
                                activeLink = match.link;
                                activeLink.classList.add('toc-active');
                            }
                        }
                    });
                }, { rootMargin: '0px 0px -80% 0px', threshold: 0 });

                headings.forEach(h => observer.observe(h));
            }
        }
    }

    // Reading progress bar
    const progressBar = document.getElementById('reading-progress');
    if (progressBar) {
        const updateProgress = () => {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const pct = docHeight > 0 ? Math.min(100, (scrollTop / docHeight) * 100) : 0;
            progressBar.style.width = pct + '%';
        };
        window.addEventListener('scroll', updateProgress, { passive: true });
        updateProgress();
    }

    // Code block: language label + copy button
    document.querySelectorAll('.post-content pre').forEach(pre => {
        const code = pre.querySelector('code');
        if (!code) return;
        const langClass = Array.from(code.classList).find(c => c.startsWith('language-'));
        const lang = langClass ? langClass.replace('language-', '') : '';

        const header = document.createElement('div');
        header.className = 'code-header';

        if (lang) {
            const langSpan = document.createElement('span');
            langSpan.className = 'code-lang';
            langSpan.textContent = lang;
            header.appendChild(langSpan);
        }

        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.type = 'button';
        copyBtn.textContent = 'Copy';
        copyBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(code.textContent).then(() => {
                copyBtn.textContent = 'Copied!';
                copyBtn.classList.add('copied');
                setTimeout(() => {
                    copyBtn.textContent = 'Copy';
                    copyBtn.classList.remove('copied');
                }, 1500);
            }).catch(() => {
                copyBtn.textContent = 'Failed';
                setTimeout(() => {
                    copyBtn.textContent = 'Copy';
                }, 1500);
            });
        });
        header.appendChild(copyBtn);
        pre.prepend(header);
    });
})();
