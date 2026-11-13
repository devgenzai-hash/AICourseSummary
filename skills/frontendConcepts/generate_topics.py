"""
Generator script for Frontend Concepts course HTML files.
Creates 88 deep-dive topic files following the CS Concept Teacher format.
"""

import os

BASE_DIR = r"c:\Users\aranjan\Documents\Projects\brandWork\skills\frontendConcepts"

# All 88 topics organized by module
MODULES = [
    ("Rendering & Hydration", [
        (1, "hydration", "Hydration"),
        (2, "partial-hydration", "Partial Hydration"),
        (3, "islands-architecture", "Islands Architecture"),
        (4, "streaming-ssr", "Streaming SSR"),
        (5, "concurrent-rendering", "Concurrent Rendering"),
        (6, "time-slicing", "Time Slicing"),
    ]),
    ("React Internals", [
        (7, "reconciliation-algorithm", "Reconciliation Algorithm"),
        (8, "fiber-architecture", "Fiber Architecture"),
        (9, "virtual-dom-diffing", "Virtual DOM Diffing Complexity"),
        (10, "structural-sharing", "Structural Sharing"),
    ]),
    ("Data & State Patterns", [
        (11, "immutable-data-patterns", "Immutable Data Patterns"),
        (12, "referential-equality", "Referential Equality"),
        (13, "memoization-pitfalls", "Memoization Pitfalls"),
        (14, "stale-closure-problem", "Stale Closure Problem"),
    ]),
    ("Event Loop & Scheduling", [
        (15, "event-loop", "Event Loop (Macro vs Microtasks)"),
        (16, "task-starvation", "Task Starvation"),
    ]),
    ("Browser Rendering Pipeline", [
        (17, "layout-thrashing", "Layout Thrashing"),
        (18, "critical-rendering-path", "Critical Rendering Path"),
        (19, "render-blocking-resources", "Render Blocking Resources"),
    ]),
    ("Bundling & Code Delivery", [
        (20, "tree-shaking-internals", "Tree Shaking Internals"),
        (21, "code-splitting-strategies", "Code Splitting Strategies"),
        (22, "dynamic-import-chunking", "Dynamic Import Chunking"),
        (23, "module-federation", "Module Federation"),
    ]),
    ("Web Components", [
        (24, "shadow-dom", "Shadow DOM"),
        (25, "custom-elements-lifecycle", "Custom Elements Lifecycle"),
        (26, "web-components-interop", "Web Components Interoperability"),
    ]),
    ("Workers & Threading", [
        (27, "web-workers-vs-service-workers", "Web Workers vs Service Workers"),
        (28, "sharedarraybuffer", "SharedArrayBuffer"),
        (29, "transferable-objects", "Transferable Objects"),
        (30, "offscreencanvas", "OffscreenCanvas"),
        (31, "webassembly-integration", "WebAssembly Integration"),
    ]),
    ("Compositing & GPU", [
        (32, "browser-compositing-layers", "Browser Compositing Layers"),
        (33, "paint-composite-layout", "Paint vs Composite vs Layout"),
        (34, "gpu-acceleration-css", "GPU Acceleration in CSS"),
        (35, "css-containment", "CSS Containment"),
        (36, "subpixel-rendering", "Subpixel Rendering"),
    ]),
    ("Observer APIs", [
        (37, "intersection-observer", "IntersectionObserver Internals"),
        (38, "resize-observer", "ResizeObserver Loop Limits"),
        (39, "mutation-observer", "MutationObserver Cost"),
    ]),
    ("Storage & Caching", [
        (40, "indexeddb", "IndexedDB"),
        (41, "service-worker-lifecycle", "Service Worker Lifecycle Traps"),
        (42, "cache-invalidation", "Cache Invalidation Strategies"),
        (43, "stale-while-revalidate", "Stale-While-Revalidate"),
        (44, "etag-vs-cache-control", "ETag vs Cache-Control"),
    ]),
    ("Network & Protocols", [
        (45, "http3-quic", "HTTP/3 and QUIC"),
        (46, "priority-hints", "Priority Hints"),
        (47, "preload-prefetch-preconnect", "Preload vs Prefetch vs Preconnect"),
        (48, "cors-preflight", "CORS Preflight"),
    ]),
    ("Security", [
        (49, "samesite-cookies", "SameSite Cookie Modes"),
        (50, "csrf-vs-xss", "CSRF vs XSS Mitigation"),
        (51, "content-security-policy", "Content Security Policy (CSP)"),
        (52, "trusted-types", "Trusted Types"),
        (53, "dom-clobbering", "DOM Clobbering"),
        (54, "prototype-pollution", "Prototype Pollution"),
    ]),
    ("Concurrent UI Patterns", [
        (55, "race-conditions-ui", "Race Conditions in UI State"),
        (56, "tearing-concurrent-ui", "Tearing in Concurrent UI"),
        (57, "scheduler-priorities", "Scheduler Priorities"),
        (58, "render-waterfalls", "Render Waterfalls"),
        (59, "suspense-boundaries", "Suspense Boundaries"),
        (60, "selective-hydration", "Selective Hydration"),
        (61, "server-components", "Server Components"),
        (62, "edge-rendering", "Edge Rendering"),
    ]),
    ("Architecture & State Machines", [
        (63, "micro-frontend-orchestration", "Micro-Frontend Orchestration"),
        (64, "finite-state-modeling", "Finite State Modeling"),
        (65, "event-sourcing-frontend", "Event Sourcing in Frontend"),
        (66, "optimistic-ui-rollback", "Optimistic UI Rollback Strategy"),
    ]),
    ("Offline & Collaboration", [
        (67, "offline-conflict-resolution", "Offline Conflict Resolution"),
        (68, "crdt-basics", "CRDT Basics for Collaboration"),
        (69, "webrtc", "WebRTC"),
    ]),
    ("Streams & Async Patterns", [
        (70, "backpressure-streams", "Backpressure in Streams API"),
        (71, "abort-controller", "AbortController"),
        (72, "streaming-fetch", "Streaming Fetch Response Handling"),
    ]),
    ("Memory & GC", [
        (73, "memory-leak-detection", "Browser Memory Leak Detection"),
        (74, "detached-dom-nodes", "Detached DOM Nodes"),
        (75, "garbage-collection-timing", "Garbage Collection Timing"),
    ]),
    ("Performance APIs & Metrics", [
        (76, "performance-observer", "PerformanceObserver API"),
        (77, "long-tasks-api", "Long Tasks API"),
        (78, "first-input-delay", "First Input Delay (FID)"),
        (79, "interaction-next-paint", "Interaction to Next Paint (INP)"),
        (80, "cumulative-layout-shift", "Cumulative Layout Shift (CLS)"),
        (81, "largest-contentful-paint", "Largest Contentful Paint (LCP)"),
    ]),
    ("Advanced Patterns", [
        (82, "speculative-prerendering", "Speculative Prerendering"),
        (83, "priority-inversion-async", "Priority Inversion in Async Code"),
        (84, "deterministic-rendering", "Deterministic Rendering"),
        (85, "idempotent-ui-actions", "Idempotent UI Actions"),
    ]),
    ("Accessibility Internals", [
        (86, "accessibility-tree", "Accessibility Tree"),
        (87, "aria-live-regions", "ARIA Live Regions Internals"),
        (88, "pointer-events", "Pointer Events"),
    ]),
]

def get_all_topics():
    topics = []
    for module_name, module_topics in MODULES:
        for num, slug, title in module_topics:
            topics.append((num, slug, title, module_name))
    return topics

def get_sidebar_html():
    lines = []
    lines.append('    <aside class="sidebar">')
    lines.append('        <div class="sidebar-header">')
    lines.append('            <h2>Frontend Concepts</h2>')
    lines.append('            <div class="subtitle">Deep Dives &bull; 88 Topics</div>')
    lines.append('        </div>')
    lines.append('        <ul class="sidebar-nav">')
    lines.append('            <li><a href="index.html"><span class="nav-number">🏠</span> Course Overview</a></li>')
    
    for module_name, module_topics in MODULES:
        lines.append(f'            <li class="module-label">{module_name}</li>')
        for num, slug, title in module_topics:
            short_title = title if len(title) <= 30 else title[:28] + '…'
            lines.append(f'            <li><a href="{num:02d}-{slug}.html"><span class="nav-number">{num}</span> {short_title}</a></li>')
    
    lines.append('        </ul>')
    lines.append('        <div class="progress-tracker">')
    lines.append('            <div class="progress-label">Progress: 0/88 topics completed</div>')
    lines.append('            <div class="progress-bar"><div class="progress-bar-fill" style="width: 0%"></div></div>')
    lines.append('        </div>')
    lines.append('    </aside>')
    return '\n'.join(lines)

SIDEBAR = get_sidebar_html()

# ===== TOPIC CONTENT =====
# Each topic gets a full deep-dive explanation

TOPIC_CONTENT = {}

TOPIC_CONTENT[1] = {
    "title": "Hydration",
    "subtitle": "How server-rendered HTML becomes an interactive application in the browser — the bridge between static markup and dynamic behavior.",
    "tags": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-browser">Browser</span>'],
    "content": """
            <div class="analogy-box">
                <div class="analogy-title">🌊 Daily-Life Analogy: Inflating a Bounce House</div>
                <p>Imagine you receive a <strong>deflated bounce house</strong> (server HTML). It looks like a bounce house — you can see its shape and colors — but you can't interact with it. <strong>Hydration</strong> is the process of pumping air into it (attaching event listeners, initializing state), transforming the static structure into something interactive.</p>
                <p>The key insight: the <strong>structure already exists</strong>. You don't rebuild the bounce house from scratch — you just make the existing one functional.</p>
            </div>

            <h2>The Problem: Why Hydration Exists</h2>
            <p>Modern web apps face a fundamental tension:</p>
            <ul>
                <li><strong>Server-Side Rendering (SSR)</strong> gives fast first paint and SEO — the user sees content quickly</li>
                <li><strong>Client-Side Rendering (CSR)</strong> gives rich interactivity — buttons work, forms validate, state updates</li>
            </ul>
            <p>Hydration solves this by doing <em>both</em>: render HTML on the server for speed, then "hydrate" it on the client for interactivity. Without hydration, you'd either have a slow initial load (pure CSR) or a non-interactive page (pure SSR).</p>

            <h2>How Hydration Works Internally</h2>
            <h3>Step-by-Step Process</h3>
            <ol>
                <li><strong>Server renders HTML</strong> — Components execute on the server, producing a complete HTML string</li>
                <li><strong>HTML is sent to browser</strong> — User sees content immediately (First Contentful Paint)</li>
                <li><strong>JavaScript bundle downloads</strong> — The framework code + component code arrives</li>
                <li><strong>Framework "walks" the DOM</strong> — It traverses the existing DOM tree, matching it to the component tree</li>
                <li><strong>Event listeners are attached</strong> — Click handlers, change handlers, etc. get wired up</li>
                <li><strong>State is initialized</strong> — Component state is set up (often from serialized server state)</li>
                <li><strong>App is interactive</strong> — Time to Interactive (TTI) is reached</li>
            </ol>

            <div class="callout callout-warning">
                <div class="callout-title">⚠️ The Hydration Mismatch Problem</div>
                <p>If the server-rendered HTML doesn't match what the client would render, you get a <strong>hydration mismatch</strong>. React will throw warnings and may discard the server HTML entirely, defeating the purpose of SSR. Common causes: <code>Date.now()</code>, <code>Math.random()</code>, browser-only APIs like <code>window.innerWidth</code>.</p>
            </div>

            <h2>Code: React Hydration</h2>
<pre><code><span class="token-comment">// server.js — Server renders the initial HTML</span>
<span class="token-keyword">import</span> { renderToString } <span class="token-keyword">from</span> <span class="token-string">'react-dom/server'</span>;
<span class="token-keyword">import</span> App <span class="token-keyword">from</span> <span class="token-string">'./App'</span>;

<span class="token-keyword">function</span> <span class="token-function">handleRequest</span>(req, res) {
    <span class="token-comment">// Execute components on server — produces HTML string</span>
    <span class="token-keyword">const</span> html = renderToString(&lt;App initialData={data} /&gt;);
    
    <span class="token-comment">// Send complete HTML — user sees content before JS loads</span>
    res.send(<span class="token-string">`
        &lt;!DOCTYPE html&gt;
        &lt;html&gt;
        &lt;body&gt;
            &lt;div id="root"&gt;\${html}&lt;/div&gt;
            &lt;script&gt;
                // Serialize state so client can pick up where server left off
                window.__INITIAL_STATE__ = \${JSON.stringify(data)};
            &lt;/script&gt;
            &lt;script src="/bundle.js"&gt;&lt;/script&gt;
        &lt;/body&gt;
        &lt;/html&gt;
    `</span>);
}
</code></pre>

<pre><code><span class="token-comment">// client.js — Client hydrates the existing HTML</span>
<span class="token-keyword">import</span> { hydrateRoot } <span class="token-keyword">from</span> <span class="token-string">'react-dom/client'</span>;
<span class="token-keyword">import</span> App <span class="token-keyword">from</span> <span class="token-string">'./App'</span>;

<span class="token-comment">// hydrateRoot does NOT rebuild the DOM — it attaches to existing HTML</span>
<span class="token-comment">// React walks the existing DOM tree and wires up event handlers</span>
<span class="token-keyword">const</span> root = hydrateRoot(
    document.getElementById(<span class="token-string">'root'</span>),
    &lt;App initialData={window.__INITIAL_STATE__} /&gt;
);

<span class="token-comment">// Key difference from createRoot:</span>
<span class="token-comment">// createRoot: builds DOM from scratch (discards existing HTML)</span>
<span class="token-comment">// hydrateRoot: reuses existing DOM, only adds interactivity</span>
</code></pre>

            <h2>The Performance Cost of Hydration</h2>
            <p>Full hydration has a dirty secret: <strong>it's expensive</strong>. The framework must:</p>
            <ul>
                <li>Download ALL component JavaScript (even for static content)</li>
                <li>Execute ALL components on the client (to build the virtual tree)</li>
                <li>Walk the entire DOM tree to reconcile</li>
                <li>Attach event listeners to every interactive element</li>
            </ul>
            <p>This means <strong>Time to Interactive (TTI) can be much later than First Contentful Paint (FCP)</strong>. The user sees content but can't interact — the "uncanny valley" of web apps.</p>

            <table class="comparison-table">
                <thead>
                    <tr><th>Metric</th><th>No Hydration (CSR)</th><th>Full Hydration (SSR+CSR)</th></tr>
                </thead>
                <tbody>
                    <tr><td>First Contentful Paint</td><td>Slow (wait for JS)</td><td>Fast (server HTML)</td></tr>
                    <tr><td>Time to Interactive</td><td>Same as FCP</td><td>Delayed (hydration cost)</td></tr>
                    <tr><td>Bundle Size Impact</td><td>Full bundle needed</td><td>Full bundle STILL needed</td></tr>
                    <tr><td>Main Thread Work</td><td>Render once</td><td>Render twice (server + client)</td></tr>
                </tbody>
            </table>

            <h2>Where This Is Used in Production</h2>
            <ul>
                <li><strong>Next.js</strong> — Uses React's hydrateRoot for all SSR pages. Their App Router leverages streaming + selective hydration for better performance.</li>
                <li><strong>Gatsby</strong> — Static HTML at build time, hydrated on load. Every page is pre-rendered then made interactive.</li>
                <li><strong>Nuxt.js (Vue)</strong> — Same pattern with Vue's createSSRApp and hydration phase.</li>
            </ul>

            <h2>Common Mistakes</h2>
            <ul>
                <li><strong>Using browser APIs during render</strong> — <code>window</code>, <code>document</code>, <code>localStorage</code> don't exist on server. Guard with <code>typeof window !== 'undefined'</code></li>
                <li><strong>Non-deterministic rendering</strong> — <code>Date.now()</code> produces different values on server vs client, causing mismatches</li>
                <li><strong>CSS-in-JS without server extraction</strong> — Styles must be extracted during SSR or you get a flash of unstyled content</li>
                <li><strong>Assuming instant interactivity</strong> — Users click buttons that aren't hydrated yet. Use loading states or progressive enhancement.</li>
            </ul>

            <div class="understanding-section">
                <h3>✅ You Truly Understand Hydration When...</h3>
                <p>You can explain why a user clicking a button 500ms after page load might get no response, and how to design around that gap.</p>
                <h3>🧪 Try This Challenge</h3>
                <p>Build a page that renders a timestamp on the server. Fix the hydration mismatch without removing the timestamp. (Hint: <code>suppressHydrationWarning</code> or useEffect for client-only values.)</p>
                <h3>🔗 Connect It</h3>
                <p>Hydration connects to: <strong>Partial Hydration</strong> (hydrating only interactive parts), <strong>Streaming SSR</strong> (sending HTML in chunks), and <strong>Selective Hydration</strong> (prioritizing user-interacted components).</p>
            </div>
"""
}

TOPIC_CONTENT[2] = {
    "title": "Partial Hydration",
    "subtitle": "The optimization that says: don't hydrate what doesn't need to be interactive. Only send JavaScript for components that actually have event handlers.",
    "tags": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-performance">Performance</span>'],
    "content": """
            <div class="analogy-box">
                <div class="analogy-title">🏗️ Analogy: Wiring a House</div>
                <p>Full hydration is like running electrical wires to <em>every single wall</em> in a house — even walls that will never have an outlet. Partial hydration is like an electrician who only wires the walls where you actually want outlets and switches. The other walls remain perfectly fine as-is — they just don't need electricity.</p>
            </div>

            <h2>The Problem: Full Hydration is Wasteful</h2>
            <p>Consider a typical blog post page: 90% is static text, images, and layout. Only 10% is interactive (comment form, like button, share menu). With full hydration, you download and execute JavaScript for the <em>entire</em> page — including all that static content that will never change.</p>
            <p>Partial hydration recognizes that <strong>most server-rendered content doesn't need client-side JavaScript</strong>. It only sends JS for the "interactive islands" on the page.</p>

            <h2>How Partial Hydration Works</h2>
            <ol>
                <li><strong>Server renders full HTML</strong> — The complete page is generated server-side</li>
                <li><strong>Compiler/framework identifies interactive components</strong> — Either via directives or static analysis</li>
                <li><strong>Only interactive component JS is sent</strong> — Static components get zero client JavaScript</li>
                <li><strong>Hydration runs ONLY on interactive components</strong> — The rest of the DOM is left alone</li>
            </ol>

            <h2>Code: Astro's Partial Hydration</h2>
<pre><code><span class="token-comment">&lt;!-- Astro uses "client directives" to mark what gets hydrated --&gt;</span>
<span class="token-comment">&lt;!-- This component sends ZERO JavaScript to the browser --&gt;</span>
<span class="token-tag">&lt;StaticHeader</span> <span class="token-attr">title</span>=<span class="token-string">"My Blog Post"</span> <span class="token-tag">/&gt;</span>

<span class="token-comment">&lt;!-- This component gets hydrated immediately on page load --&gt;</span>
<span class="token-tag">&lt;SearchBar</span> <span class="token-attr">client:load</span> <span class="token-tag">/&gt;</span>

<span class="token-comment">&lt;!-- This one hydrates only when it scrolls into the viewport --&gt;</span>
<span class="token-tag">&lt;CommentSection</span> <span class="token-attr">client:visible</span> <span class="token-tag">/&gt;</span>

<span class="token-comment">&lt;!-- This hydrates only when the browser is idle (requestIdleCallback) --&gt;</span>
<span class="token-tag">&lt;RecommendedPosts</span> <span class="token-attr">client:idle</span> <span class="token-tag">/&gt;</span>

<span class="token-comment">&lt;!-- This NEVER hydrates unless explicitly triggered by JS --&gt;</span>
<span class="token-tag">&lt;HeavyChart</span> <span class="token-attr">client:only="react"</span> <span class="token-tag">/&gt;</span>

<span class="token-comment">&lt;!-- 
  Result: Instead of shipping 200KB of JS for the full page,
  you might ship only 15KB for just the interactive components.
  The blog post text, navigation, footer — all zero-JS static HTML.
--&gt;</span>
</code></pre>

            <h2>Implementation Pattern: Manual Partial Hydration</h2>
<pre><code><span class="token-comment">// A simplified partial hydration loader</span>
<span class="token-comment">// Only hydrates elements marked with data-hydrate attribute</span>

<span class="token-keyword">async function</span> <span class="token-function">partialHydrate</span>() {
    <span class="token-comment">// Find all elements that need hydration</span>
    <span class="token-keyword">const</span> islands = document.querySelectorAll(<span class="token-string">'[data-hydrate]'</span>);
    
    <span class="token-keyword">for</span> (<span class="token-keyword">const</span> island <span class="token-keyword">of</span> islands) {
        <span class="token-keyword">const</span> componentName = island.dataset.hydrate;
        <span class="token-keyword">const</span> strategy = island.dataset.strategy || <span class="token-string">'load'</span>;
        
        <span class="token-keyword">switch</span> (strategy) {
            <span class="token-keyword">case</span> <span class="token-string">'load'</span>:
                <span class="token-comment">// Hydrate immediately</span>
                <span class="token-keyword">await</span> hydrateComponent(island, componentName);
                <span class="token-keyword">break</span>;
                
            <span class="token-keyword">case</span> <span class="token-string">'visible'</span>:
                <span class="token-comment">// Hydrate when element enters viewport</span>
                <span class="token-keyword">const</span> observer = <span class="token-keyword">new</span> IntersectionObserver(
                    <span class="token-keyword">async</span> ([entry]) => {
                        <span class="token-keyword">if</span> (entry.isIntersecting) {
                            observer.disconnect();
                            <span class="token-keyword">await</span> hydrateComponent(island, componentName);
                        }
                    }
                );
                observer.observe(island);
                <span class="token-keyword">break</span>;
                
            <span class="token-keyword">case</span> <span class="token-string">'idle'</span>:
                <span class="token-comment">// Hydrate when browser is idle</span>
                requestIdleCallback(<span class="token-keyword">async</span> () => {
                    <span class="token-keyword">await</span> hydrateComponent(island, componentName);
                });
                <span class="token-keyword">break</span>;
        }
    }
}

<span class="token-keyword">async function</span> <span class="token-function">hydrateComponent</span>(element, name) {
    <span class="token-comment">// Dynamic import — only loads JS for this specific component</span>
    <span class="token-keyword">const</span> { default: Component } = <span class="token-keyword">await</span> import(<span class="token-string">`./components/\${name}.js`</span>);
    
    <span class="token-comment">// Get serialized props from the HTML</span>
    <span class="token-keyword">const</span> props = JSON.parse(element.dataset.props || <span class="token-string">'{}'</span>);
    
    <span class="token-comment">// Hydrate only this island — rest of page untouched</span>
    hydrateRoot(element, &lt;Component {...props} /&gt;);
}

partialHydrate();
</code></pre>

            <h2>Real-World Usage</h2>
            <ul>
                <li><strong>Astro</strong> — The pioneer of partial hydration in modern frameworks. Uses "client directives" (client:load, client:visible, client:idle, client:media) to control when/if components hydrate.</li>
                <li><strong>Eleventy + Islands</strong> — Static site generator with opt-in island hydration via <code>is-land</code> web component.</li>
                <li><strong>Marko (eBay)</strong> — Automatically detects which components are interactive and only sends JS for those.</li>
            </ul>

            <h2>Trade-offs</h2>
            <table class="comparison-table">
                <thead><tr><th>Aspect</th><th>Full Hydration</th><th>Partial Hydration</th></tr></thead>
                <tbody>
                    <tr><td>JS Bundle Size</td><td>All components shipped</td><td>Only interactive components</td></tr>
                    <tr><td>Time to Interactive</td><td>Slower (hydrate everything)</td><td>Faster (less work)</td></tr>
                    <tr><td>Complexity</td><td>Simple (everything hydrates)</td><td>Requires explicit marking</td></tr>
                    <tr><td>State Sharing</td><td>Easy (single React tree)</td><td>Hard (isolated islands)</td></tr>
                    <tr><td>Framework Support</td><td>All frameworks</td><td>Astro, Marko, Fresh</td></tr>
                </tbody>
            </table>

            <div class="understanding-section">
                <h3>✅ You Truly Understand Partial Hydration When...</h3>
                <p>You can look at a page design and identify which components are "islands" that need JS vs pure static content, and explain why sharing state between islands is architecturally challenging.</p>
                <h3>🧪 Try This Challenge</h3>
                <p>Take a typical e-commerce product page and list every component. Mark each as "static" or "interactive island." Calculate what percentage of JS you'd save with partial hydration.</p>
                <h3>🔗 Connect It</h3>
                <p>Connects to: <strong>Islands Architecture</strong> (the pattern that partial hydration enables), <strong>Code Splitting</strong> (each island is its own chunk), <strong>Selective Hydration</strong> (React's approach to prioritizing hydration).</p>
            </div>
"""
}

TOPIC_CONTENT[3] = {
    "title": "Islands Architecture",
    "subtitle": "A web architecture where pages are mostly static HTML with isolated 'islands' of interactivity — each independently hydrated and potentially using different frameworks.",
    "tags": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-performance">Performance</span>'],
    "content": """
            <div class="analogy-box">
                <div class="analogy-title">🏝️ Analogy: Islands in an Ocean</div>
                <p>Picture a vast ocean of <strong>static HTML</strong> (the page). Scattered across it are small <strong>islands</strong> — each island is a self-contained interactive component. The islands don't connect to each other underwater. Each has its own ecosystem (framework, state, lifecycle). The ocean itself requires zero JavaScript.</p>
            </div>

            <h2>The Problem: SPA Overhead for Content Sites</h2>
            <p>Single Page Applications treat the entire page as one JavaScript application. For a marketing site or blog, this means:</p>
            <ul>
                <li>A navigation bar that barely changes requires a full React runtime</li>
                <li>A static footer ships with event handlers it never uses</li>
                <li>The "contact us" form forces the entire page to be a JS app</li>
            </ul>
            <p>Islands architecture flips this: the page is <strong>HTML-first</strong>, with JavaScript only injected where interactivity is required.</p>

            <h2>How Islands Architecture Works</h2>
<pre><code><span class="token-comment">&lt;!-- The page is plain HTML — rendered at build time or on server --&gt;</span>
<span class="token-tag">&lt;html&gt;</span>
<span class="token-tag">&lt;body&gt;</span>
    <span class="token-comment">&lt;!-- Static: Zero JavaScript --&gt;</span>
    <span class="token-tag">&lt;header&gt;</span>
        <span class="token-tag">&lt;nav&gt;</span>...<span class="token-tag">&lt;/nav&gt;</span>
    <span class="token-tag">&lt;/header&gt;</span>
    
    <span class="token-comment">&lt;!-- Static article content: Zero JavaScript --&gt;</span>
    <span class="token-tag">&lt;article&gt;</span>
        <span class="token-tag">&lt;h1&gt;</span>Understanding Islands<span class="token-tag">&lt;/h1&gt;</span>
        <span class="token-tag">&lt;p&gt;</span>Lots of static text...<span class="token-tag">&lt;/p&gt;</span>
    <span class="token-tag">&lt;/article&gt;</span>
    
    <span class="token-comment">&lt;!-- 🏝️ ISLAND: Interactive search widget (React) --&gt;</span>
    <span class="token-tag">&lt;div</span> <span class="token-attr">data-island</span>=<span class="token-string">"search"</span> <span class="token-attr">data-framework</span>=<span class="token-string">"react"</span><span class="token-tag">&gt;</span>
        <span class="token-comment">&lt;!-- Server-rendered placeholder --&gt;</span>
        <span class="token-tag">&lt;input</span> <span class="token-attr">placeholder</span>=<span class="token-string">"Search..."</span> <span class="token-tag">/&gt;</span>
    <span class="token-tag">&lt;/div&gt;</span>
    
    <span class="token-comment">&lt;!-- More static content: Zero JavaScript --&gt;</span>
    <span class="token-tag">&lt;section&gt;</span>...<span class="token-tag">&lt;/section&gt;</span>
    
    <span class="token-comment">&lt;!-- 🏝️ ISLAND: Interactive carousel (Svelte) --&gt;</span>
    <span class="token-tag">&lt;div</span> <span class="token-attr">data-island</span>=<span class="token-string">"carousel"</span> <span class="token-attr">data-framework</span>=<span class="token-string">"svelte"</span><span class="token-tag">&gt;</span>
        <span class="token-comment">&lt;!-- Server-rendered images --&gt;</span>
    <span class="token-tag">&lt;/div&gt;</span>
    
    <span class="token-comment">&lt;!-- Static footer: Zero JavaScript --&gt;</span>
    <span class="token-tag">&lt;footer&gt;</span>...<span class="token-tag">&lt;/footer&gt;</span>
<span class="token-tag">&lt;/body&gt;</span>
<span class="token-tag">&lt;/html&gt;</span>
</code></pre>

            <h2>Real-World Implementations</h2>
            <ul>
                <li><strong>Astro</strong> — The most popular islands framework. Supports React, Vue, Svelte, Solid islands on the same page.</li>
                <li><strong>Fresh (Deno)</strong> — Deno's web framework uses islands architecture by default. Components in an <code>islands/</code> directory get JS; everything else is static.</li>
                <li><strong>Marko (eBay)</strong> — Automatically determines island boundaries through static analysis of component interactivity.</li>
            </ul>

            <h2>Trade-offs</h2>
            <ul>
                <li><strong>Pro:</strong> Dramatically less JavaScript shipped — often 90%+ reduction for content sites</li>
                <li><strong>Pro:</strong> Each island can use a different framework (mix React + Svelte)</li>
                <li><strong>Pro:</strong> Islands fail independently — one broken island doesn't crash the page</li>
                <li><strong>Con:</strong> Sharing state between islands is difficult (no shared React context)</li>
                <li><strong>Con:</strong> Not suitable for highly interactive apps (dashboards, editors)</li>
                <li><strong>Con:</strong> Developer experience can be confusing with mixed frameworks</li>
            </ul>

            <div class="understanding-section">
                <h3>✅ You Truly Understand Islands Architecture When...</h3>
                <p>You can identify which pages benefit from islands (content-heavy, few interactive spots) vs which need a full SPA (highly interactive, deeply connected state).</p>
                <h3>🧪 Try This Challenge</h3>
                <p>Redesign a news website's architecture using islands. Identify each island, its hydration strategy (load, visible, idle), and estimate total JS savings vs a Next.js SPA.</p>
                <h3>🔗 Connect It</h3>
                <p>Connects to: <strong>Partial Hydration</strong> (the mechanism islands use), <strong>Micro-Frontends</strong> (similar composition model), <strong>Web Components</strong> (another way to create isolated interactive elements).</p>
            </div>
"""
}

TOPIC_CONTENT[4] = {
    "title": "Streaming SSR",
    "subtitle": "Sending HTML to the browser in chunks as it's generated rather than waiting for the entire page to be ready — dramatically reducing Time to First Byte.",
    "tags": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-performance">Performance</span>'],
    "content": """
            <div class="analogy-box">
                <div class="analogy-title">📺 Analogy: Streaming Video vs Downloading</div>
                <p>Traditional SSR is like <strong>downloading an entire movie</strong> before you can watch it. Streaming SSR is like <strong>Netflix</strong> — you start watching immediately while the rest buffers in the background. The header and navigation appear instantly; slower parts (database queries for the main content) arrive as they're ready.</p>
            </div>

            <h2>The Problem: Blocking SSR</h2>
            <p>Traditional SSR has a serial bottleneck:</p>
            <ol>
                <li>Server receives request</li>
                <li>Server fetches ALL data (database calls, API requests) — <strong>blocks here</strong></li>
                <li>Server renders ALL components to HTML — <strong>blocks here</strong></li>
                <li>Server sends complete HTML response</li>
                <li>Browser receives and displays</li>
            </ol>
            <p>If one slow API call takes 2 seconds, the <em>entire page</em> is delayed by 2 seconds — even the parts that were ready instantly.</p>

            <h2>How Streaming SSR Works</h2>
<pre><code><span class="token-comment">// React 18 Streaming SSR with renderToPipeableStream</span>
<span class="token-keyword">import</span> { renderToPipeableStream } <span class="token-keyword">from</span> <span class="token-string">'react-dom/server'</span>;

<span class="token-keyword">function</span> <span class="token-function">handleRequest</span>(req, res) {
    <span class="token-keyword">const</span> { pipe } = renderToPipeableStream(
        <span class="token-tag">&lt;App /&gt;</span>,
        {
            <span class="token-comment">// Called when the shell (non-suspended content) is ready</span>
            onShellReady() {
                res.setHeader(<span class="token-string">'Content-Type'</span>, <span class="token-string">'text/html'</span>);
                res.setHeader(<span class="token-string">'Transfer-Encoding'</span>, <span class="token-string">'chunked'</span>);
                <span class="token-comment">// Start streaming immediately — don't wait for everything</span>
                pipe(res);
            },
            onShellError(err) {
                <span class="token-comment">// If the shell fails, fall back to client rendering</span>
                res.status(<span class="token-number">500</span>).send(<span class="token-string">'&lt;script&gt;location.href="/client-only"&lt;/script&gt;'</span>);
            },
            onError(err) {
                console.error(err);
            }
        }
    );
}
</code></pre>

<pre><code><span class="token-comment">// The App component uses Suspense boundaries to define streaming chunks</span>
<span class="token-keyword">function</span> <span class="token-function">App</span>() {
    <span class="token-keyword">return</span> (
        <span class="token-tag">&lt;&gt;</span>
            <span class="token-comment">{/* This renders immediately — part of the "shell" */}</span>
            <span class="token-tag">&lt;Header /&gt;</span>
            <span class="token-tag">&lt;Navigation /&gt;</span>
            
            <span class="token-comment">{/* This streams in when the data fetch completes */}</span>
            <span class="token-tag">&lt;Suspense</span> <span class="token-attr">fallback</span>=<span class="token-string">{&lt;ArticleSkeleton /&gt;}</span><span class="token-tag">&gt;</span>
                <span class="token-tag">&lt;ArticleContent /&gt;</span>  <span class="token-comment">{/* Fetches from database */}</span>
            <span class="token-tag">&lt;/Suspense&gt;</span>
            
            <span class="token-comment">{/* This streams independently — doesn't block article */}</span>
            <span class="token-tag">&lt;Suspense</span> <span class="token-attr">fallback</span>=<span class="token-string">{&lt;CommentsSkeleton /&gt;}</span><span class="token-tag">&gt;</span>
                <span class="token-tag">&lt;Comments /&gt;</span>  <span class="token-comment">{/* Fetches from API */}</span>
            <span class="token-tag">&lt;/Suspense&gt;</span>
            
            <span class="token-tag">&lt;Footer /&gt;</span>
        <span class="token-tag">&lt;/&gt;</span>
    );
}
</code></pre>

            <div class="callout callout-info">
                <div class="callout-title">💡 How Streaming Sends Late Content</div>
                <p>When a Suspense boundary resolves, React doesn't re-send the HTML. Instead, it sends a small <code>&lt;script&gt;</code> tag at the bottom of the stream that calls a function to swap the fallback with the real content. The browser executes this inline script and replaces the skeleton. This is called <strong>out-of-order streaming</strong>.</p>
            </div>

            <h2>Real-World Usage</h2>
            <ul>
                <li><strong>Next.js App Router</strong> — Uses React 18 streaming by default. Every <code>loading.js</code> file creates a Suspense boundary that streams.</li>
                <li><strong>Remix</strong> — Uses <code>defer()</code> to stream non-critical data while sending the shell immediately.</li>
                <li><strong>Shopify Hydrogen</strong> — Streams product pages; the product info loads fast while reviews stream later.</li>
            </ul>

            <h2>Trade-offs</h2>
            <ul>
                <li><strong>Pro:</strong> TTFB is dramatically faster — user sees shell immediately</li>
                <li><strong>Pro:</strong> Slow data sources don't block fast ones</li>
                <li><strong>Pro:</strong> Better perceived performance (progressive loading)</li>
                <li><strong>Con:</strong> Can't set HTTP headers after streaming starts (status code, redirects)</li>
                <li><strong>Con:</strong> Error handling is more complex (can't show 500 page if data fails mid-stream)</li>
                <li><strong>Con:</strong> CDN caching is harder with chunked responses</li>
            </ul>

            <div class="understanding-section">
                <h3>✅ You Truly Understand Streaming SSR When...</h3>
                <p>You can explain why you can't do a redirect after the stream starts, and how Suspense boundaries define the granularity of what streams independently.</p>
                <h3>🧪 Try This Challenge</h3>
                <p>Design the Suspense boundary layout for a social media feed page. Which parts are in the shell? Which parts stream? What happens if the user's profile fetch fails after the shell is sent?</p>
                <h3>🔗 Connect It</h3>
                <p>Connects to: <strong>Suspense Boundaries</strong> (the mechanism that enables streaming), <strong>Selective Hydration</strong> (hydrating streamed content by priority), <strong>Render Waterfalls</strong> (streaming eliminates sequential data fetching).</p>
            </div>
"""
}

TOPIC_CONTENT[5] = {
    "title": "Concurrent Rendering",
    "subtitle": "React's ability to work on multiple UI updates simultaneously, pausing and resuming rendering work without blocking the main thread.",
    "tags": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-performance">Performance</span>'],
    "content": """
            <div class="analogy-box">
                <div class="analogy-title">🍳 Analogy: Cooking Multiple Dishes</div>
                <p>Synchronous rendering is like a chef who <strong>must finish one dish completely before starting another</strong> — even if a customer is waiting for just a glass of water. Concurrent rendering is like a chef who can <strong>pause chopping vegetables to quickly serve that water</strong>, then resume chopping. Work is interruptible and prioritized by urgency.</p>
            </div>

            <h2>The Problem: Blocking Renders</h2>
            <p>In synchronous React (pre-18), once a render starts, it runs to completion. If a render takes 100ms (large list, complex tree), the main thread is blocked for 100ms. During that time:</p>
            <ul>
                <li>User input is ignored (typing feels laggy)</li>
                <li>Animations freeze</li>
                <li>The page appears unresponsive</li>
            </ul>
            <p>Concurrent rendering makes renders <strong>interruptible</strong>. React can pause work on a low-priority update to handle a high-priority one (like user input), then resume the paused work later.</p>

            <h2>How It Works: Interruptible Rendering</h2>
<pre><code><span class="token-comment">// Without concurrent rendering — this blocks for 100ms</span>
<span class="token-keyword">function</span> <span class="token-function">SearchResults</span>({ query }) {
    <span class="token-comment">// Filtering 10,000 items blocks the main thread</span>
    <span class="token-keyword">const</span> results = items.filter(item => item.name.includes(query));
    <span class="token-keyword">return</span> results.map(item => <span class="token-tag">&lt;ResultCard</span> <span class="token-attr">key</span>={item.id} <span class="token-attr">item</span>={item} <span class="token-tag">/&gt;</span>);
}

<span class="token-comment">// With concurrent rendering — useTransition marks as low priority</span>
<span class="token-keyword">function</span> <span class="token-function">SearchPage</span>() {
    <span class="token-keyword">const</span> [query, setQuery] = useState(<span class="token-string">''</span>);
    <span class="token-keyword">const</span> [deferredQuery, setDeferredQuery] = useState(<span class="token-string">''</span>);
    <span class="token-keyword">const</span> [isPending, startTransition] = useTransition();
    
    <span class="token-keyword">function</span> <span class="token-function">handleChange</span>(e) {
        <span class="token-comment">// HIGH priority: update input value immediately</span>
        setQuery(e.target.value);
        
        <span class="token-comment">// LOW priority: update search results (can be interrupted)</span>
        startTransition(() => {
            setDeferredQuery(e.target.value);
        });
    }
    
    <span class="token-keyword">return</span> (
        <span class="token-tag">&lt;&gt;</span>
            <span class="token-tag">&lt;input</span> <span class="token-attr">value</span>={query} <span class="token-attr">onChange</span>={handleChange} <span class="token-tag">/&gt;</span>
            {isPending && <span class="token-tag">&lt;Spinner /&gt;</span>}
            <span class="token-comment">{/* This re-render can be paused if user types again */}</span>
            <span class="token-tag">&lt;SearchResults</span> <span class="token-attr">query</span>={deferredQuery} <span class="token-tag">/&gt;</span>
        <span class="token-tag">&lt;/&gt;</span>
    );
}
</code></pre>

            <div class="callout callout-info">
                <div class="callout-title">💡 Key Mechanism: Time Slicing</div>
                <p>Concurrent rendering uses <strong>time slicing</strong> — React works on rendering for ~5ms, then yields to the browser's event loop. If user input arrives during a yield point, React can abandon the in-progress render and start a new one for the high-priority update. The Fiber architecture makes this possible by tracking work in a linked-list structure that can be paused/resumed.</p>
            </div>

            <h2>Real-World Usage</h2>
            <ul>
                <li><strong>React 18+</strong> — All React 18 apps opt into concurrent rendering via <code>createRoot</code> (vs legacy <code>ReactDOM.render</code>)</li>
                <li><strong>Facebook Feed</strong> — The infinite scrolling feed uses transitions so new posts rendering doesn't block scrolling</li>
                <li><strong>VS Code Web</strong> — Large file tree renders use concurrent-like patterns to keep the editor responsive</li>
            </ul>

            <h2>Common Mistakes</h2>
            <ul>
                <li><strong>Expecting renders to always complete</strong> — A transition render may be abandoned if a higher-priority update arrives. Don't put side effects in render.</li>
                <li><strong>Using useTransition for everything</strong> — Only use it when you have low-priority updates that might block high-priority ones.</li>
                <li><strong>Not understanding tearing</strong> — In concurrent mode, two parts of the UI might show different versions of state momentarily. Use <code>useSyncExternalStore</code> for external stores.</li>
            </ul>

            <div class="understanding-section">
                <h3>✅ You Truly Understand Concurrent Rendering When...</h3>
                <p>You can explain what "interruptible" means at the Fiber level — how React tracks partially-completed work and can throw it away or resume it.</p>
                <h3>🧪 Try This Challenge</h3>
                <p>Build a typeahead search that filters 10,000 items. Without useTransition, notice how typing lags. Add useTransition and demonstrate the input stays responsive while results update in the background.</p>
                <h3>🔗 Connect It</h3>
                <p>Connects to: <strong>Fiber Architecture</strong> (the data structure enabling interruption), <strong>Time Slicing</strong> (the mechanism for yielding), <strong>Tearing</strong> (the consistency problem concurrent rendering introduces).</p>
            </div>
"""
}

TOPIC_CONTENT[6] = {
    "title": "Time Slicing",
    "subtitle": "Breaking long-running rendering work into small chunks that yield control back to the browser between frames, preventing UI freezes.",
    "tags": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-performance">Performance</span>'],
    "content": """
            <div class="analogy-box">
                <div class="analogy-title">⏰ Analogy: Microwave in 30-Second Bursts</div>
                <p>Imagine you need to microwave food for 5 minutes, but you also need to answer the doorbell if it rings. Instead of running 5 minutes straight (blocking), you run <strong>30 seconds at a time</strong>, check if the doorbell rang, then continue. Each 30-second burst is a "time slice." The food still gets cooked, but you remain responsive to interrupts.</p>
            </div>

            <h2>The Problem: Long Tasks Block the Main Thread</h2>
            <p>The browser's main thread handles everything: rendering, user input, JavaScript execution. If a JavaScript task runs for 200ms straight, the browser can't:</p>
            <ul>
                <li>Process user clicks or keypresses</li>
                <li>Run CSS animations</li>
                <li>Paint new frames (causes visible jank at 60fps = 16.67ms per frame)</li>
            </ul>

            <h2>How Time Slicing Works</h2>
<pre><code><span class="token-comment">// React's scheduler yields every ~5ms to check for higher-priority work</span>
<span class="token-comment">// Simplified model of how React's workLoop operates:</span>

<span class="token-keyword">let</span> deadline = <span class="token-number">0</span>;
<span class="token-keyword">const</span> YIELD_INTERVAL = <span class="token-number">5</span>; <span class="token-comment">// ms — React yields every 5ms</span>

<span class="token-keyword">function</span> <span class="token-function">workLoop</span>() {
    <span class="token-comment">// Process Fiber nodes one at a time</span>
    <span class="token-keyword">while</span> (currentWork !== <span class="token-keyword">null</span>) {
        <span class="token-comment">// Check: should we yield control back to the browser?</span>
        <span class="token-keyword">if</span> (shouldYield()) {
            <span class="token-comment">// Stop working — let browser handle events, paint frames</span>
            <span class="token-comment">// Schedule ourselves to continue later</span>
            scheduleCallback(workLoop);
            <span class="token-keyword">return</span>;
        }
        
        <span class="token-comment">// Process one unit of work (one Fiber/component)</span>
        currentWork = performUnitOfWork(currentWork);
    }
    
    <span class="token-comment">// All work complete — commit to DOM in one batch</span>
    commitRoot();
}

<span class="token-keyword">function</span> <span class="token-function">shouldYield</span>() {
    <span class="token-comment">// Have we used up our time slice?</span>
    <span class="token-keyword">return</span> performance.now() >= deadline;
}

<span class="token-keyword">function</span> <span class="token-function">scheduleCallback</span>(callback) {
    <span class="token-comment">// Use MessageChannel for scheduling (not setTimeout which has 4ms min delay)</span>
    <span class="token-keyword">const</span> channel = <span class="token-keyword">new</span> MessageChannel();
    channel.port1.onmessage = () => {
        deadline = performance.now() + YIELD_INTERVAL;
        callback();
    };
    channel.port2.postMessage(<span class="token-keyword">null</span>);
}
</code></pre>

            <h2>Manual Time Slicing (Without React)</h2>
<pre><code><span class="token-comment">// Processing a large array without blocking the UI</span>

<span class="token-keyword">async function</span> <span class="token-function">processLargeList</span>(items, processItem) {
    <span class="token-keyword">const</span> CHUNK_SIZE = <span class="token-number">100</span>;
    <span class="token-keyword">const</span> results = [];
    
    <span class="token-keyword">for</span> (<span class="token-keyword">let</span> i = <span class="token-number">0</span>; i < items.length; i += CHUNK_SIZE) {
        <span class="token-comment">// Process a chunk</span>
        <span class="token-keyword">const</span> chunk = items.slice(i, i + CHUNK_SIZE);
        <span class="token-keyword">for</span> (<span class="token-keyword">const</span> item <span class="token-keyword">of</span> chunk) {
            results.push(processItem(item));
        }
        
        <span class="token-comment">// Yield to the browser — let it handle events and paint</span>
        <span class="token-keyword">await</span> yieldToMain();
    }
    
    <span class="token-keyword">return</span> results;
}

<span class="token-keyword">function</span> <span class="token-function">yieldToMain</span>() {
    <span class="token-comment">// scheduler.yield() is the modern API (Chrome 115+)</span>
    <span class="token-keyword">if</span> (<span class="token-string">'scheduler'</span> <span class="token-keyword">in</span> window && <span class="token-string">'yield'</span> <span class="token-keyword">in</span> scheduler) {
        <span class="token-keyword">return</span> scheduler.yield();
    }
    <span class="token-comment">// Fallback: setTimeout(0) yields but has minimum 4ms delay</span>
    <span class="token-keyword">return new</span> Promise(resolve => setTimeout(resolve, <span class="token-number">0</span>));
}

<span class="token-comment">// Usage: processing 50,000 items without freezing UI</span>
<span class="token-keyword">await</span> processLargeList(hugeArray, item => transform(item));
</code></pre>

            <h2>Real-World Usage</h2>
            <ul>
                <li><strong>React Scheduler</strong> — Uses MessageChannel-based scheduling to slice rendering work into 5ms chunks. This is what makes concurrent features (useTransition, Suspense) possible.</li>
                <li><strong>Google Maps</strong> — Tile rendering is time-sliced so panning the map remains smooth even while loading new tiles.</li>
                <li><strong>scheduler.yield()</strong> — A new web platform API (Chrome 115+) designed specifically for cooperative yielding without the 4ms setTimeout penalty.</li>
            </ul>

            <div class="understanding-section">
                <h3>✅ You Truly Understand Time Slicing When...</h3>
                <p>You can explain why React uses MessageChannel instead of setTimeout for scheduling, and what the performance difference is (hint: setTimeout has a minimum 4ms delay after 5 nested calls).</p>
                <h3>🧪 Try This Challenge</h3>
                <p>Create a visualization that sorts 10,000 items. Implement it both blocking (one shot) and time-sliced. Measure FPS during each approach using the Performance panel.</p>
                <h3>🔗 Connect It</h3>
                <p>Connects to: <strong>Concurrent Rendering</strong> (time slicing is the mechanism), <strong>Fiber Architecture</strong> (enables pausing at any node), <strong>Event Loop</strong> (understanding when yielded tasks resume), <strong>Long Tasks API</strong> (detecting when you're NOT time-slicing).</p>
            </div>
"""
}

TOPIC_CONTENT[7] = {
    "title": "Reconciliation Algorithm",
    "subtitle": "How React determines the minimal set of DOM changes needed when your component tree updates — the diff algorithm at the heart of virtual DOM.",
    "tags": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-code">Code</span>'],
    "content": """
            <div class="analogy-box">
                <div class="analogy-title">📝 Analogy: Editing a Document</div>
                <p>Imagine you have two versions of a document. Instead of deleting the entire document and rewriting it, you <strong>find the differences</strong> (a word changed here, a paragraph added there) and apply only those changes. Reconciliation is React's "track changes" algorithm — it compares the old virtual tree to the new one and produces the minimum edit script for the real DOM.</p>
            </div>

            <h2>The Problem: DOM Updates Are Expensive</h2>
            <p>Directly manipulating the DOM is slow because every change can trigger layout recalculation, repaint, and reflow. If your app updates 1000 list items but only 3 actually changed, you want to touch the DOM exactly 3 times — not 1000.</p>
            <p>The general tree-diff problem is O(n³) — completely impractical. React's reconciliation uses <strong>two heuristics</strong> to achieve O(n):</p>
            <ol>
                <li><strong>Different element types produce different trees</strong> — If a <code>&lt;div&gt;</code> becomes a <code>&lt;span&gt;</code>, React destroys the old subtree and builds a new one (no deep comparison)</li>
                <li><strong>Keys identify stable elements across renders</strong> — Elements with the same key are the "same" element, just potentially moved or updated</li>
            </ol>

            <h2>The Algorithm Step by Step</h2>
<pre><code><span class="token-comment">// Simplified reconciliation logic</span>

<span class="token-keyword">function</span> <span class="token-function">reconcile</span>(parentDom, oldFiber, newElement) {
    <span class="token-comment">// CASE 1: Same type — update props, recurse on children</span>
    <span class="token-keyword">if</span> (oldFiber && oldFiber.type === newElement.type) {
        <span class="token-comment">// Reuse the DOM node — just update changed attributes</span>
        updateDomProperties(oldFiber.dom, oldFiber.props, newElement.props);
        <span class="token-comment">// Recursively reconcile children</span>
        reconcileChildren(oldFiber, newElement.props.children);
        <span class="token-keyword">return</span>;
    }
    
    <span class="token-comment">// CASE 2: Different type — destroy old, create new</span>
    <span class="token-keyword">if</span> (oldFiber && oldFiber.type !== newElement.type) {
        <span class="token-comment">// Unmount old component tree entirely</span>
        deleteFiber(oldFiber);
        <span class="token-comment">// Create brand new DOM subtree</span>
        createFiber(parentDom, newElement);
        <span class="token-keyword">return</span>;
    }
    
    <span class="token-comment">// CASE 3: New element, no old fiber — mount</span>
    <span class="token-keyword">if</span> (!oldFiber && newElement) {
        createFiber(parentDom, newElement);
        <span class="token-keyword">return</span>;
    }
    
    <span class="token-comment">// CASE 4: Old fiber, no new element — unmount</span>
    <span class="token-keyword">if</span> (oldFiber && !newElement) {
        deleteFiber(oldFiber);
        <span class="token-keyword">return</span>;
    }
}

<span class="token-comment">// Key-based child reconciliation (simplified)</span>
<span class="token-keyword">function</span> <span class="token-function">reconcileChildren</span>(parentFiber, newChildren) {
    <span class="token-keyword">const</span> oldChildren = parentFiber.children;
    <span class="token-keyword">const</span> oldKeyMap = <span class="token-keyword">new</span> Map();
    
    <span class="token-comment">// Build map of old children by key for O(1) lookup</span>
    oldChildren.forEach(child => {
        <span class="token-keyword">if</span> (child.key !== <span class="token-keyword">null</span>) {
            oldKeyMap.set(child.key, child);
        }
    });
    
    newChildren.forEach((newChild, index) => {
        <span class="token-keyword">let</span> oldChild = <span class="token-keyword">null</span>;
        
        <span class="token-keyword">if</span> (newChild.key !== <span class="token-keyword">null</span>) {
            <span class="token-comment">// Key exists — find matching old child (possibly moved)</span>
            oldChild = oldKeyMap.get(newChild.key);
        } <span class="token-keyword">else</span> {
            <span class="token-comment">// No key — match by index position (fragile!)</span>
            oldChild = oldChildren[index];
        }
        
        reconcile(parentFiber.dom, oldChild, newChild);
    });
}
</code></pre>

            <div class="callout callout-warning">
                <div class="callout-title">⚠️ Why Index Keys Are Dangerous</div>
                <p>Using array index as key (<code>key={index}</code>) means React identifies elements by position, not identity. If you insert an item at the beginning of a list, React thinks EVERY element changed (because all indices shifted). This causes unnecessary re-renders and can break component state. Always use stable IDs.</p>
            </div>

            <h2>Real-World Usage</h2>
            <ul>
                <li><strong>React</strong> — Uses this algorithm in the Fiber reconciler. Each Fiber node stores the previous render's output for comparison.</li>
                <li><strong>Vue 3</strong> — Uses a similar algorithm with additional optimizations: compiler-generated "patch flags" tell the runtime exactly which attributes might change.</li>
                <li><strong>Preact</strong> — Smaller implementation of the same algorithm, optimized for bundle size over edge-case performance.</li>
            </ul>

            <div class="understanding-section">
                <h3>✅ You Truly Understand Reconciliation When...</h3>
                <p>You can predict exactly which DOM nodes React will create, update, or destroy given a before/after component tree — and explain why keys change the answer.</p>
                <h3>🧪 Try This Challenge</h3>
                <p>Create a sortable list. First use <code>key={index}</code>, then switch to <code>key={item.id}</code>. Open React DevTools "Highlight Updates" to visualize the difference in what re-renders.</p>
                <h3>🔗 Connect It</h3>
                <p>Connects to: <strong>Virtual DOM Diffing Complexity</strong> (the O(n) vs O(n³) trade-off), <strong>Fiber Architecture</strong> (where reconciliation results are stored), <strong>Structural Sharing</strong> (reusing unchanged parts of the tree).</p>
            </div>
"""
}

TOPIC_CONTENT[8] = {
    "title": "Fiber Architecture",
    "subtitle": "React's internal data structure that represents the component tree as a linked list of 'fibers,' enabling interruptible rendering, priorities, and concurrent features.",
    "tags": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-code">Code</span>'],
    "content": """
            <div class="analogy-box">
                <div class="analogy-title">🧬 Analogy: A To-Do List You Can Pause</div>
                <p>The old React (stack reconciler) was like reading a book cover-to-cover — you couldn't bookmark your place and come back. Fiber is like a <strong>checklist</strong> where each item (component) is a separate card. You can stop after any card, handle an interruption, then pick up exactly where you left off. Each card points to the next one — it's a linked list of work units.</p>
            </div>

            <h2>The Problem: Stack Recursion Can't Be Paused</h2>
            <p>React's pre-Fiber reconciler used the JavaScript call stack directly. When rendering a tree of 10,000 components:</p>
            <ul>
                <li>It recursed into each component, one by one</li>
                <li>The call stack grew deeper with each nested component</li>
                <li>You cannot pause or resume a call stack — it must run to completion</li>
                <li>Result: 200ms+ blocking the main thread</li>
            </ul>

            <h2>What a Fiber Is</h2>
<pre><code><span class="token-comment">// Each component instance becomes a Fiber node</span>
<span class="token-comment">// This is (simplified) what React stores internally</span>

<span class="token-keyword">interface</span> Fiber {
    <span class="token-comment">// Identity</span>
    type: Function | <span class="token-builtin">string</span>;     <span class="token-comment">// Component function or DOM tag ('div')</span>
    key: <span class="token-builtin">string</span> | <span class="token-keyword">null</span>;           <span class="token-comment">// Reconciliation key</span>
    
    <span class="token-comment">// Tree structure (linked list, not array of children)</span>
    child: Fiber | <span class="token-keyword">null</span>;          <span class="token-comment">// First child</span>
    sibling: Fiber | <span class="token-keyword">null</span>;        <span class="token-comment">// Next sibling</span>
    return: Fiber | <span class="token-keyword">null</span>;         <span class="token-comment">// Parent (called "return" because it's where we return to)</span>
    
    <span class="token-comment">// State</span>
    memoizedState: <span class="token-builtin">any</span>;          <span class="token-comment">// Hooks linked list (useState, useEffect, etc.)</span>
    memoizedProps: <span class="token-builtin">object</span>;        <span class="token-comment">// Props from last render</span>
    pendingProps: <span class="token-builtin">object</span>;         <span class="token-comment">// Props for this render</span>
    
    <span class="token-comment">// Work tracking</span>
    flags: <span class="token-builtin">number</span>;               <span class="token-comment">// What effects to apply (Placement, Update, Deletion)</span>
    lanes: <span class="token-builtin">number</span>;               <span class="token-comment">// Priority lanes (which updates affect this fiber)</span>
    
    <span class="token-comment">// Double buffering</span>
    alternate: Fiber | <span class="token-keyword">null</span>;      <span class="token-comment">// The "other" version (current vs work-in-progress)</span>
    
    <span class="token-comment">// Output</span>
    stateNode: DOMElement | <span class="token-keyword">null</span>; <span class="token-comment">// The actual DOM node (for host components)</span>
}
</code></pre>

            <div class="callout callout-info">
                <div class="callout-title">💡 Double Buffering</div>
                <p>React maintains TWO fiber trees simultaneously: the <strong>current tree</strong> (what's on screen) and the <strong>work-in-progress tree</strong> (what's being built). When rendering completes, React swaps them — the work-in-progress becomes current. This is like double buffering in games: you draw to a back buffer, then flip. The <code>alternate</code> pointer connects each fiber to its counterpart in the other tree.</p>
            </div>

            <h2>The Work Loop: Traversal</h2>
<pre><code><span class="token-comment">// React traverses the Fiber tree using this pattern:</span>
<span class="token-comment">// 1. Go DOWN (child) — "begin work" on each fiber</span>
<span class="token-comment">// 2. When no more children, go SIDEWAYS (sibling)</span>
<span class="token-comment">// 3. When no more siblings, go UP (return)</span>

<span class="token-keyword">function</span> <span class="token-function">workLoop</span>(fiber) {
    <span class="token-keyword">while</span> (fiber) {
        <span class="token-comment">// Process this fiber (render the component, diff props)</span>
        <span class="token-keyword">const</span> next = beginWork(fiber);
        
        <span class="token-keyword">if</span> (next) {
            <span class="token-comment">// Has child — go deeper</span>
            fiber = next;
        } <span class="token-keyword">else</span> {
            <span class="token-comment">// No child — complete this fiber and look for sibling</span>
            <span class="token-keyword">let</span> current = fiber;
            <span class="token-keyword">while</span> (current) {
                completeWork(current);
                <span class="token-keyword">if</span> (current.sibling) {
                    fiber = current.sibling;
                    <span class="token-keyword">break</span>;
                }
                <span class="token-comment">// No sibling — go up to parent</span>
                current = current.return;
            }
            <span class="token-keyword">if</span> (!current) fiber = <span class="token-keyword">null</span>; <span class="token-comment">// Done!</span>
        }
        
        <span class="token-comment">// ⭐ KEY: We can stop here and resume later!</span>
        <span class="token-keyword">if</span> (shouldYield()) <span class="token-keyword">return</span>;
    }
}
</code></pre>

            <h2>Real-World Usage</h2>
            <ul>
                <li><strong>React 16+</strong> — The Fiber reconciler replaced the stack reconciler. Every React app today runs on Fiber.</li>
                <li><strong>React DevTools</strong> — The component tree you see IS the Fiber tree. Hooks panel shows the <code>memoizedState</code> linked list.</li>
                <li><strong>React Native</strong> — Same Fiber architecture, different "host" layer. Fibers resolve to native views instead of DOM nodes.</li>
            </ul>

            <div class="understanding-section">
                <h3>✅ You Truly Understand Fiber When...</h3>
                <p>You can draw the linked-list traversal (child → sibling → return) for a given component tree and explain why this linked list (vs recursive call stack) enables interruptibility.</p>
                <h3>🧪 Try This Challenge</h3>
                <p>Open React DevTools, inspect a component, and find its Fiber node in the browser console using <code>$r._debugOwner</code>. Navigate the <code>child</code>, <code>sibling</code>, and <code>return</code> pointers to understand the tree structure.</p>
                <h3>🔗 Connect It</h3>
                <p>Connects to: <strong>Reconciliation</strong> (Fiber is where reconciliation happens), <strong>Time Slicing</strong> (Fiber enables the "yield" points), <strong>Concurrent Rendering</strong> (the user-facing feature Fiber makes possible).</p>
            </div>
"""
}

TOPIC_CONTENT[9] = {
    "title": "Virtual DOM Diffing Complexity",
    "subtitle": "Understanding the O(n) heuristic diff algorithm that virtual DOM libraries use — and why the theoretical O(n³) general tree edit distance is avoided.",
    "tags": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-code">Code</span>'],
    "content": """
            <div class="analogy-box">
                <div class="analogy-title">📊 Analogy: Comparing Two Org Charts</div>
                <p>Finding the minimum edits to transform one arbitrary tree into another (moving nodes, renaming, adding, deleting) is O(n³). But if you know that <strong>departments don't change type</strong> (engineering stays engineering) and <strong>people keep their employee IDs</strong> (keys), you can compare level-by-level in O(n). React's diff is this simplified comparison — it sacrifices theoretical optimality for practical speed.</p>
            </div>

            <h2>The Theoretical Problem: Tree Edit Distance is O(n³)</h2>
            <p>The general tree edit distance problem asks: "Given tree A and tree B, what's the minimum number of insertions, deletions, and moves to transform A into B?" The best known algorithm for this is O(n³). For a tree with 10,000 nodes, that's 10¹² operations — completely unusable at 60fps.</p>

            <h2>React's O(n) Heuristic</h2>
            <p>React trades optimality for speed with two constraints:</p>
            <ol>
                <li><strong>Level-by-level comparison only</strong> — React never moves a node to a different depth. If a component moves from being a child to a grandchild, React destroys and recreates it.</li>
                <li><strong>Same-type assumption</strong> — If the element type changes (div → span, ComponentA → ComponentB), React doesn't even look at children — it tears down the entire subtree.</li>
            </ol>
<pre><code><span class="token-comment">// Why React's diff is O(n):</span>
<span class="token-comment">// It only compares nodes at the same position in the tree</span>

<span class="token-comment">// Before:</span>
<span class="token-comment">//   div</span>
<span class="token-comment">//   ├── h1 "Title"</span>
<span class="token-comment">//   └── p "Content"</span>

<span class="token-comment">// After:</span>
<span class="token-comment">//   div</span>
<span class="token-comment">//   ├── h1 "New Title"  ← Same type (h1), just update text: O(1)</span>
<span class="token-comment">//   └── span "Content"  ← Different type! Destroy p, create span: O(1)</span>

<span class="token-comment">// Total: 2 comparisons for 2 children = O(n)</span>
<span class="token-comment">// No cross-level comparison, no optimal move detection</span>
</code></pre>

            <h2>List Diffing with Keys: O(n) with Reordering</h2>
<pre><code><span class="token-comment">// For lists, React uses keys to match elements across renders</span>
<span class="token-comment">// This uses a two-pointer + map approach similar to LCS</span>

<span class="token-comment">// Before: [A, B, C, D]</span>
<span class="token-comment">// After:  [D, A, B, C]  (D moved to front)</span>

<span class="token-comment">// Without keys (by index):</span>
<span class="token-comment">//   Index 0: A → D (different! destroy A, create D)</span>
<span class="token-comment">//   Index 1: B → A (different! destroy B, create A)</span>
<span class="token-comment">//   Index 2: C → B (different! destroy C, create B)</span>
<span class="token-comment">//   Index 3: D → C (different! destroy D, create C)</span>
<span class="token-comment">//   Result: 4 destroy + 4 create = 8 DOM operations!</span>

<span class="token-comment">// With keys:</span>
<span class="token-comment">//   Key "D": was at index 3, now at index 0 → MOVE</span>
<span class="token-comment">//   Keys "A","B","C": same relative order → no moves needed</span>
<span class="token-comment">//   Result: 1 DOM move operation!</span>
</code></pre>

            <h2>When the Heuristic Fails</h2>
            <table class="comparison-table">
                <thead><tr><th>Scenario</th><th>What React Does</th><th>Optimal Solution</th></tr></thead>
                <tbody>
                    <tr><td>Component moves to different depth</td><td>Destroy + recreate</td><td>Move (preserving state)</td></tr>
                    <tr><td>Type changes but children are same</td><td>Destroy entire subtree</td><td>Reuse children</td></tr>
                    <tr><td>List without keys, item inserted at start</td><td>Mutate every item</td><td>Insert one item</td></tr>
                </tbody>
            </table>

            <div class="understanding-section">
                <h3>✅ You Truly Understand Virtual DOM Diffing When...</h3>
                <p>You can explain why wrapping a component in an extra div (changing tree depth) causes all descendants to unmount/remount, destroying their state — and why this is an acceptable trade-off.</p>
                <h3>🧪 Try This Challenge</h3>
                <p>Create a list where items have input fields. Render without keys, type in the inputs, then sort the list. Observe how state (input values) gets mixed up. Now add proper keys and repeat.</p>
                <h3>🔗 Connect It</h3>
                <p>Connects to: <strong>Reconciliation Algorithm</strong> (this IS the reconciliation algorithm's complexity), <strong>Structural Sharing</strong> (immutability helps skip subtrees), <strong>Memoization</strong> (React.memo short-circuits the diff).</p>
            </div>
"""
}

TOPIC_CONTENT[10] = {
    "title": "Structural Sharing",
    "subtitle": "A technique where updated data structures reuse unchanged parts of the old structure rather than copying everything — the backbone of efficient immutable state management.",
    "tags": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-code">Code</span>'],
    "content": """
            <div class="analogy-box">
                <div class="analogy-title">🌲 Analogy: Changing a Leaf on a Tree</div>
                <p>Imagine a tree with 1000 branches. If one leaf changes color, you don't grow an entirely new tree. You create a <strong>new path from root to the changed leaf</strong>, pointing to the same unchanged branches. The old tree still exists (immutability), but you only allocated memory for the changed path — not the whole tree.</p>
            </div>

            <h2>The Problem: Naive Immutability is Expensive</h2>
<pre><code><span class="token-comment">// Naive deep copy for immutability — O(n) time and space EVERY update</span>
<span class="token-keyword">const</span> newState = JSON.parse(JSON.stringify(state));
newState.users[42].name = <span class="token-string">"Alice"</span>;
<span class="token-comment">// Copied ALL 10,000 users just to change one name!</span>

<span class="token-comment">// Structural sharing — only copy the PATH to the change</span>
<span class="token-keyword">const</span> newState = {
    ...state,                    <span class="token-comment">// Reuse top-level references</span>
    users: [
        ...state.users.slice(<span class="token-number">0</span>, <span class="token-number">42</span>),  <span class="token-comment">// Reuse array prefix references</span>
        { ...state.users[<span class="token-number">42</span>], name: <span class="token-string">"Alice"</span> }, <span class="token-comment">// New object for changed item</span>
        ...state.users.slice(<span class="token-number">43</span>)   <span class="token-comment">// Reuse array suffix references</span>
    ]
};
<span class="token-comment">// Only the users array and user[42] are new objects</span>
<span class="token-comment">// Everything else is SHARED with the old state (same memory)</span>
</code></pre>

            <h2>How Immer Implements Structural Sharing</h2>
<pre><code><span class="token-keyword">import</span> { produce } <span class="token-keyword">from</span> <span class="token-string">'immer'</span>;

<span class="token-keyword">const</span> state = {
    users: [{ id: <span class="token-number">1</span>, name: <span class="token-string">"Bob"</span> }, { id: <span class="token-number">2</span>, name: <span class="token-string">"Carol"</span> }],
    settings: { theme: <span class="token-string">"dark"</span>, lang: <span class="token-string">"en"</span> }
};

<span class="token-keyword">const</span> nextState = produce(state, draft => {
    <span class="token-comment">// Immer uses Proxies to track which parts you actually modify</span>
    draft.users[<span class="token-number">0</span>].name = <span class="token-string">"Alice"</span>;
});

<span class="token-comment">// What Immer produced via structural sharing:</span>
nextState !== state;                   <span class="token-comment">// true — new root</span>
nextState.users !== state.users;       <span class="token-comment">// true — users array changed</span>
nextState.users[<span class="token-number">0</span>] !== state.users[<span class="token-number">0</span>]; <span class="token-comment">// true — this user changed</span>
nextState.users[<span class="token-number">1</span>] === state.users[<span class="token-number">1</span>]; <span class="token-comment">// TRUE! Same reference — unchanged</span>
nextState.settings === state.settings; <span class="token-comment">// TRUE! Same reference — untouched</span>
</code></pre>

            <h2>Persistent Data Structures (Tries)</h2>
<pre><code><span class="token-comment">// Libraries like Immutable.js use Hash Array Mapped Tries (HAMT)</span>
<span class="token-comment">// This gives O(log₃₂ n) ≈ O(1) updates with structural sharing</span>

<span class="token-comment">// Conceptual model of a 32-way branching trie:</span>
<span class="token-comment">//         ROOT</span>
<span class="token-comment">//       /   |   \</span>
<span class="token-comment">//     [0-31] [32-63] [64-95] ...</span>
<span class="token-comment">//     /  \</span>
<span class="token-comment">//   [0-15] [16-31]</span>

<span class="token-comment">// To update index 42:</span>
<span class="token-comment">// 1. Create new root pointing to new branch for [32-63]</span>
<span class="token-comment">// 2. Create new [32-63] node pointing to new leaf at position 42</span>
<span class="token-comment">// 3. All other branches are SHARED with old trie</span>
<span class="token-comment">// 4. Total new nodes: O(log₃₂ n) ≈ 4 for a million elements</span>
</code></pre>

            <h2>Real-World Usage</h2>
            <ul>
                <li><strong>Redux</strong> — Relies on structural sharing for change detection. <code>useSelector</code> uses <code>===</code> to check if state slices changed — only works because unchanged parts keep the same reference.</li>
                <li><strong>Immer (used by Redux Toolkit)</strong> — Automatically produces structurally-shared immutable updates using Proxies.</li>
                <li><strong>Immutable.js (Facebook)</strong> — Persistent data structures with O(log₃₂n) structural sharing via HAMTs.</li>
                <li><strong>Clojure/ClojureScript</strong> — Language-level persistent data structures that pioneered this approach in the frontend world.</li>
            </ul>

            <div class="understanding-section">
                <h3>✅ You Truly Understand Structural Sharing When...</h3>
                <p>You can explain why <code>state.settings === nextState.settings</code> being true lets React skip re-rendering the Settings component, and why deep-copying would break this optimization.</p>
                <h3>🧪 Try This Challenge</h3>
                <p>Create a Redux store with nested state. Log <code>Object.is(prev.nested, next.nested)</code> in a selector. Observe that untouched slices keep referential equality — then break it by accidentally spreading everything.</p>
                <h3>🔗 Connect It</h3>
                <p>Connects to: <strong>Immutable Data Patterns</strong> (structural sharing makes immutability efficient), <strong>Referential Equality</strong> (how React detects changes), <strong>Memoization</strong> (useMemo/useCallback rely on stable references).</p>
            </div>
"""
}

def generate_topic_html(num, slug, title, module_name, content_data):
    """Generate a complete HTML file for a topic."""
    
    # Get nav info
    all_topics = get_all_topics()
    prev_topic = None
    next_topic = None
    for i, (n, s, t, m) in enumerate(all_topics):
        if n == num:
            if i > 0:
                pn, ps, pt, pm = all_topics[i-1]
                prev_topic = (pn, ps, pt)
            if i < len(all_topics) - 1:
                nn, ns, nt, nm = all_topics[i+1]
                next_topic = (nn, ns, nt)
            break
    
    nav_footer = '            <div class="nav-footer">\n'
    if prev_topic:
        nav_footer += f'                <a href="{prev_topic[0]:02d}-{prev_topic[1]}.html" class="nav-btn">← {prev_topic[2]}</a>\n'
    if next_topic:
        nav_footer += f'                <a href="{next_topic[0]:02d}-{next_topic[1]}.html" class="nav-btn nav-btn-next">{next_topic[2]} →</a>\n'
    nav_footer += '            </div>'
    
    tags_html = ' '.join(content_data.get('tags', []))
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Frontend Concepts Deep Dive</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="sidebar-overlay"></div>

{SIDEBAR}

    <header class="topbar">
        <div class="topbar-left">
            <button class="hamburger">☰</button>
            <div class="breadcrumb">
                <a href="index.html">Frontend Concepts</a>
                <span>/</span> {title}
            </div>
        </div>
        <div class="topbar-right">
            <button class="theme-toggle">🌙</button>
        </div>
    </header>

    <main class="main-content">
        <div class="content-wrapper">

            <div class="hero">
                <h1>{title}</h1>
                <p class="subtitle">{content_data["subtitle"]}</p>
                <div class="tag-row">
                    {tags_html}
                </div>
            </div>

{content_data["content"]}

{nav_footer}

        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>'''
    return html


def generate_placeholder_content(num, slug, title, module_name):
    """Generate placeholder for topics not yet fully written."""
    tags_map = {
        "Rendering & Hydration": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-browser">Browser</span>'],
        "React Internals": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-code">Code</span>'],
        "Data & State Patterns": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-code">Code</span>'],
        "Event Loop & Scheduling": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-browser">Browser</span>'],
        "Browser Rendering Pipeline": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-performance">Performance</span>', '<span class="tag tag-browser">Browser</span>'],
        "Bundling & Code Delivery": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-performance">Performance</span>'],
        "Web Components": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-browser">Browser</span>'],
        "Workers & Threading": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-browser">Browser</span>'],
        "Compositing & GPU": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-performance">Performance</span>', '<span class="tag tag-browser">Browser</span>'],
        "Observer APIs": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-code">Code</span>', '<span class="tag tag-browser">Browser</span>'],
        "Storage & Caching": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-performance">Performance</span>'],
        "Network & Protocols": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-performance">Performance</span>'],
        "Security": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-security">Security</span>', '<span class="tag tag-browser">Browser</span>'],
        "Concurrent UI Patterns": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-code">Code</span>'],
        "Architecture & State Machines": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-code">Code</span>'],
        "Offline & Collaboration": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-code">Code</span>'],
        "Streams & Async Patterns": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-code">Code</span>', '<span class="tag tag-browser">Browser</span>'],
        "Memory & GC": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-performance">Performance</span>', '<span class="tag tag-browser">Browser</span>'],
        "Performance APIs & Metrics": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-performance">Performance</span>', '<span class="tag tag-browser">Browser</span>'],
        "Advanced Patterns": ['<span class="tag tag-advanced">Advanced</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-code">Code</span>'],
        "Accessibility Internals": ['<span class="tag tag-intermediate">Intermediate</span>', '<span class="tag tag-concept">Concept</span>', '<span class="tag tag-browser">Browser</span>'],
    }
    return {
        "tags": tags_map.get(module_name, ['<span class="tag tag-concept">Concept</span>']),
    }


if __name__ == "__main__":
    all_topics = get_all_topics()
    
    for num, slug, title, module_name in all_topics:
        filename = f"{num:02d}-{slug}.html"
        filepath = os.path.join(BASE_DIR, filename)
        
        if num in TOPIC_CONTENT:
            content_data = TOPIC_CONTENT[num]
        else:
            # We'll need to generate remaining content
            continue
        
        html = generate_topic_html(num, slug, title, module_name, content_data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Created: {filename}")
    
    print(f"\nGenerated {len([n for n in TOPIC_CONTENT])} topic files")
    print("Run the expanded generator for remaining topics.")
