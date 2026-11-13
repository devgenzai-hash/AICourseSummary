"""
Template engine for generating System Design course topic files.
Run: python gen_template.py
This generates a base HTML file for each topic that doesn't yet exist.
"""
import os

SIDEBAR_NAV = """            <li><a href="index.html"><span class="nav-number">🏠</span> Course Overview</a></li>
            <li class="module-label">Concurrency Foundations</li>
            <li><a href="01-threads-vs-processes.html"><span class="nav-number">1</span> Threads vs Processes</a></li>
            <li><a href="02-context-switching.html"><span class="nav-number">2</span> Context Switching</a></li>
            <li><a href="03-race-conditions.html"><span class="nav-number">3</span> Race Conditions</a></li>
            <li><a href="04-critical-sections.html"><span class="nav-number">4</span> Critical Sections</a></li>
            <li><a href="05-mutex-locks.html"><span class="nav-number">5</span> Mutex &amp; Locks</a></li>
            <li><a href="06-deadlocks.html"><span class="nav-number">6</span> Deadlocks</a></li>
            <li><a href="07-livelocks-starvation.html"><span class="nav-number">7</span> Livelocks &amp; Starvation</a></li>
            <li><a href="08-thread-safety.html"><span class="nav-number">8</span> Thread Safety</a></li>
            <li class="module-label">Low-Level Concurrency</li>
            <li><a href="09-atomic-operations-cas.html"><span class="nav-number">9</span> Atomic Ops &amp; CAS</a></li>
            <li><a href="10-memory-visibility.html"><span class="nav-number">10</span> Memory Visibility</a></li>
            <li><a href="11-happens-before.html"><span class="nav-number">11</span> Happens-Before</a></li>
            <li><a href="12-volatile-vs-synchronized.html"><span class="nav-number">12</span> Volatile vs Synchronized</a></li>
            <li><a href="13-false-sharing.html"><span class="nav-number">13</span> False Sharing</a></li>
            <li class="module-label">Concurrency Patterns</li>
            <li><a href="14-thread-pools.html"><span class="nav-number">14</span> Thread Pools</a></li>
            <li><a href="15-futures-promises-async.html"><span class="nav-number">15</span> Futures &amp; Async</a></li>
            <li><a href="16-producer-consumer.html"><span class="nav-number">16</span> Producer-Consumer</a></li>
            <li><a href="17-blocking-vs-nonblocking.html"><span class="nav-number">17</span> Blocking vs Non-Blocking</a></li>
            <li><a href="18-lock-free-wait-free.html"><span class="nav-number">18</span> Lock-Free Algorithms</a></li>
            <li><a href="19-read-write-locks.html"><span class="nav-number">19</span> Read-Write Locks</a></li>
            <li><a href="20-semaphore-latch-barrier.html"><span class="nav-number">20</span> Semaphore/Latch/Barrier</a></li>
            <li class="module-label">Distributed Systems Core</li>
            <li><a href="21-cap-theorem.html"><span class="nav-number">21</span> CAP Theorem</a></li>
            <li><a href="22-acid-properties.html"><span class="nav-number">22</span> ACID Properties</a></li>
            <li><a href="23-consistent-hashing.html"><span class="nav-number">23</span> Consistent Hashing</a></li>
            <li><a href="24-leader-election.html"><span class="nav-number">24</span> Leader Election</a></li>
            <li><a href="25-distributed-consensus.html"><span class="nav-number">25</span> Distributed Consensus</a></li>
            <li><a href="26-replication.html"><span class="nav-number">26</span> Replication</a></li>
            <li><a href="27-partitioning-sharding.html"><span class="nav-number">27</span> Partitioning &amp; Sharding</a></li>
            <li><a href="28-quorum-reads-writes.html"><span class="nav-number">28</span> Quorum Reads/Writes</a></li>
            <li><a href="29-gossip-protocol.html"><span class="nav-number">29</span> Gossip Protocol</a></li>
            <li><a href="30-failure-detection.html"><span class="nav-number">30</span> Failure Detection</a></li>
            <li><a href="31-distributed-locking.html"><span class="nav-number">31</span> Distributed Locking</a></li>
            <li><a href="32-saga-pattern.html"><span class="nav-number">32</span> Saga Pattern</a></li>
            <li class="module-label">Resilience Patterns</li>
            <li><a href="33-idempotency.html"><span class="nav-number">33</span> Idempotency</a></li>
            <li><a href="34-delivery-guarantees.html"><span class="nav-number">34</span> Delivery Guarantees</a></li>
            <li><a href="35-backpressure.html"><span class="nav-number">35</span> Backpressure</a></li>
            <li><a href="36-circuit-breaker.html"><span class="nav-number">36</span> Circuit Breaker</a></li>
            <li><a href="37-rate-limiting.html"><span class="nav-number">37</span> Rate Limiting</a></li>
            <li><a href="38-throttling.html"><span class="nav-number">38</span> Throttling</a></li>
            <li><a href="39-retry-backoff.html"><span class="nav-number">39</span> Retry with Backoff</a></li>
            <li class="module-label">Database Engineering</li>
            <li><a href="40-isolation-levels.html"><span class="nav-number">40</span> Isolation Levels</a></li>
            <li><a href="41-indexing-internals.html"><span class="nav-number">41</span> Indexing Internals</a></li>
            <li><a href="42-write-read-amplification.html"><span class="nav-number">42</span> Write/Read Amplification</a></li>
            <li><a href="43-composite-index.html"><span class="nav-number">43</span> Composite Index</a></li>
            <li><a href="44-query-optimization.html"><span class="nav-number">44</span> Query Optimization</a></li>
            <li><a href="45-caching-strategies.html"><span class="nav-number">45</span> Caching Strategies</a></li>
            <li><a href="46-cache-invalidation.html"><span class="nav-number">46</span> Cache Invalidation</a></li>
            <li><a href="47-cache-stampede.html"><span class="nav-number">47</span> Cache Stampede</a></li>
            <li class="module-label">Architecture Patterns</li>
            <li><a href="48-event-driven-vs-request-response.html"><span class="nav-number">48</span> Event-Driven vs Req/Res</a></li>
            <li><a href="49-pagination.html"><span class="nav-number">49</span> Pagination</a></li>
            <li class="module-label">Design Patterns</li>
            <li><a href="50-singleton.html"><span class="nav-number">50</span> Singleton</a></li>
            <li><a href="51-factory-method.html"><span class="nav-number">51</span> Factory Method</a></li>
            <li><a href="52-builder.html"><span class="nav-number">52</span> Builder</a></li>
            <li><a href="53-adapter.html"><span class="nav-number">53</span> Adapter</a></li>
            <li><a href="54-decorator.html"><span class="nav-number">54</span> Decorator</a></li>
            <li><a href="55-facade.html"><span class="nav-number">55</span> Facade</a></li>
            <li><a href="56-observer.html"><span class="nav-number">56</span> Observer</a></li>
            <li><a href="57-strategy.html"><span class="nav-number">57</span> Strategy</a></li>
            <li><a href="58-command.html"><span class="nav-number">58</span> Command</a></li>
            <li class="module-label">API &amp; Communication</li>
            <li><a href="59-api-gateway.html"><span class="nav-number">59</span> API Gateway</a></li>
            <li><a href="60-load-balancer.html"><span class="nav-number">60</span> Load Balancer</a></li>
            <li><a href="61-reverse-proxy.html"><span class="nav-number">61</span> Reverse Proxy</a></li>
            <li><a href="62-graphql.html"><span class="nav-number">62</span> GraphQL</a></li>
            <li><a href="63-grpc.html"><span class="nav-number">63</span> gRPC</a></li>
            <li><a href="64-webhooks.html"><span class="nav-number">64</span> Webhooks</a></li>
            <li class="module-label">Security</li>
            <li><a href="65-jwt.html"><span class="nav-number">65</span> JWT</a></li>
            <li><a href="66-oauth.html"><span class="nav-number">66</span> OAuth</a></li>
            <li><a href="67-csrf.html"><span class="nav-number">67</span> CSRF</a></li>
            <li><a href="68-mtls.html"><span class="nav-number">68</span> mTLS</a></li>"""


def template(title, subtitle, tags, analogy_title, analogy, content, summary, mental_model, mistakes, exercise, prev_link, prev_title, next_link, next_title):
    tags_html = "\n".join(f'                    <span class="tag tag-{t}">{t.title()}</span>' for t in tags)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - System Design Course</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="sidebar-overlay"></div>
    <aside class="sidebar">
        <div class="sidebar-header"><h2>System Design</h2><div class="subtitle">Beginner → Advanced &bull; 68 Topics</div></div>
        <ul class="sidebar-nav">
{SIDEBAR_NAV}
        </ul>
        <div class="progress-tracker">
            <div class="progress-label">Progress: 0/68 topics completed</div>
            <div class="progress-bar"><div class="progress-bar-fill" style="width: 0%"></div></div>
        </div>
    </aside>

    <header class="topbar">
        <div class="topbar-left">
            <button class="hamburger">&#9776;</button>
            <div class="breadcrumb"><a href="index.html">System Design</a><span>/</span> {title}</div>
        </div>
        <div class="topbar-right"><button class="theme-toggle">&#127769;</button></div>
    </header>

    <main class="main-content">
        <div class="content-wrapper">
            <div class="hero">
                <h1>{title}</h1>
                <p class="subtitle">{subtitle}</p>
                <div class="tag-row">
{tags_html}
                </div>
            </div>

            <div class="analogy-box">
                <div class="analogy-title">{analogy_title}</div>
                {analogy}
            </div>

{content}

            <div class="summary-box">
                <h3>&#128221; Summary</h3>
                {summary}
            </div>

            <div class="mental-model">
                <h3>&#129504; Mental Model</h3>
                <div class="model-visual">{mental_model}</div>
            </div>

            <div class="mistakes-box">
                <h3>&#10060; Common Beginner Mistakes</h3>
                {mistakes}
            </div>

            <div class="exercise-box">
                <h3>&#127947; Hands-On Exercise</h3>
                {exercise}
            </div>

            <nav class="page-nav">
                <a href="{prev_link}" class="prev">{prev_title}</a>
                <a href="{next_link}" class="next">{next_title}</a>
            </nav>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>'''


def write_topic(filename, **kwargs):
    """Write a topic file if it doesn't already exist."""
    output_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(output_dir, filename)
    if os.path.exists(filepath):
        print(f"  SKIP: {filename}")
        return False
    html = template(**kwargs)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  CREATED: {filename}")
    return True
