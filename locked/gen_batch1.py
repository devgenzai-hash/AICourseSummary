"""Generate topics 03-08: Concurrency Foundations (remaining)"""
import sys
sys.path.insert(0, '.')
from gen_template import write_topic

# Topic 03
write_topic("03-race-conditions.html",
    title="Race Conditions",
    subtitle="When two threads try to change the same data at the same time and chaos ensues — the #1 most common concurrency bug.",
    tags=["beginner","concept","code"],
    analogy_title="Two People, One Bank Account",
    analogy="""<p>Imagine you and your partner both have debit cards for the same bank account with $1,000. At the exact same moment:</p>
<ul><li><strong>You</strong> check balance: $1,000 — withdraw $800</li><li><strong>Partner</strong> checks balance: $1,000 — withdraw $700</li></ul>
<p>Both see $1,000, both think the withdrawal is safe. Result: <strong>$1,500 withdrawn from a $1,000 account</strong>. The bank loses money because two operations "raced" against each other.</p>""",
    content="""
            <h2>What Is a Race Condition?</h2>
            <p>A <strong>race condition</strong> occurs when program behavior depends on the <strong>relative timing</strong> of two or more threads. The result is different depending on who "wins the race."</p>
            <p>Technical definition: two or more threads access shared data, at least one writes, and there's no synchronization controlling order.</p>

            <h3>The Classic Example: Counter Increment</h3>
            <p><code>counter += 1</code> looks atomic but is actually THREE steps: READ → ADD → WRITE</p>

<pre><code><span class="token-keyword">import</span> threading

counter = <span class="token-number">0</span>

<span class="token-keyword">def</span> <span class="token-function">increment</span>():
    <span class="token-keyword">global</span> counter
    <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">100_000</span>):
        counter += <span class="token-number">1</span>  <span class="token-comment"># NOT atomic! READ then ADD then WRITE</span>

<span class="token-comment"># Launch 10 threads all incrementing the same counter</span>
threads = [threading.Thread(target=increment) <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10</span>)]
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.start()
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.join()

print(<span class="token-string">f"Expected: 1,000,000"</span>)
print(<span class="token-string">f"Actual:   {counter}"</span>)  <span class="token-comment"># Something LESS! e.g. 834,291</span></code></pre>

            <div class="callout callout-danger">
                <div class="callout-title">Why It Breaks</div>
                <p>Thread A reads counter=100, Thread B reads counter=100. Both add 1, both write 101. We lost an increment! This happens thousands of times during a run.</p>
            </div>

            <h2>Types of Race Conditions</h2>
            <table class="comparison-table">
                <thead><tr><th>Type</th><th>Description</th><th>Example</th></tr></thead>
                <tbody>
                    <tr><td><strong>Check-then-act</strong></td><td>Check a condition then act on it — but condition changes in between</td><td>if file_exists then read_file (deleted between check and read)</td></tr>
                    <tr><td><strong>Read-modify-write</strong></td><td>Read a value, change it, write back — another thread modifies in between</td><td>counter += 1</td></tr>
                    <tr><td><strong>Compound operations</strong></td><td>Multiple ops that need to be atomic but are not</td><td>Transfer: debit A then credit B (crash between = money lost)</td></tr>
                </tbody>
            </table>

            <h2>The Fix: Synchronization</h2>
<pre><code><span class="token-keyword">import</span> threading

counter = <span class="token-number">0</span>
lock = threading.Lock()

<span class="token-keyword">def</span> <span class="token-function">safe_increment</span>():
    <span class="token-keyword">global</span> counter
    <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">100_000</span>):
        <span class="token-keyword">with</span> lock:
            counter += <span class="token-number">1</span>

threads = [threading.Thread(target=safe_increment) <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10</span>)]
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.start()
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.join()
print(<span class="token-string">f"Result: {counter}"</span>)  <span class="token-comment"># Always exactly 1,000,000</span></code></pre>

            <h2>Real-World Race Condition: Double-Spending</h2>
<pre><code><span class="token-keyword">import</span> threading, time

<span class="token-keyword">class</span> <span class="token-class">BankAccount</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self, balance):
        self.balance = balance
        self.lock = threading.Lock()

    <span class="token-keyword">def</span> <span class="token-function">unsafe_withdraw</span>(self, amount):
        <span class="token-keyword">if</span> self.balance >= amount:   <span class="token-comment"># CHECK</span>
            time.sleep(<span class="token-number">0.001</span>)         <span class="token-comment"># Simulates processing</span>
            self.balance -= amount    <span class="token-comment"># ACT — balance may have changed!</span>
            <span class="token-keyword">return</span> <span class="token-keyword">True</span>
        <span class="token-keyword">return</span> <span class="token-keyword">False</span>

    <span class="token-keyword">def</span> <span class="token-function">safe_withdraw</span>(self, amount):
        <span class="token-keyword">with</span> self.lock:
            <span class="token-keyword">if</span> self.balance >= amount:
                self.balance -= amount
                <span class="token-keyword">return</span> <span class="token-keyword">True</span>
            <span class="token-keyword">return</span> <span class="token-keyword">False</span>

account = BankAccount(<span class="token-number">1000</span>)
threads = [threading.Thread(target=account.unsafe_withdraw, args=(<span class="token-number">800</span>,)) <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">5</span>)]
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.start()
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.join()
print(<span class="token-string">f"Balance: ${account.balance}"</span>)  <span class="token-comment"># Could be NEGATIVE!</span></code></pre>

            <div class="industry-box">
                <h4>Famous Race Condition Bugs</h4>
                <ul>
                    <li><strong>Therac-25 (1985-87)</strong> — Radiation machine race condition caused 100x lethal doses. 3 deaths.</li>
                    <li><strong>Northeast Blackout (2003)</strong> — Race condition in alarm software hid cascading failures. 55 million lost power.</li>
                    <li><strong>Mars Pathfinder (1997)</strong> — Priority inversion race caused spacecraft resets on Mars.</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Race condition: outcome depends on thread timing — unpredictable</li>
<li>Happens when threads share data without synchronization and at least one writes</li>
<li>counter += 1 is NOT atomic — it is read, modify, write (three steps)</li>
<li>Fix: use locks, atomic operations, or avoid shared mutable state</li>
<li>Check-then-act is the most common race condition pattern</li>
</ul>""",
    mental_model="""Thread A:  READ(100) ────────── ADD(101) ── WRITE(101)
Thread B:        READ(100) ── ADD(101) ── WRITE(101)
                 ^ Both read 100, both write 101 = LOST update!

WITH LOCK:
Thread A:  [LOCK] READ(100) ADD(101) WRITE(101) [UNLOCK]
Thread B:              (waiting...)              [LOCK] READ(101)...""",
    mistakes="""<ul>
<li><strong>"It works on my machine"</strong> — Race conditions are timing-dependent; may not show in testing but explode in production.</li>
<li><strong>Only protecting writes</strong> — Reads of shared state need locks too.</li>
<li><strong>Using sleep() as synchronization</strong> — Never rely on timing for correctness.</li>
<li><strong>Locking too little</strong> — check-then-act needs BOTH under one lock.</li>
</ul>""",
    exercise="""<ol>
<li>Create a shared list. Have 5 threads each append 1000 items. Check the final length.</li>
<li>Fix it with a lock and verify it is always exactly 5000.</li>
<li>Create a bank transfer that debits one account and credits another. Show money loss without locks.</li>
<li>Fix it to be atomic (both operations inside one lock).</li>
</ol>""",
    prev_link="02-context-switching.html", prev_title="Context Switching",
    next_link="04-critical-sections.html", next_title="Critical Sections"
)

# Topic 04
write_topic("04-critical-sections.html",
    title="Critical Sections",
    subtitle="The danger zones in your code where only one thread should be allowed at a time. Master this and your concurrent code is safe.",
    tags=["beginner","concept","code"],
    analogy_title="The Single-Occupancy Bathroom",
    analogy="""<p>A critical section is like a <strong>single-occupancy bathroom</strong> in an office:</p>
<ul><li>Only <strong>one person</strong> can be inside at a time</li>
<li>When you go in, you <strong>lock the door</strong></li>
<li>Others must <strong>wait outside</strong></li>
<li>When you leave, you <strong>unlock</strong></li></ul>
<p>The bathroom is the critical section. The lock on the door is the mutex. If two people could be in at the same time — chaos.</p>""",
    content="""
            <h2>What Is a Critical Section?</h2>
            <p>A <strong>critical section</strong> is a piece of code that accesses a <strong>shared resource</strong> that must not be accessed by more than one thread at a time.</p>

            <h3>Identifying Critical Sections</h3>
            <p>Ask: "If two threads ran this code at the EXACT same time, could something go wrong?" If yes — it is a critical section.</p>

<pre><code><span class="token-keyword">import</span> threading

balance = <span class="token-number">1000</span>
transaction_log = []

<span class="token-keyword">def</span> <span class="token-function">transfer</span>(amount):
    <span class="token-keyword">global</span> balance
    <span class="token-comment"># --- CRITICAL SECTION START ---</span>
    <span class="token-keyword">if</span> balance >= amount:
        balance -= amount
        transaction_log.append(<span class="token-string">f"Transferred {amount}"</span>)
    <span class="token-comment"># --- CRITICAL SECTION END ---</span>

    <span class="token-comment"># This is NOT critical (local variable only)</span>
    receipt = <span class="token-string">f"Receipt: {amount}"</span>
    print(receipt)</code></pre>

            <h2>Four Requirements for Safe Critical Sections</h2>
            <table class="comparison-table">
                <thead><tr><th>Requirement</th><th>Meaning</th><th>Analogy</th></tr></thead>
                <tbody>
                    <tr><td><strong>Mutual Exclusion</strong></td><td>Only one thread in CS at a time</td><td>One person in bathroom</td></tr>
                    <tr><td><strong>Progress</strong></td><td>If CS is empty, waiting thread can enter</td><td>Empty bathroom = next person goes in</td></tr>
                    <tr><td><strong>Bounded Waiting</strong></td><td>No thread waits forever</td><td>Everyone gets a turn eventually</td></tr>
                    <tr><td><strong>No speed assumptions</strong></td><td>Works regardless of thread speed</td><td>Works whether 1 min or 30 min</td></tr>
                </tbody>
            </table>

            <h2>Implementation in Python</h2>
<pre><code><span class="token-keyword">import</span> threading

<span class="token-keyword">class</span> <span class="token-class">ThreadSafeCounter</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self):
        self._count = <span class="token-number">0</span>
        self._lock = threading.Lock()

    <span class="token-keyword">def</span> <span class="token-function">increment</span>(self):
        <span class="token-keyword">with</span> self._lock:  <span class="token-comment"># Critical section</span>
            self._count += <span class="token-number">1</span>

    <span class="token-keyword">def</span> <span class="token-function">get</span>(self):
        <span class="token-keyword">with</span> self._lock:  <span class="token-comment"># Even reads need protection!</span>
            <span class="token-keyword">return</span> self._count

counter = ThreadSafeCounter()
threads = [threading.Thread(target=<span class="token-keyword">lambda</span>: [counter.increment() <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10000</span>)])
           <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10</span>)]
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.start()
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.join()
print(<span class="token-string">f"Count: {counter.get()}"</span>)  <span class="token-comment"># Always 100,000</span></code></pre>

            <h2>Critical Section Size Matters</h2>
            <div class="callout callout-warning">
                <div class="callout-title">Keep Critical Sections SHORT</div>
                <p>The longer a thread holds a lock, the longer others wait. Long critical sections destroy parallelism.</p>
            </div>

<pre><code><span class="token-comment"># BAD: Too much inside the critical section</span>
<span class="token-keyword">def</span> <span class="token-function">process_bad</span>(data):
    <span class="token-keyword">with</span> lock:
        result = expensive_computation(data)  <span class="token-comment"># 100ms others wait!</span>
        shared_list.append(result)

<span class="token-comment"># GOOD: Minimize critical section</span>
<span class="token-keyword">def</span> <span class="token-function">process_good</span>(data):
    result = expensive_computation(data)  <span class="token-comment"># No lock needed</span>
    <span class="token-keyword">with</span> lock:
        shared_list.append(result)  <span class="token-comment"># Only this needs the lock</span></code></pre>

            <div class="industry-box">
                <h4>Industry Practice</h4>
                <ul>
                    <li><strong>Linux kernel</strong> — Moved from Big Kernel Lock (one giant CS) to fine-grained locks (many small CS).</li>
                    <li><strong>Java ConcurrentHashMap</strong> — Locks individual buckets, not the whole map.</li>
                    <li><strong>Database engines</strong> — Row-level vs table-level locking. Smaller CS = more concurrency.</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>A critical section is code accessing shared mutable state</li>
<li>Only one thread may be in a critical section at a time (mutual exclusion)</li>
<li>Use locks to protect critical sections</li>
<li>Always use context managers (with lock:) to ensure release</li>
<li>Keep critical sections as SHORT as possible</li>
<li>Move expensive computation OUTSIDE the critical section</li>
</ul>""",
    mental_model="""Thread A: ---- [LOCK] --- critical section --- [UNLOCK] --------
Thread B: ---- (waiting...) ---------------------- [LOCK] --- CS --- [UNLOCK]

RULE: Keep the CS small!
BAD:  [LOCK] ---- 100ms work ---- [UNLOCK]   (everyone waits)
GOOD: -- 100ms work -- [LOCK] 1us [UNLOCK]   (minimal waiting)""",
    mistakes="""<ul>
<li><strong>Forgetting to release the lock</strong> — Always use with lock: or try/finally.</li>
<li><strong>Making critical sections too large</strong> — Only protect shared state access.</li>
<li><strong>Not protecting reads</strong> — Reads of shared data need locks too.</li>
<li><strong>Using different locks for the same data</strong> — All threads must use THE SAME lock.</li>
</ul>""",
    exercise="""<ol>
<li>Write a thread-safe queue (push/pop) using a list and a lock.</li>
<li>Have 5 producers and 5 consumers use it simultaneously.</li>
<li>First without lock — show corruption. Then with lock — show correctness.</li>
<li>Measure: what % of time do threads spend waiting vs doing useful work?</li>
</ol>""",
    prev_link="03-race-conditions.html", prev_title="Race Conditions",
    next_link="05-mutex-locks.html", next_title="Mutex & Locks"
)

# Topic 05
write_topic("05-mutex-locks.html",
    title="Mutex &amp; Locks",
    subtitle="The fundamental tool for protecting shared data. A mutex ensures only one thread can access a resource at a time.",
    tags=["beginner","concept","code"],
    analogy_title="The Hotel Room Key",
    analogy="""<p>A mutex is like a <strong>hotel room with one key</strong>:</p>
<ul><li>Only the person <strong>holding the key</strong> can enter</li>
<li>Everyone else <strong>waits at the front desk</strong></li>
<li>When done, you <strong>return the key</strong></li>
<li>Forget to return it? <strong>Nobody else can ever enter</strong> = deadlock</li></ul>
<p><strong>Mutex</strong> = MUTual EXclusion. Only one thread at a time.</p>""",
    content="""
            <h2>What Is a Mutex?</h2>
            <p>A <strong>mutex</strong> has two states: locked or unlocked. Only the locking thread can unlock it. Others block until available.</p>

            <table class="comparison-table">
                <thead><tr><th>Operation</th><th>What Happens</th><th>If Already Locked?</th></tr></thead>
                <tbody>
                    <tr><td><code>lock()/acquire()</code></td><td>Take ownership</td><td>Thread blocks (waits)</td></tr>
                    <tr><td><code>unlock()/release()</code></td><td>Release ownership</td><td>N/A</td></tr>
                    <tr><td><code>try_lock()</code></td><td>Try to lock, return immediately</td><td>Returns False</td></tr>
                </tbody>
            </table>

            <h2>Python Implementation</h2>
<pre><code><span class="token-keyword">import</span> threading

mutex = threading.Lock()
shared_data = {<span class="token-string">"count"</span>: <span class="token-number">0</span>}

<span class="token-keyword">def</span> <span class="token-function">safe_update</span>(thread_id):
    <span class="token-keyword">for</span> i <span class="token-keyword">in</span> range(<span class="token-number">1000</span>):
        <span class="token-keyword">with</span> mutex:  <span class="token-comment"># Acquires on enter, releases on exit</span>
            shared_data[<span class="token-string">"count"</span>] += <span class="token-number">1</span>

<span class="token-comment"># === Reentrant Lock (RLock) ===</span>
rlock = threading.RLock()

<span class="token-keyword">def</span> <span class="token-function">outer</span>():
    <span class="token-keyword">with</span> rlock:
        print(<span class="token-string">"Outer acquired"</span>)
        inner()  <span class="token-comment"># Would DEADLOCK with regular Lock!</span>

<span class="token-keyword">def</span> <span class="token-function">inner</span>():
    <span class="token-keyword">with</span> rlock:  <span class="token-comment"># Same thread re-acquires — OK with RLock</span>
        print(<span class="token-string">"Inner acquired"</span>)

<span class="token-comment"># === Try-Lock (Non-blocking) ===</span>
<span class="token-keyword">def</span> <span class="token-function">try_work</span>():
    acquired = mutex.acquire(blocking=<span class="token-keyword">False</span>)
    <span class="token-keyword">if</span> acquired:
        <span class="token-keyword">try</span>:
            shared_data[<span class="token-string">"count"</span>] += <span class="token-number">1</span>
        <span class="token-keyword">finally</span>:
            mutex.release()
    <span class="token-keyword">else</span>:
        print(<span class="token-string">"Busy, will try later"</span>)

<span class="token-comment"># === Timed Lock ===</span>
<span class="token-keyword">def</span> <span class="token-function">timed_work</span>():
    acquired = mutex.acquire(timeout=<span class="token-number">2.0</span>)
    <span class="token-keyword">if</span> acquired:
        <span class="token-keyword">try</span>:
            shared_data[<span class="token-string">"count"</span>] += <span class="token-number">1</span>
        <span class="token-keyword">finally</span>:
            mutex.release()
    <span class="token-keyword">else</span>:
        print(<span class="token-string">"Timeout! Could not acquire in 2s"</span>)</code></pre>

            <h2>Lock vs RLock vs Condition</h2>
            <table class="comparison-table">
                <thead><tr><th>Type</th><th>Re-entrant?</th><th>Use Case</th></tr></thead>
                <tbody>
                    <tr><td><code>Lock()</code></td><td>No — deadlocks if same thread acquires twice</td><td>Simple mutual exclusion</td></tr>
                    <tr><td><code>RLock()</code></td><td>Yes — same thread can acquire many times</td><td>Recursive/nested locking</td></tr>
                    <tr><td><code>Condition()</code></td><td>Built on Lock/RLock</td><td>Wait for a condition to be true</td></tr>
                </tbody>
            </table>

            <h2>Lock Granularity: Fine vs Coarse</h2>
<pre><code><span class="token-comment"># COARSE-GRAINED: One lock for everything (simple but slow)</span>
<span class="token-keyword">class</span> <span class="token-class">CoarseDB</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self):
        self.lock = threading.Lock()
        self.users = {}
        self.orders = {}

    <span class="token-keyword">def</span> <span class="token-function">update_user</span>(self, uid, data):
        <span class="token-keyword">with</span> self.lock:  <span class="token-comment"># Blocks ALL operations</span>
            self.users[uid] = data

<span class="token-comment"># FINE-GRAINED: Separate locks (complex but fast)</span>
<span class="token-keyword">class</span> <span class="token-class">FineDB</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self):
        self.user_lock = threading.Lock()
        self.order_lock = threading.Lock()
        self.users = {}
        self.orders = {}

    <span class="token-keyword">def</span> <span class="token-function">update_user</span>(self, uid, data):
        <span class="token-keyword">with</span> self.user_lock:  <span class="token-comment"># Only blocks user ops</span>
            self.users[uid] = data</code></pre>

            <div class="industry-box">
                <h4>Industry Usage</h4>
                <ul>
                    <li><strong>PostgreSQL</strong> — lwlocks and spinlocks for different structures</li>
                    <li><strong>Go sync.Mutex</strong> — Simple Lock()/Unlock() with no re-entrancy</li>
                    <li><strong>Rust Mutex&lt;T&gt;</strong> — Compiler FORCES you to acquire lock before accessing data</li>
                    <li><strong>Java synchronized</strong> — Built-in monitor lock on every object</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>A mutex ensures only one thread accesses a shared resource at a time</li>
<li>Always use context managers (with lock:) to prevent forgetting to unlock</li>
<li>RLock allows same thread to acquire multiple times (for recursive functions)</li>
<li>Fine-grained locks allow more parallelism than coarse-grained</li>
<li>Lock contention is the #1 performance killer in concurrent systems</li>
</ul>""",
    mental_model="""MUTEX STATE MACHINE:
    [UNLOCKED] --acquire()--> [LOCKED by T1]
    [LOCKED]   --release()--> [UNLOCKED]
    T2 calls acquire() while locked --> T2 BLOCKS until T1 releases

GRANULARITY:
    One lock for all  <--------->  One lock per item
    (simple, slow)                  (complex, fast)""",
    mistakes="""<ul>
<li><strong>Forgetting to release</strong> — Exception leaves lock held forever. Use with lock: always.</li>
<li><strong>Acquiring Lock twice (same thread)</strong> — Deadlocks! Use RLock for re-entrancy.</li>
<li><strong>Holding locks during I/O</strong> — Others blocked for network latency. Do I/O outside lock.</li>
<li><strong>Wrong lock instance</strong> — Each thread creating its own Lock object defeats the purpose.</li>
</ul>""",
    exercise="""<ol>
<li>Implement a thread-safe bounded buffer (max 10 items) with a Lock.</li>
<li>Add blocking: producer waits when full, consumer waits when empty (use Condition).</li>
<li>Compare coarse vs fine-grained locking with a shared dictionary.</li>
<li>Demonstrate RLock with a recursive function needing to re-acquire the same lock.</li>
</ol>""",
    prev_link="04-critical-sections.html", prev_title="Critical Sections",
    next_link="06-deadlocks.html", next_title="Deadlocks"
)

# Topic 06
write_topic("06-deadlocks.html",
    title="Deadlocks",
    subtitle="When two or more threads are stuck waiting for each other forever — like two cars meeting on a one-lane bridge, neither willing to back up.",
    tags=["beginner","concept","code"],
    analogy_title="The Dining Philosophers Problem",
    analogy="""<p>Imagine 5 philosophers sitting at a round table with 5 forks (one between each pair). To eat, each needs TWO forks.</p>
<ul><li>Everyone picks up their LEFT fork at the same time</li>
<li>Everyone waits for their RIGHT fork... which their neighbor is holding</li>
<li><strong>Nobody can eat. Nobody will put down their fork. Everyone starves.</strong></li></ul>
<p>This is a deadlock. Each person holds one resource and waits for another that someone else holds.</p>""",
    content="""
            <h2>What Is a Deadlock?</h2>
            <p>A <strong>deadlock</strong> occurs when two or more threads are each waiting for a resource held by one of the others. Nobody can proceed. The program hangs forever.</p>

            <h3>The Four Conditions (ALL must be true for deadlock)</h3>
            <table class="comparison-table">
                <thead><tr><th>Condition</th><th>Meaning</th><th>Break it to prevent deadlock</th></tr></thead>
                <tbody>
                    <tr><td><strong>Mutual Exclusion</strong></td><td>Resources can only be held by one thread</td><td>Use sharable resources where possible</td></tr>
                    <tr><td><strong>Hold and Wait</strong></td><td>Thread holds one resource while waiting for another</td><td>Acquire all resources at once or none</td></tr>
                    <tr><td><strong>No Preemption</strong></td><td>Resources cannot be forcibly taken away</td><td>Allow timeouts or forced release</td></tr>
                    <tr><td><strong>Circular Wait</strong></td><td>A cycle: A waits for B, B waits for A</td><td>Order your lock acquisition!</td></tr>
                </tbody>
            </table>

            <h2>Classic Deadlock Example</h2>
<pre><code><span class="token-keyword">import</span> threading, time

lock_a = threading.Lock()
lock_b = threading.Lock()

<span class="token-keyword">def</span> <span class="token-function">thread_1</span>():
    <span class="token-keyword">with</span> lock_a:
        print(<span class="token-string">"T1 holds A, waiting for B..."</span>)
        time.sleep(<span class="token-number">0.1</span>)
        <span class="token-keyword">with</span> lock_b:  <span class="token-comment"># BLOCKED — T2 holds B!</span>
            print(<span class="token-string">"T1 got both"</span>)

<span class="token-keyword">def</span> <span class="token-function">thread_2</span>():
    <span class="token-keyword">with</span> lock_b:
        print(<span class="token-string">"T2 holds B, waiting for A..."</span>)
        time.sleep(<span class="token-number">0.1</span>)
        <span class="token-keyword">with</span> lock_a:  <span class="token-comment"># BLOCKED — T1 holds A!</span>
            print(<span class="token-string">"T2 got both"</span>)

<span class="token-comment"># DEADLOCK: T1 has A wants B, T2 has B wants A</span>
t1 = threading.Thread(target=thread_1)
t2 = threading.Thread(target=thread_2)
t1.start(); t2.start()
t1.join(); t2.join()  <span class="token-comment"># Hangs forever!</span></code></pre>

            <h2>Prevention: Lock Ordering</h2>
<pre><code><span class="token-comment"># FIX: Always acquire locks in the SAME order (A before B)</span>
<span class="token-keyword">def</span> <span class="token-function">thread_1_fixed</span>():
    <span class="token-keyword">with</span> lock_a:
        <span class="token-keyword">with</span> lock_b:
            print(<span class="token-string">"T1 got both safely"</span>)

<span class="token-keyword">def</span> <span class="token-function">thread_2_fixed</span>():
    <span class="token-keyword">with</span> lock_a:  <span class="token-comment"># Same order as T1! A then B</span>
        <span class="token-keyword">with</span> lock_b:
            print(<span class="token-string">"T2 got both safely"</span>)</code></pre>

            <h2>Prevention: Timeout-Based</h2>
<pre><code><span class="token-keyword">def</span> <span class="token-function">thread_with_timeout</span>():
    acquired_a = lock_a.acquire(timeout=<span class="token-number">1.0</span>)
    <span class="token-keyword">if</span> <span class="token-keyword">not</span> acquired_a:
        <span class="token-keyword">return</span>  <span class="token-comment"># Give up, try later</span>
    <span class="token-keyword">try</span>:
        acquired_b = lock_b.acquire(timeout=<span class="token-number">1.0</span>)
        <span class="token-keyword">if</span> <span class="token-keyword">not</span> acquired_b:
            <span class="token-keyword">return</span>  <span class="token-comment"># Release A and back off</span>
        <span class="token-keyword">try</span>:
            <span class="token-comment"># Do work with both locks</span>
            <span class="token-keyword">pass</span>
        <span class="token-keyword">finally</span>:
            lock_b.release()
    <span class="token-keyword">finally</span>:
        lock_a.release()</code></pre>

            <h2>Deadlock Detection</h2>
<pre><code><span class="token-keyword">import</span> threading

<span class="token-comment"># Python's faulthandler can dump threads stuck in deadlock</span>
<span class="token-keyword">import</span> faulthandler
faulthandler.enable()
<span class="token-comment"># If program hangs, press Ctrl+C to see thread tracebacks</span>
<span class="token-comment"># In production: use watchdog timers and thread dumps</span></code></pre>

            <div class="industry-box">
                <h4>Real-World Deadlock Stories</h4>
                <ul>
                    <li><strong>Databases</strong> — PostgreSQL, MySQL detect deadlocks automatically and kill one transaction (victim selection).</li>
                    <li><strong>Operating Systems</strong> — Resource Allocation Graphs detect cycles = deadlock.</li>
                    <li><strong>Kubernetes</strong> — Pod scheduling deadlocks when resources are over-committed.</li>
                    <li><strong>Microservices</strong> — Distributed deadlock: Service A calls B, B calls A, both timeout.</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Deadlock: threads permanently stuck waiting for each other's resources</li>
<li>Requires ALL four conditions: mutual exclusion, hold-and-wait, no preemption, circular wait</li>
<li>Prevention #1: Always acquire locks in the SAME global order</li>
<li>Prevention #2: Use timeouts — give up and retry if lock not acquired in time</li>
<li>Prevention #3: Acquire all needed locks at once (atomically)</li>
<li>Detection: thread dumps, watchdog timers, database deadlock detectors</li>
</ul>""",
    mental_model="""DEADLOCK CYCLE:
    Thread 1: holds [Lock A] --wants--> [Lock B]
                      ^                      |
                      |                      v
    Thread 2: holds [Lock B] --wants--> [Lock A]

    Both wait forever. CIRCULAR DEPENDENCY.

FIX (ordered acquisition):
    Thread 1: acquire A, then B  --> gets both
    Thread 2: acquire A, then B  --> waits for A, gets both after T1 releases""",
    mistakes="""<ul>
<li><strong>Inconsistent lock ordering</strong> — Thread 1 takes A then B; Thread 2 takes B then A. Always use same order!</li>
<li><strong>Holding locks across I/O</strong> — Network calls while holding locks dramatically increases deadlock risk.</li>
<li><strong>Nested locks without planning</strong> — Each new nested lock is a deadlock opportunity.</li>
<li><strong>No timeout strategy</strong> — Without timeouts, deadlocks hang forever silently.</li>
</ul>""",
    exercise="""<ol>
<li>Create a deadlock with two threads and two locks. Observe the hang.</li>
<li>Fix it using consistent lock ordering.</li>
<li>Implement a transfer function between two bank accounts using lock ordering (always lock lower account ID first).</li>
<li>Add deadlock detection: a watchdog thread that prints warning if main thread is stuck for > 5 seconds.</li>
</ol>""",
    prev_link="05-mutex-locks.html", prev_title="Mutex & Locks",
    next_link="07-livelocks-starvation.html", next_title="Livelocks & Starvation"
)

# Topic 07
write_topic("07-livelocks-starvation.html",
    title="Livelocks &amp; Starvation",
    subtitle="Deadlock's sneaky cousins. In a livelock, threads are active but make no progress. In starvation, one thread never gets a turn.",
    tags=["beginner","concept","code"],
    analogy_title="The Hallway Dance &amp; the Polite Person",
    analogy="""<p><strong>Livelock</strong>: Two people meet in a narrow hallway. Both step left to let the other pass. Then both step right. Then left again. They keep "dancing" but neither passes. They are active (moving) but make ZERO progress.</p>
<p><strong>Starvation</strong>: A polite person at a buffet who always says "after you." Everyone else keeps going first. The polite person never gets food — starved out by others.</p>""",
    content="""
            <h2>Livelock: Active but No Progress</h2>
            <p>Unlike deadlock (threads frozen), in a <strong>livelock</strong> threads are running, consuming CPU, responding to each other — but no useful work gets done.</p>

<pre><code><span class="token-keyword">import</span> threading, time

<span class="token-keyword">class</span> <span class="token-class">Worker</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self, name, partner=<span class="token-keyword">None</span>):
        self.name = name
        self.working = <span class="token-keyword">False</span>
        self.partner = partner

    <span class="token-keyword">def</span> <span class="token-function">work</span>(self):
        <span class="token-keyword">while</span> <span class="token-keyword">True</span>:
            <span class="token-keyword">if</span> self.partner.working:
                <span class="token-comment"># "Politely" wait — but partner does the same!</span>
                print(<span class="token-string">f"{self.name}: Partner busy, backing off"</span>)
                time.sleep(<span class="token-number">0.01</span>)
                <span class="token-keyword">continue</span>
            self.working = <span class="token-keyword">True</span>
            print(<span class="token-string">f"{self.name}: Working!"</span>)
            time.sleep(<span class="token-number">0.01</span>)
            self.working = <span class="token-keyword">False</span>
            <span class="token-keyword">break</span>

<span class="token-comment"># Both see the other as "working" and back off forever</span>
alice = Worker(<span class="token-string">"Alice"</span>)
bob = Worker(<span class="token-string">"Bob"</span>)
alice.partner = bob
bob.partner = alice</code></pre>

            <h2>Starvation: Never Getting a Turn</h2>
<pre><code><span class="token-keyword">import</span> threading, time, random

resource_lock = threading.Lock()
access_count = {<span class="token-string">"high_priority"</span>: <span class="token-number">0</span>, <span class="token-string">"low_priority"</span>: <span class="token-number">0</span>}

<span class="token-keyword">def</span> <span class="token-function">high_priority_worker</span>():
    <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">1000</span>):
        <span class="token-keyword">with</span> resource_lock:
            access_count[<span class="token-string">"high_priority"</span>] += <span class="token-number">1</span>
        time.sleep(<span class="token-number">0.0001</span>)  <span class="token-comment"># Tiny gap — grabs lock again quickly</span>

<span class="token-keyword">def</span> <span class="token-function">low_priority_worker</span>():
    <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10</span>):
        <span class="token-keyword">with</span> resource_lock:
            access_count[<span class="token-string">"low_priority"</span>] += <span class="token-number">1</span>

<span class="token-comment"># With many high-priority threads, low-priority gets starved</span>
threads = [threading.Thread(target=high_priority_worker) <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10</span>)]
threads.append(threading.Thread(target=low_priority_worker))
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.start()
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.join()
print(access_count)  <span class="token-comment"># low_priority might be way behind</span></code></pre>

            <h2>Deadlock vs Livelock vs Starvation</h2>
            <table class="comparison-table">
                <thead><tr><th>Problem</th><th>Threads Active?</th><th>Progress?</th><th>Fix</th></tr></thead>
                <tbody>
                    <tr><td><strong>Deadlock</strong></td><td>No (blocked)</td><td>None</td><td>Lock ordering, timeouts</td></tr>
                    <tr><td><strong>Livelock</strong></td><td>Yes (running)</td><td>None</td><td>Random backoff, priority</td></tr>
                    <tr><td><strong>Starvation</strong></td><td>Some yes, victim no</td><td>Others progress, victim does not</td><td>Fair locks, aging</td></tr>
                </tbody>
            </table>

            <h2>Solutions</h2>
<pre><code><span class="token-comment"># Fix Livelock: Random backoff (like Ethernet CSMA/CD)</span>
<span class="token-keyword">import</span> random

<span class="token-keyword">def</span> <span class="token-function">work_with_backoff</span>(worker):
    retries = <span class="token-number">0</span>
    <span class="token-keyword">while</span> <span class="token-keyword">True</span>:
        <span class="token-keyword">if</span> worker.partner.working:
            <span class="token-comment"># Random backoff breaks the symmetry!</span>
            time.sleep(random.uniform(<span class="token-number">0.001</span>, <span class="token-number">0.01</span>) * (<span class="token-number">2</span> ** retries))
            retries += <span class="token-number">1</span>
            <span class="token-keyword">continue</span>
        worker.working = <span class="token-keyword">True</span>
        <span class="token-keyword">break</span>

<span class="token-comment"># Fix Starvation: Fair lock (FIFO ordering)</span>
<span class="token-keyword">import</span> queue

<span class="token-keyword">class</span> <span class="token-class">FairLock</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self):
        self._queue = queue.Queue()
        self._lock = threading.Lock()

    <span class="token-keyword">def</span> <span class="token-function">acquire</span>(self):
        event = threading.Event()
        self._queue.put(event)
        <span class="token-keyword">while</span> <span class="token-keyword">True</span>:
            <span class="token-keyword">with</span> self._lock:
                <span class="token-keyword">if</span> self._queue.queue[<span class="token-number">0</span>] <span class="token-keyword">is</span> event:
                    <span class="token-keyword">return</span>
            event.wait(timeout=<span class="token-number">0.01</span>)

    <span class="token-keyword">def</span> <span class="token-function">release</span>(self):
        self._queue.get()</code></pre>

            <div class="industry-box">
                <h4>Industry Examples</h4>
                <ul>
                    <li><strong>Ethernet (CSMA/CD)</strong> — Random exponential backoff prevents livelock when multiple devices transmit simultaneously.</li>
                    <li><strong>Java ReentrantLock(fair=true)</strong> — FIFO ordering prevents starvation.</li>
                    <li><strong>OS schedulers</strong> — Priority aging: low-priority processes slowly gain priority to prevent starvation.</li>
                    <li><strong>Database write-starved readers</strong> — Too many readers can starve writers. Fixed with write-preferring locks.</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Livelock: threads are active but make no progress (hallway dance)</li>
<li>Starvation: one thread never gets access to a resource</li>
<li>Fix livelock: random backoff breaks symmetry between competing threads</li>
<li>Fix starvation: fair/FIFO locks, priority aging</li>
<li>Unlike deadlock, livelocked threads consume CPU doing nothing useful</li>
</ul>""",
    mental_model="""DEADLOCK:   T1 blocked, T2 blocked. Neither moves.
LIVELOCK:   T1 backs off, T2 backs off, T1 backs off... (infinite loop)
STARVATION: T1 gets lock, T2 gets lock, T3 gets lock... T4 NEVER gets lock.

Random backoff fix:
    T1 waits 3ms, T2 waits 7ms --> T1 goes first, T2 follows. Progress!""",
    mistakes="""<ul>
<li><strong>Confusing livelock with deadlock</strong> — In livelock, threads ARE running (check CPU usage).</li>
<li><strong>Symmetric retry logic</strong> — If all threads retry identically, they stay synchronized. Add randomness!</li>
<li><strong>Ignoring fairness</strong> — Default locks are not fair. Under contention, some threads may starve.</li>
<li><strong>Priority inversion</strong> — High-priority thread starved because low-priority thread holds a lock it needs.</li>
</ul>""",
    exercise="""<ol>
<li>Create a livelock: two threads that back off when they see the other working (both stay stuck).</li>
<li>Fix it with random exponential backoff.</li>
<li>Demonstrate starvation: 10 aggressive threads vs 1 that rarely gets the lock.</li>
<li>Implement a fair lock using a queue and show it prevents starvation.</li>
</ol>""",
    prev_link="06-deadlocks.html", prev_title="Deadlocks",
    next_link="08-thread-safety.html", next_title="Thread Safety"
)

# Topic 08
write_topic("08-thread-safety.html",
    title="Thread Safety",
    subtitle="How to write code that works correctly even when multiple threads use it simultaneously. The gold standard for shared code in concurrent programs.",
    tags=["beginner","concept","code"],
    analogy_title="The Vending Machine",
    analogy="""<p>A <strong>thread-safe</strong> vending machine works perfectly even when 10 people press buttons at the same time:</p>
<ul><li>It processes one transaction at a time internally</li>
<li>It never gives two people the same item</li>
<li>It never takes money without dispensing</li></ul>
<p>A <strong>non-thread-safe</strong> vending machine might give the same soda to two people or eat your money when two people insert coins simultaneously.</p>""",
    content="""
            <h2>What Is Thread Safety?</h2>
            <p>Code is <strong>thread-safe</strong> if it behaves correctly when accessed from multiple threads simultaneously, with no additional synchronization needed by the caller.</p>

            <h3>Levels of Thread Safety</h3>
            <table class="comparison-table">
                <thead><tr><th>Level</th><th>Definition</th><th>Example</th></tr></thead>
                <tbody>
                    <tr><td><strong>Immutable</strong></td><td>Cannot be modified after creation</td><td>Python tuples, frozensets, strings</td></tr>
                    <tr><td><strong>Thread-safe</strong></td><td>Internal synchronization handles everything</td><td>queue.Queue, logging module</td></tr>
                    <tr><td><strong>Conditionally safe</strong></td><td>Safe for specific operations only</td><td>Python dict (single ops safe, compound ops not)</td></tr>
                    <tr><td><strong>Not thread-safe</strong></td><td>Caller must provide synchronization</td><td>list.append is safe, but read+modify+write is not</td></tr>
                </tbody>
            </table>

            <h2>Strategies for Thread Safety</h2>
<pre><code><span class="token-keyword">import</span> threading
<span class="token-keyword">from</span> queue <span class="token-keyword">import</span> Queue

<span class="token-comment"># Strategy 1: Immutability (safest)</span>
<span class="token-keyword">class</span> <span class="token-class">ImmutableConfig</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self, host, port):
        self._host = host
        self._port = port
    <span class="token-builtin">@property</span>
    <span class="token-keyword">def</span> <span class="token-function">host</span>(self): <span class="token-keyword">return</span> self._host
    <span class="token-builtin">@property</span>
    <span class="token-keyword">def</span> <span class="token-function">port</span>(self): <span class="token-keyword">return</span> self._port
    <span class="token-comment"># No setters! Cannot be modified = always thread-safe</span>

<span class="token-comment"># Strategy 2: Thread-local storage (no sharing)</span>
local_data = threading.local()

<span class="token-keyword">def</span> <span class="token-function">worker</span>():
    local_data.request_id = threading.current_thread().name
    <span class="token-comment"># Each thread has its own copy — no sharing, no conflict</span>
    print(<span class="token-string">f"My request: {local_data.request_id}"</span>)

<span class="token-comment"># Strategy 3: Synchronized access (locks)</span>
<span class="token-keyword">class</span> <span class="token-class">ThreadSafeList</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self):
        self._items = []
        self._lock = threading.Lock()

    <span class="token-keyword">def</span> <span class="token-function">append</span>(self, item):
        <span class="token-keyword">with</span> self._lock:
            self._items.append(item)

    <span class="token-keyword">def</span> <span class="token-function">pop</span>(self):
        <span class="token-keyword">with</span> self._lock:
            <span class="token-keyword">return</span> self._items.pop() <span class="token-keyword">if</span> self._items <span class="token-keyword">else</span> <span class="token-keyword">None</span>

    <span class="token-keyword">def</span> <span class="token-function">size</span>(self):
        <span class="token-keyword">with</span> self._lock:
            <span class="token-keyword">return</span> len(self._items)

<span class="token-comment"># Strategy 4: Message passing (no shared state)</span>
<span class="token-keyword">def</span> <span class="token-function">producer</span>(q):
    <span class="token-keyword">for</span> i <span class="token-keyword">in</span> range(<span class="token-number">100</span>):
        q.put(i)  <span class="token-comment"># Queue handles synchronization internally</span>

<span class="token-keyword">def</span> <span class="token-function">consumer</span>(q):
    <span class="token-keyword">while</span> <span class="token-keyword">True</span>:
        item = q.get()  <span class="token-comment"># Blocks until item available</span>
        <span class="token-keyword">if</span> item <span class="token-keyword">is</span> <span class="token-keyword">None</span>: <span class="token-keyword">break</span>
        process(item)</code></pre>

            <h2>Python GIL and Thread Safety</h2>
            <div class="callout callout-info">
                <div class="callout-title">The GIL Does NOT Make Your Code Thread-Safe!</div>
                <p>Python's GIL prevents two threads from executing Python bytecodes simultaneously, but it does NOT make compound operations atomic. <code>counter += 1</code> is still three bytecodes (LOAD, ADD, STORE) and the GIL can release between any of them.</p>
            </div>

<pre><code><span class="token-comment"># GIL does NOT protect this!</span>
counter = <span class="token-number">0</span>
<span class="token-keyword">def</span> <span class="token-function">unsafe</span>():
    <span class="token-keyword">global</span> counter
    <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">100000</span>):
        counter += <span class="token-number">1</span>  <span class="token-comment"># LOAD_GLOBAL, then BINARY_ADD, then STORE_GLOBAL</span>
        <span class="token-comment"># GIL can switch threads between any of these!</span></code></pre>

            <div class="industry-box">
                <h4>Thread-Safe by Design</h4>
                <ul>
                    <li><strong>Go</strong> — "Don't communicate by sharing memory; share memory by communicating" (channels)</li>
                    <li><strong>Rust</strong> — Ownership system prevents data races at compile time</li>
                    <li><strong>Erlang/Elixir</strong> — All data is immutable, communication via message passing only</li>
                    <li><strong>Java ConcurrentHashMap</strong> — Thread-safe without external synchronization</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Thread-safe code works correctly under concurrent access without caller synchronization</li>
<li>Strategies: immutability, thread-local storage, locks, message passing</li>
<li>Immutability is the safest — data that cannot change cannot race</li>
<li>Python's GIL does NOT make code thread-safe for compound operations</li>
<li>Prefer message passing (queues) over shared mutable state when possible</li>
<li>queue.Queue is Python's best friend for thread-safe communication</li>
</ul>""",
    mental_model="""THREAD SAFETY HIERARCHY (safest to least safe):

1. IMMUTABLE      -- Cannot be changed, always safe
2. THREAD-LOCAL   -- Each thread owns its copy, no sharing
3. MESSAGE PASSING-- Communicate via queues, no shared state
4. SYNCHRONIZED   -- Shared state + locks = safe but complex
5. UNSAFE         -- Shared state + no locks = BUGS""",
    mistakes="""<ul>
<li><strong>Relying on the GIL</strong> — GIL protects CPython internals, NOT your logic.</li>
<li><strong>Marking a class "thread-safe" without testing</strong> — Test with 100+ concurrent threads to find races.</li>
<li><strong>Thread-safe individual ops but unsafe compound ops</strong> — dict[key] is safe, but check-then-set is not.</li>
<li><strong>Mixing strategies</strong> — Using both locks AND queues for the same data creates confusion.</li>
</ul>""",
    exercise="""<ol>
<li>Create a thread-safe stack (push, pop, peek) using locks.</li>
<li>Create the same stack using queue.LifoQueue — compare code complexity.</li>
<li>Show that Python's list is NOT thread-safe: have threads do check-length-then-pop.</li>
<li>Rewrite a shared-state solution to use message passing (Queue) instead.</li>
</ol>""",
    prev_link="07-livelocks-starvation.html", prev_title="Livelocks & Starvation",
    next_link="09-atomic-operations-cas.html", next_title="Atomic Ops & CAS"
)

print("\n=== Module 1 (topics 03-08) generation complete ===")
