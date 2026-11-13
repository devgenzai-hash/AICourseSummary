"""
Generate all 68 topic HTML files for the System Design course.
Run this script from the systemDesign/ directory.
"""

import os

SIDEBAR_NAV = '''            <li><a href="index.html"><span class="nav-number">🏠</span> Course Overview</a></li>
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
            <li><a href="68-mtls.html"><span class="nav-number">68</span> mTLS</a></li>'''


# All 68 topics with their content
TOPICS = [
    # Already created: 01, 02
    {
        "num": "03", "file": "03-race-conditions.html",
        "title": "Race Conditions",
        "subtitle": "When two threads try to change the same data at the same time and chaos ensues. The #1 most common concurrency bug in all of software engineering.",
        "tags": ['beginner', 'concept', 'code'],
        "analogy_title": "🏠 Daily-Life Analogy: Two People, One Bank Account",
        "analogy": """<p>Imagine you and your partner both have debit cards for the same bank account with $1,000. At the exact same moment:</p>
                <ul>
                    <li><strong>You</strong> check the balance: $1,000 ✓ — withdraw $800</li>
                    <li><strong>Partner</strong> checks the balance: $1,000 ✓ — withdraw $700</li>
                </ul>
                <p>Both see $1,000, both think the withdrawal is safe. Result: <strong>$1,500 withdrawn from a $1,000 account</strong>. The bank loses money because two operations "raced" against each other.</p>
                <p>This is a race condition. The outcome depends on <strong>who runs first</strong> — and in a computer, that's unpredictable.</p>""",
        "content": """
            <h2>What Is a Race Condition?</h2>
            <p>A <strong>race condition</strong> occurs when the behavior of a program depends on the <strong>relative timing</strong> of two or more threads. The result is different depending on who "wins the race" — which thread executes first.</p>
            <p>The technical definition: A race condition exists when <strong>two or more threads access shared data</strong>, at least one of them <strong>writes</strong> to it, and there is <strong>no synchronization</strong> to control the order of access.</p>

            <h3>The Classic Example: Counter Increment</h3>
            <p>The statement <code>counter += 1</code> looks atomic (one step), but it's actually THREE steps:</p>
            <ol>
                <li><strong>READ</strong> the current value of counter from memory</li>
                <li><strong>ADD</strong> 1 to the value</li>
                <li><strong>WRITE</strong> the new value back to memory</li>
            </ol>

<pre><code><span class="token-keyword">import</span> threading

counter = <span class="token-number">0</span>

<span class="token-keyword">def</span> <span class="token-function">increment</span>():
    <span class="token-keyword">global</span> counter
    <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">100_000</span>):
        counter += <span class="token-number">1</span>  <span class="token-comment"># NOT atomic! This is READ → ADD → WRITE</span>

<span class="token-comment"># Launch 10 threads all incrementing the same counter</span>
threads = [threading.Thread(target=increment) <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10</span>)]
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.start()
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.join()

print(<span class="token-string">f"Expected: 1,000,000"</span>)
print(<span class="token-string">f"Actual:   {counter}"</span>)  <span class="token-comment"># Something less! e.g., 834,291</span>
<span class="token-comment"># Run it multiple times — you get DIFFERENT results each time!</span></code></pre>

            <div class="callout callout-danger">
                <div class="callout-title">🔥 Why It Breaks</div>
                <p>Thread A reads counter=100, Thread B reads counter=100. Thread A writes 101. Thread B writes 101. We lost an increment! This happened thousands of times during the run.</p>
            </div>

            <h2>Types of Race Conditions</h2>
            <table class="comparison-table">
                <thead>
                    <tr><th>Type</th><th>Description</th><th>Example</th></tr>
                </thead>
                <tbody>
                    <tr><td><strong>Check-then-act</strong></td><td>Check a condition, then act on it — but condition changes between check and act</td><td>if file exists → read file (file deleted between check and read)</td></tr>
                    <tr><td><strong>Read-modify-write</strong></td><td>Read a value, modify it, write it back — another thread modifies in between</td><td>counter += 1 (our example above)</td></tr>
                    <tr><td><strong>Compound operations</strong></td><td>Multiple operations that need to be atomic but aren't</td><td>Transfer money: debit A, credit B (crash between = money lost)</td></tr>
                </tbody>
            </table>

            <h2>The Fix: Synchronization</h2>
<pre><code><span class="token-keyword">import</span> threading

counter = <span class="token-number">0</span>
lock = threading.Lock()  <span class="token-comment"># The fix!</span>

<span class="token-keyword">def</span> <span class="token-function">safe_increment</span>():
    <span class="token-keyword">global</span> counter
    <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">100_000</span>):
        <span class="token-keyword">with</span> lock:  <span class="token-comment"># Only one thread can be here at a time</span>
            counter += <span class="token-number">1</span>

threads = [threading.Thread(target=safe_increment) <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10</span>)]
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.start()
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.join()

print(<span class="token-string">f"Result: {counter}"</span>)  <span class="token-comment"># Always exactly 1,000,000 ✓</span></code></pre>

            <h2>Real-World Race Condition: Double-Spending</h2>
<pre><code><span class="token-keyword">import</span> threading
<span class="token-keyword">import</span> time

<span class="token-keyword">class</span> <span class="token-class">BankAccount</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self, balance):
        self.balance = balance
        self.lock = threading.Lock()
    
    <span class="token-keyword">def</span> <span class="token-function">unsafe_withdraw</span>(self, amount):
        <span class="token-string">"""BUGGY: Race condition between check and withdrawal."""</span>
        <span class="token-keyword">if</span> self.balance >= amount:  <span class="token-comment"># CHECK</span>
            time.sleep(<span class="token-number">0.001</span>)  <span class="token-comment"># Simulates some processing time</span>
            self.balance -= amount  <span class="token-comment"># ACT — balance might have changed!</span>
            <span class="token-keyword">return</span> <span class="token-keyword">True</span>
        <span class="token-keyword">return</span> <span class="token-keyword">False</span>
    
    <span class="token-keyword">def</span> <span class="token-function">safe_withdraw</span>(self, amount):
        <span class="token-string">"""FIXED: Lock makes check-and-act atomic."""</span>
        <span class="token-keyword">with</span> self.lock:
            <span class="token-keyword">if</span> self.balance >= amount:
                self.balance -= amount
                <span class="token-keyword">return</span> <span class="token-keyword">True</span>
            <span class="token-keyword">return</span> <span class="token-keyword">False</span>

<span class="token-comment"># Demonstrate the bug</span>
account = BankAccount(<span class="token-number">1000</span>)
threads = [threading.Thread(target=account.unsafe_withdraw, args=(<span class="token-number">800</span>,)) <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">5</span>)]
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.start()
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.join()
print(<span class="token-string">f"Balance: ${account.balance}"</span>)  <span class="token-comment"># Could be NEGATIVE!</span></code></pre>

            <div class="industry-box">
                <h4>🏢 Famous Race Condition Bugs</h4>
                <ul>
                    <li><strong>Therac-25 (1985-87)</strong> — Radiation therapy machine. Race condition caused patients to receive 100x lethal radiation doses. 3 deaths.</li>
                    <li><strong>Northeast Blackout (2003)</strong> — Race condition in alarm software prevented operators from seeing cascading failures. 55 million people lost power.</li>
                    <li><strong>Mars Pathfinder (1997)</strong> — Priority inversion race condition caused the spacecraft to keep resetting on Mars.</li>
                    <li><strong>Every fintech startup</strong> — Double-charging, double-crediting from race conditions in payment processing.</li>
                </ul>
            </div>""",
        "summary": """<ul>
                    <li>A race condition occurs when the outcome depends on thread timing — unpredictable by nature</li>
                    <li>Happens when threads share data without synchronization, and at least one writes</li>
                    <li>counter += 1 is NOT atomic — it's read, modify, write (three steps)</li>
                    <li>Fix: use locks (mutex), atomic operations, or avoid shared mutable state entirely</li>
                    <li>Check-then-act is the most common pattern that causes race conditions</li>
                    <li>Race conditions can cause data corruption, security vulnerabilities, and even deaths (Therac-25)</li>
                </ul>""",
        "mental_model": """Thread A:  READ(100) ──────────── ADD(101) ── WRITE(101)
Thread B:        READ(100) ── ADD(101) ── WRITE(101)
                 ↑ Both read 100, both write 101
                 ↑ We LOST one increment!

Fix with lock:
Thread A:  [LOCK] READ(100) ADD(101) WRITE(101) [UNLOCK]
Thread B:              (waiting...)              [LOCK] READ(101) ADD(102) WRITE(102) [UNLOCK]
                                                 ↑ Reads AFTER A's write — correct!""",
        "mistakes": """<ul>
                    <li><strong>Thinking "it works on my machine"</strong> — Race conditions are timing-dependent. They might not show up in testing but explode in production under load.</li>
                    <li><strong>Only protecting writes, not reads</strong> — If you read without a lock while another thread writes, you can see torn/inconsistent data.</li>
                    <li><strong>Using time.sleep() as synchronization</strong> — Sleeping doesn't guarantee order. Never rely on timing for correctness.</li>
                    <li><strong>Locking too little</strong> — Protecting individual operations but not the compound operation (check-then-act needs both under one lock).</li>
                </ul>""",
        "exercise": """<ol>
                    <li>Create a shared list. Have 5 threads each append 1000 items. Check the final length (it might be less than 5000!)</li>
                    <li>Fix it with a lock and verify it's always exactly 5000</li>
                    <li>Create a "bank transfer" function that debits one account and credits another. Show how it can lose money without locks</li>
                    <li>Fix the bank transfer to be atomic (both operations inside one lock)</li>
                </ol>""",
        "prev_link": "02-context-switching.html", "prev_title": "Context Switching",
        "next_link": "04-critical-sections.html", "next_title": "Critical Sections"
    },
    {
        "num": "04", "file": "04-critical-sections.html",
        "title": "Critical Sections",
        "subtitle": "The 'danger zones' in your code where only one thread should be allowed at a time. Get this wrong and you get race conditions; get it right and your concurrent code is safe.",
        "tags": ['beginner', 'concept', 'code'],
        "analogy_title": "🏠 Daily-Life Analogy: The Bathroom",
        "analogy": """<p>A <strong>critical section</strong> is like a <strong>single-occupancy bathroom</strong> in an office:</p>
                <ul>
                    <li>Only <strong>one person</strong> can be inside at a time</li>
                    <li>When you go in, you <strong>lock the door</strong></li>
                    <li>Others must <strong>wait outside</strong> until you're done</li>
                    <li>When you leave, you <strong>unlock the door</strong></li>
                </ul>
                <p>The bathroom itself is the "critical section" — the code that accesses shared data. The lock on the door is the mutex/lock. The person inside is the thread currently executing.</p>
                <p>If two people could be in the bathroom at the same time... chaos. Same with code accessing shared data.</p>""",
        "content": """
            <h2>What Is a Critical Section?</h2>
            <p>A <strong>critical section</strong> is a piece of code that accesses a <strong>shared resource</strong> (variable, file, database connection, etc.) that must not be accessed by more than one thread at the same time.</p>
            <p>Formally: A critical section is a code segment where <strong>shared mutable state</strong> is read or modified, and concurrent access would lead to a race condition.</p>

            <h3>Identifying Critical Sections</h3>
            <p>Ask yourself: "If two threads ran this code at the EXACT same time, could something go wrong?" If yes — it's a critical section.</p>

<pre><code><span class="token-keyword">import</span> threading

<span class="token-comment"># Shared state</span>
balance = <span class="token-number">1000</span>
transaction_log = []

<span class="token-keyword">def</span> <span class="token-function">transfer</span>(amount, to_account):
    <span class="token-keyword">global</span> balance
    
    <span class="token-comment"># ─── CRITICAL SECTION START ───</span>
    <span class="token-keyword">if</span> balance >= amount:          <span class="token-comment"># Read shared state</span>
        balance -= amount            <span class="token-comment"># Modify shared state</span>
        to_account += amount         <span class="token-comment"># Modify shared state</span>
        transaction_log.append(      <span class="token-comment"># Modify shared state</span>
            <span class="token-string">f"Transferred {amount}"</span>
        )
    <span class="token-comment"># ─── CRITICAL SECTION END ───</span>
    
    <span class="token-comment"># This is NOT a critical section (local variable only)</span>
    receipt = <span class="token-string">f"Receipt: {amount} transferred"</span>
    print(receipt)</code></pre>

            <h2>The Four Requirements for Safe Critical Sections</h2>
            <p>For a critical section solution to be correct, it must satisfy:</p>
            <table class="comparison-table">
                <thead><tr><th>Requirement</th><th>Meaning</th><th>Analogy</th></tr></thead>
                <tbody>
                    <tr><td><strong>Mutual Exclusion</strong></td><td>Only one thread in the critical section at a time</td><td>Only one person in the bathroom</td></tr>
                    <tr><td><strong>Progress</strong></td><td>If no one is in the CS, a waiting thread can enter</td><td>Empty bathroom → next person can go in</td></tr>
                    <tr><td><strong>Bounded Waiting</strong></td><td>No thread waits forever (no starvation)</td><td>Everyone gets a turn eventually</td></tr>
                    <tr><td><strong>No assumptions about speed</strong></td><td>Works regardless of how fast each thread runs</td><td>Works whether someone takes 1 min or 30 min</td></tr>
                </tbody>
            </table>

            <h2>Implementing Critical Sections in Python</h2>
<pre><code><span class="token-keyword">import</span> threading

<span class="token-keyword">class</span> <span class="token-class">ThreadSafeCounter</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self):
        self._count = <span class="token-number">0</span>
        self._lock = threading.Lock()
    
    <span class="token-keyword">def</span> <span class="token-function">increment</span>(self):
        <span class="token-comment"># Enter critical section</span>
        self._lock.acquire()
        <span class="token-keyword">try</span>:
            self._count += <span class="token-number">1</span>  <span class="token-comment"># Only one thread here at a time</span>
        <span class="token-keyword">finally</span>:
            self._lock.release()  <span class="token-comment"># ALWAYS release, even if exception</span>
    
    <span class="token-keyword">def</span> <span class="token-function">increment_pythonic</span>(self):
        <span class="token-comment"># Better: context manager handles acquire/release</span>
        <span class="token-keyword">with</span> self._lock:  <span class="token-comment"># ← Critical section is inside this block</span>
            self._count += <span class="token-number">1</span>
    
    <span class="token-keyword">def</span> <span class="token-function">get</span>(self):
        <span class="token-keyword">with</span> self._lock:  <span class="token-comment"># Even reads should be protected!</span>
            <span class="token-keyword">return</span> self._count

<span class="token-comment"># Usage</span>
counter = ThreadSafeCounter()
threads = [threading.Thread(target=<span class="token-keyword">lambda</span>: [counter.increment() <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10000</span>)]) <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10</span>)]
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.start()
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.join()
print(<span class="token-string">f"Count: {counter.get()}"</span>)  <span class="token-comment"># Always 100,000 ✓</span></code></pre>

            <h2>Critical Section Size Matters</h2>
            <div class="callout callout-warning">
                <div class="callout-title">⚠️ Keep Critical Sections SHORT</div>
                <p>The longer a thread holds a lock (stays in the critical section), the longer other threads must wait. Long critical sections destroy parallelism.</p>
            </div>

<pre><code><span class="token-comment"># BAD: Too much inside the critical section</span>
<span class="token-keyword">def</span> <span class="token-function">process_bad</span>(data):
    <span class="token-keyword">with</span> lock:
        result = expensive_computation(data)  <span class="token-comment"># 100ms — others wait!</span>
        shared_list.append(result)             <span class="token-comment"># Only THIS needs the lock</span>

<span class="token-comment"># GOOD: Minimize critical section</span>
<span class="token-keyword">def</span> <span class="token-function">process_good</span>(data):
    result = expensive_computation(data)  <span class="token-comment"># 100ms — NO lock needed (local work)</span>
    <span class="token-keyword">with</span> lock:
        shared_list.append(result)         <span class="token-comment"># Only 1μs under lock</span></code></pre>

            <div class="industry-box">
                <h4>🏢 Industry Practice</h4>
                <ul>
                    <li><strong>Linux kernel</strong> — Uses "Big Kernel Lock" historically (one giant critical section = slow). Modern kernels use fine-grained locks (many small critical sections = fast).</li>
                    <li><strong>Database engines</strong> — Row-level locking vs table-level locking. Smaller critical sections = more concurrency.</li>
                    <li><strong>Java ConcurrentHashMap</strong> — Instead of locking the whole map, locks individual buckets (16+ separate critical sections).</li>
                </ul>
            </div>""",
        "summary": """<ul>
                    <li>A critical section is code that accesses shared mutable state</li>
                    <li>Only one thread may be in a critical section at a time (mutual exclusion)</li>
                    <li>Use locks (mutex) to protect critical sections</li>
                    <li>Always use try/finally or context managers (with lock:) to ensure release</li>
                    <li>Keep critical sections as SHORT as possible — long locks kill parallelism</li>
                    <li>Move expensive computation OUTSIDE the critical section</li>
                </ul>""",
        "mental_model": """Thread A: ──── [LOCK] ─── critical section ─── [UNLOCK] ────────
Thread B: ──── (waiting...) ──────────────────── [LOCK] ─── CS ─── [UNLOCK]
Thread C: ──── (waiting...) ──────────────────── (waiting...) ──── [LOCK]...

RULE: Keep the CS small!
BAD:  [LOCK] ──── 100ms of work ──── [UNLOCK]  (everyone waits 100ms)
GOOD: ── 100ms work ── [LOCK] 1μs [UNLOCK]     (minimal waiting)""",
        "mistakes": """<ul>
                    <li><strong>Forgetting to release the lock</strong> — If an exception occurs between acquire() and release(), the lock is held forever (deadlock). Always use with lock: or try/finally.</li>
                    <li><strong>Making critical sections too large</strong> — Putting expensive computation inside the lock. Only protect shared state access.</li>
                    <li><strong>Not protecting read operations</strong> — If another thread writes while you read, you see inconsistent data. Reads of shared state need locks too.</li>
                    <li><strong>Using different locks for the same data</strong> — All threads must use THE SAME lock instance to protect the same data.</li>
                </ul>""",
        "exercise": """<ol>
                    <li>Write a thread-safe queue (push/pop) using a list and a lock</li>
                    <li>Have 5 producer threads and 5 consumer threads use it simultaneously</li>
                    <li>First write it WITHOUT a lock — show it crashes or corrupts</li>
                    <li>Then add the lock — show it works perfectly</li>
                    <li>Measure: what percentage of time do threads spend waiting for the lock vs doing useful work?</li>
                </ol>""",
        "prev_link": "03-race-conditions.html", "prev_title": "Race Conditions",
        "next_link": "05-mutex-locks.html", "next_title": "Mutex & Locks"
    },
    {
        "num": "05", "file": "05-mutex-locks.html",
        "title": "Mutual Exclusion (Mutex &amp; Locks)",
        "subtitle": "The fundamental tool for protecting shared data. A mutex is a lock that ensures only one thread can access a resource at a time — the most important primitive in concurrent programming.",
        "tags": ['beginner', 'concept', 'code'],
        "analogy_title": "🏠 Daily-Life Analogy: The Hotel Room Key",
        "analogy": """<p>A mutex is like a <strong>hotel room with one key</strong>:</p>
                <ul>
                    <li>Only the person <strong>holding the key</strong> can enter the room</li>
                    <li>Everyone else must <strong>wait at the front desk</strong> until the key is returned</li>
                    <li>When you're done, you <strong>return the key</strong> so the next person can enter</li>
                    <li>If you forget to return the key (forget to unlock), <strong>nobody else can ever enter</strong> — that's a deadlock</li>
                </ul>
                <p><strong>Mutex</strong> = MUTual EXclusion. Only one thread at a time. That's the entire concept.</p>""",
        "content": """
            <h2>What Is a Mutex?</h2>
            <p>A <strong>mutex (mutual exclusion lock)</strong> is a synchronization primitive that:</p>
            <ul>
                <li>Has two states: <strong>locked</strong> (held by a thread) or <strong>unlocked</strong> (available)</li>
                <li>Only the thread that <strong>locked</strong> it can <strong>unlock</strong> it</li>
                <li>Other threads calling lock() will <strong>block</strong> (sleep) until the mutex becomes available</li>
            </ul>

            <h3>The Three Operations</h3>
            <table class="comparison-table">
                <thead><tr><th>Operation</th><th>What Happens</th><th>If Already Locked?</th></tr></thead>
                <tbody>
                    <tr><td><code>lock()</code> / <code>acquire()</code></td><td>Take ownership of the mutex</td><td>Thread blocks (waits/sleeps)</td></tr>
                    <tr><td><code>unlock()</code> / <code>release()</code></td><td>Release ownership</td><td>N/A — only owner can unlock</td></tr>
                    <tr><td><code>try_lock()</code></td><td>Try to lock, return immediately</td><td>Returns False (doesn't block)</td></tr>
                </tbody>
            </table>

            <h2>Python Implementation</h2>
<pre><code><span class="token-keyword">import</span> threading
<span class="token-keyword">import</span> time

<span class="token-comment"># === Basic Mutex Usage ===</span>
mutex = threading.Lock()
shared_data = {<span class="token-string">"count"</span>: <span class="token-number">0</span>, <span class="token-string">"items"</span>: []}

<span class="token-keyword">def</span> <span class="token-function">safe_update</span>(thread_id):
    <span class="token-keyword">for</span> i <span class="token-keyword">in</span> range(<span class="token-number">1000</span>):
        <span class="token-keyword">with</span> mutex:  <span class="token-comment"># Acquires on enter, releases on exit (even if exception)</span>
            shared_data[<span class="token-string">"count"</span>] += <span class="token-number">1</span>
            shared_data[<span class="token-string">"items"</span>].append(<span class="token-string">f"{thread_id}-{i}"</span>)

<span class="token-comment"># === Reentrant Lock (RLock) ===</span>
<span class="token-comment"># A regular Lock will DEADLOCK if the same thread tries to acquire it twice</span>
<span class="token-comment"># RLock allows the same thread to acquire multiple times (must release same number)</span>

rlock = threading.RLock()

<span class="token-keyword">def</span> <span class="token-function">outer</span>():
    <span class="token-keyword">with</span> rlock:
        print(<span class="token-string">"Outer acquired"</span>)
        inner()  <span class="token-comment"># This would DEADLOCK with a regular Lock!</span>

<span class="token-keyword">def</span> <span class="token-function">inner</span>():
    <span class="token-keyword">with</span> rlock:  <span class="token-comment"># Same thread re-acquires — OK with RLock</span>
        print(<span class="token-string">"Inner acquired"</span>)

<span class="token-comment"># === Try-Lock (Non-blocking) ===</span>
<span class="token-keyword">def</span> <span class="token-function">try_work</span>():
    acquired = mutex.acquire(blocking=<span class="token-keyword">False</span>)  <span class="token-comment"># Don't wait if busy</span>
    <span class="token-keyword">if</span> acquired:
        <span class="token-keyword">try</span>:
            <span class="token-comment"># Do work with shared resource</span>
            shared_data[<span class="token-string">"count"</span>] += <span class="token-number">1</span>
        <span class="token-keyword">finally</span>:
            mutex.release()
    <span class="token-keyword">else</span>:
        print(<span class="token-string">"Busy — will try again later"</span>)

<span class="token-comment"># === Timed Lock (wait with timeout) ===</span>
<span class="token-keyword">def</span> <span class="token-function">timed_work</span>():
    acquired = mutex.acquire(timeout=<span class="token-number">2.0</span>)  <span class="token-comment"># Wait max 2 seconds</span>
    <span class="token-keyword">if</span> acquired:
        <span class="token-keyword">try</span>:
            shared_data[<span class="token-string">"count"</span>] += <span class="token-number">1</span>
        <span class="token-keyword">finally</span>:
            mutex.release()
    <span class="token-keyword">else</span>:
        print(<span class="token-string">"Timeout! Could not acquire lock in 2s"</span>)</code></pre>

            <h2>Lock vs RLock vs Condition</h2>
            <table class="comparison-table">
                <thead><tr><th>Type</th><th>Re-entrant?</th><th>Use Case</th></tr></thead>
                <tbody>
                    <tr><td><code>threading.Lock()</code></td><td>No — deadlocks if same thread acquires twice</td><td>Simple mutual exclusion</td></tr>
                    <tr><td><code>threading.RLock()</code></td><td>Yes — same thread can acquire multiple times</td><td>Recursive/nested locking</td></tr>
                    <tr><td><code>threading.Condition()</code></td><td>Built on Lock/RLock</td><td>Wait for a condition to become true</td></tr>
                </tbody>
            </table>

            <h2>Lock Granularity: Fine vs Coarse</h2>
<pre><code><span class="token-comment"># COARSE-GRAINED: One lock for everything (simple but slow)</span>
<span class="token-keyword">class</span> <span class="token-class">CoarseGrainedDB</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self):
        self.lock = threading.Lock()
        self.users = {}
        self.orders = {}
    
    <span class="token-keyword">def</span> <span class="token-function">update_user</span>(self, user_id, data):
        <span class="token-keyword">with</span> self.lock:  <span class="token-comment"># Blocks ALL operations (even unrelated ones)</span>
            self.users[user_id] = data
    
    <span class="token-keyword">def</span> <span class="token-function">update_order</span>(self, order_id, data):
        <span class="token-keyword">with</span> self.lock:  <span class="token-comment"># User update blocks order update!</span>
            self.orders[order_id] = data

<span class="token-comment"># FINE-GRAINED: Separate locks for separate data (complex but fast)</span>
<span class="token-keyword">class</span> <span class="token-class">FineGrainedDB</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self):
        self.user_lock = threading.Lock()
        self.order_lock = threading.Lock()
        self.users = {}
        self.orders = {}
    
    <span class="token-keyword">def</span> <span class="token-function">update_user</span>(self, user_id, data):
        <span class="token-keyword">with</span> self.user_lock:  <span class="token-comment"># Only blocks other user operations</span>
            self.users[user_id] = data
    
    <span class="token-keyword">def</span> <span class="token-function">update_order</span>(self, order_id, data):
        <span class="token-keyword">with</span> self.order_lock:  <span class="token-comment"># Users and orders are independent!</span>
            self.orders[order_id] = data</code></pre>

            <div class="industry-box">
                <h4>🏢 Industry Usage</h4>
                <ul>
                    <li><strong>PostgreSQL</strong> — Uses lwlocks (lightweight locks) and spinlocks for different internal structures</li>
                    <li><strong>Linux kernel</strong> — Has mutex_lock(), spin_lock(), read_lock(), write_lock() for different scenarios</li>
                    <li><strong>Java's synchronized keyword</strong> — Built-in mutex on every object (monitor lock)</li>
                    <li><strong>Go's sync.Mutex</strong> — Simple Lock()/Unlock() with no re-entrancy (keeps it simple)</li>
                    <li><strong>Rust's Mutex&lt;T&gt;</strong> — Compiler FORCES you to acquire the lock before accessing data. Cannot forget!</li>
                </ul>
            </div>""",
        "summary": """<ul>
                    <li>A mutex ensures only one thread can access a shared resource at a time</li>
                    <li>Always use context managers (with lock:) or try/finally to prevent forgetting to unlock</li>
                    <li>RLock allows the same thread to acquire multiple times (for recursive functions)</li>
                    <li>Fine-grained locks (one per resource) allow more parallelism than coarse-grained (one for all)</li>
                    <li>try_lock() is non-blocking — useful when you can do something else instead of waiting</li>
                    <li>Lock contention (many threads waiting) is the #1 performance killer in concurrent systems</li>
                </ul>""",
        "mental_model": """MUTEX STATE MACHINE:
    ┌──────────┐   acquire()    ┌──────────┐
    │ UNLOCKED │ ────────────→  │  LOCKED  │
    │          │ ←────────────  │ (by T1)  │
    └──────────┘   release()    └──────────┘
                                     │
                          Thread T2 calls acquire()
                                     ↓
                              T2 BLOCKS (sleeps)
                              until T1 releases

GRANULARITY SPECTRUM:
    One lock for everything ←──────────────→ One lock per data item
    (simple, slow)                           (complex, fast)
    PostgreSQL table lock                    PostgreSQL row lock""",
        "mistakes": """<ul>
                    <li><strong>Forgetting to release</strong> — If an exception happens, the lock stays held forever. ALWAYS use with lock: or try/finally.</li>
                    <li><strong>Acquiring a Lock twice from the same thread</strong> — This deadlocks! Use RLock if you need re-entrancy.</li>
                    <li><strong>Holding locks during I/O</strong> — Lock, then network call, then unlock = other threads blocked for 100ms+. Do I/O outside the lock.</li>
                    <li><strong>Wrong lock instance</strong> — Each thread creating its own lock object. All threads must share the SAME lock instance.</li>
                </ul>""",
        "exercise": """<ol>
                    <li>Implement a thread-safe bounded buffer (max 10 items) with a Lock</li>
                    <li>Add blocking behavior: producer waits when full, consumer waits when empty (hint: use Condition variable)</li>
                    <li>Compare performance: coarse-grained vs fine-grained locking with a shared dictionary (separate locks for different key ranges)</li>
                    <li>Demonstrate RLock: write a recursive function that needs to re-acquire the same lock</li>
                </ol>""",
        "prev_link": "04-critical-sections.html", "prev_title": "Critical Sections",
        "next_link": "06-deadlocks.html", "next_title": "Deadlocks"
    },
]

def generate_html(topic):
    """Generate full HTML for a topic."""
    tags_html = ""
    for tag in topic["tags"]:
        tags_html += f'                    <span class="tag tag-{tag}">{tag.title()}</span>\n'
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic["title"]} - System Design Course</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="sidebar-overlay"></div>
    <aside class="sidebar">
        <div class="sidebar-header"><h2>System Design</h2><div class="subtitle">Beginner → Advanced • 68 Topics</div></div>
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
            <button class="hamburger">☰</button>
            <div class="breadcrumb"><a href="index.html">System Design</a><span>/</span> {topic["title"]}</div>
        </div>
        <div class="topbar-right"><button class="theme-toggle">🌙</button></div>
    </header>

    <main class="main-content">
        <div class="content-wrapper">

            <div class="hero">
                <h1>{topic["title"]}</h1>
                <p class="subtitle">{topic["subtitle"]}</p>
                <div class="tag-row">
{tags_html}                </div>
            </div>

            <div class="analogy-box">
                <div class="analogy-title">{topic["analogy_title"]}</div>
                {topic["analogy"]}
            </div>

            {topic["content"]}

            <div class="summary-box">
                <h3>📝 Summary</h3>
                {topic["summary"]}
            </div>

            <div class="mental-model">
                <h3>🧠 Mental Model</h3>
                <div class="model-visual">{topic["mental_model"]}</div>
            </div>

            <div class="mistakes-box">
                <h3>❌ Common Beginner Mistakes</h3>
                {topic["mistakes"]}
            </div>

            <div class="exercise-box">
                <h3>🏋️ Hands-On Exercise</h3>
                {topic["exercise"]}
            </div>

            <nav class="page-nav">
                <a href="{topic["prev_link"]}" class="prev">{topic["prev_title"]}</a>
                <a href="{topic["next_link"]}" class="next">{topic["next_title"]}</a>
            </nav>

        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>'''


if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    for topic in TOPICS:
        filepath = os.path.join(output_dir, topic["file"])
        if os.path.exists(filepath):
            print(f"  SKIP (exists): {topic['file']}")
            continue
        html = generate_html(topic)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Created: {topic['file']}")
    
    print(f"\nGenerated {len(TOPICS)} topic files.")
