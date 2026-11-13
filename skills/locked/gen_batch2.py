"""Generate topics 09-13: Low-Level Concurrency"""
import sys
sys.path.insert(0, '.')
from gen_template import write_topic

# Topic 09
write_topic("09-atomic-operations-cas.html",
    title="Atomic Operations &amp; CAS",
    subtitle="Operations that complete in a single indivisible step — no other thread can see them half-done. The foundation of lock-free programming.",
    tags=["intermediate","concept","code"],
    analogy_title="The Light Switch",
    analogy="""<p>Flipping a light switch is <strong>atomic</strong> — it is either ON or OFF, never halfway. You cannot catch it between states.</p>
<p><strong>Compare-And-Swap (CAS)</strong> is like a safe with a combination: "Change the code to 5678 ONLY IF it is currently 1234." If someone already changed it, your attempt fails and you must retry with the new code.</p>""",
    content="""
            <h2>What Are Atomic Operations?</h2>
            <p>An <strong>atomic operation</strong> completes in a single indivisible step at the hardware level. No thread can observe it half-done. No lock needed.</p>

            <h3>Why Locks Are Slow</h3>
            <p>Locks require: acquire (system call) → do work → release (system call). That is expensive. Atomic operations do the same thing with a <strong>single CPU instruction</strong>.</p>

            <table class="comparison-table">
                <thead><tr><th>Operation</th><th>Description</th><th>CPU Instruction</th></tr></thead>
                <tbody>
                    <tr><td><strong>Atomic Load</strong></td><td>Read a value atomically</td><td>MOV (aligned)</td></tr>
                    <tr><td><strong>Atomic Store</strong></td><td>Write a value atomically</td><td>MOV (aligned)</td></tr>
                    <tr><td><strong>Atomic Add</strong></td><td>Increment in one step</td><td>LOCK XADD</td></tr>
                    <tr><td><strong>Compare-And-Swap</strong></td><td>Update only if current value matches expected</td><td>LOCK CMPXCHG</td></tr>
                </tbody>
            </table>

            <h2>Compare-And-Swap (CAS)</h2>
            <p>The most important atomic operation. Pseudocode:</p>
<pre><code><span class="token-comment"># CAS(location, expected_value, new_value)</span>
<span class="token-comment"># Atomically:</span>
<span class="token-comment">#   if memory[location] == expected_value:</span>
<span class="token-comment">#       memory[location] = new_value</span>
<span class="token-comment">#       return True</span>
<span class="token-comment">#   else:</span>
<span class="token-comment">#       return False  (someone else changed it first)</span></code></pre>

            <h2>Python Implementation (using ctypes for true atomics)</h2>
<pre><code><span class="token-keyword">import</span> threading
<span class="token-keyword">import</span> ctypes

<span class="token-comment"># Python doesn't have built-in atomics, but we can simulate CAS logic</span>
<span class="token-keyword">class</span> <span class="token-class">AtomicCounter</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self, initial=<span class="token-number">0</span>):
        self._value = initial
        self._lock = threading.Lock()  <span class="token-comment"># Simulates hardware CAS</span>

    <span class="token-keyword">def</span> <span class="token-function">compare_and_swap</span>(self, expected, new_value):
        <span class="token-keyword">with</span> self._lock:
            <span class="token-keyword">if</span> self._value == expected:
                self._value = new_value
                <span class="token-keyword">return</span> <span class="token-keyword">True</span>
            <span class="token-keyword">return</span> <span class="token-keyword">False</span>

    <span class="token-keyword">def</span> <span class="token-function">increment</span>(self):
        <span class="token-keyword">while</span> <span class="token-keyword">True</span>:
            current = self._value
            <span class="token-keyword">if</span> self.compare_and_swap(current, current + <span class="token-number">1</span>):
                <span class="token-keyword">return</span> current + <span class="token-number">1</span>
            <span class="token-comment"># CAS failed — someone else changed it. Retry!</span>

    <span class="token-keyword">def</span> <span class="token-function">get</span>(self):
        <span class="token-keyword">return</span> self._value

<span class="token-comment"># Lock-free increment using CAS retry loop</span>
counter = AtomicCounter()
threads = [threading.Thread(target=<span class="token-keyword">lambda</span>: [counter.increment() <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10000</span>)])
           <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10</span>)]
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.start()
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.join()
print(<span class="token-string">f"Counter: {counter.get()}"</span>)  <span class="token-comment"># Always 100,000</span></code></pre>

            <h2>The ABA Problem</h2>
            <div class="callout callout-warning">
                <div class="callout-title">CAS Pitfall: ABA</div>
                <p>Thread reads value A. Another thread changes it to B, then back to A. CAS succeeds (sees A) but the state may have changed semantically. Fix: use version counters or tagged pointers.</p>
            </div>

            <div class="collapsible">
                <button class="collapsible-toggle">Go Example: sync/atomic</button>
                <div class="collapsible-content">
<pre><code><span class="token-keyword">package</span> main

<span class="token-keyword">import</span> (
    <span class="token-string">"fmt"</span>
    <span class="token-string">"sync"</span>
    <span class="token-string">"sync/atomic"</span>
)

<span class="token-keyword">func</span> <span class="token-function">main</span>() {
    <span class="token-keyword">var</span> counter <span class="token-builtin">int64</span>
    <span class="token-keyword">var</span> wg sync.WaitGroup

    <span class="token-keyword">for</span> i := <span class="token-number">0</span>; i &lt; <span class="token-number">10</span>; i++ {
        wg.Add(<span class="token-number">1</span>)
        <span class="token-keyword">go</span> <span class="token-keyword">func</span>() {
            <span class="token-keyword">defer</span> wg.Done()
            <span class="token-keyword">for</span> j := <span class="token-number">0</span>; j &lt; <span class="token-number">10000</span>; j++ {
                atomic.AddInt64(&amp;counter, <span class="token-number">1</span>)  <span class="token-comment">// True hardware atomic!</span>
            }
        }()
    }
    wg.Wait()
    fmt.Println(<span class="token-string">"Counter:"</span>, counter)  <span class="token-comment">// Always 100,000</span>
}</code></pre>
                </div>
            </div>

            <div class="industry-box">
                <h4>Industry Usage</h4>
                <ul>
                    <li><strong>Java AtomicInteger/AtomicReference</strong> — Built-in CAS via Unsafe class</li>
                    <li><strong>Linux kernel</strong> — atomic_t type for reference counting, spinlock implementation</li>
                    <li><strong>Lock-free queues</strong> — Michael-Scott queue uses CAS for enqueue/dequeue</li>
                    <li><strong>Database MVCC</strong> — Version numbers are atomic counters</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Atomic operations complete in one indivisible CPU instruction — no lock needed</li>
<li>CAS (Compare-And-Swap): update only if current value matches expected</li>
<li>CAS retry loop: read → compute new value → CAS. If fails, retry.</li>
<li>Faster than locks for simple operations (no system call overhead)</li>
<li>ABA problem: value changes and returns — CAS succeeds incorrectly. Fix with version numbers.</li>
<li>Python lacks true atomics; use locks to simulate. Go/Java/C++ have hardware atomics.</li>
</ul>""",
    mental_model="""CAS RETRY LOOP:
    1. Read current value (e.g., 42)
    2. Compute new value (e.g., 43)
    3. CAS(expected=42, new=43)
       - SUCCESS: value was still 42, now 43. Done!
       - FAIL: someone changed it (it's now 44). Go to step 1.

LOCK vs CAS:
    Lock:   [acquire] --- work --- [release]   (blocks others)
    CAS:    read, compute, attempt. Fail? Retry. (no blocking!)""",
    mistakes="""<ul>
<li><strong>Using CAS for complex operations</strong> — CAS works for single values. For multi-field updates, use locks.</li>
<li><strong>Ignoring ABA</strong> — Always consider if "same value" means "same state."</li>
<li><strong>Infinite retry under high contention</strong> — Many threads CASing the same value = many retries. Locks may be faster.</li>
<li><strong>Thinking Python has true atomics</strong> — CPython GIL is not a substitute for proper atomics.</li>
</ul>""",
    exercise="""<ol>
<li>Implement an atomic counter using CAS retry loop.</li>
<li>Benchmark: CAS counter vs Lock-based counter with 10 threads x 100K increments.</li>
<li>Demonstrate ABA: show a scenario where CAS succeeds but semantics are wrong.</li>
<li>Implement a lock-free stack (push/pop using CAS on the head pointer).</li>
</ol>""",
    prev_link="08-thread-safety.html", prev_title="Thread Safety",
    next_link="10-memory-visibility.html", next_title="Memory Visibility"
)

# Topic 10
write_topic("10-memory-visibility.html",
    title="Memory Visibility",
    subtitle="Why changes made by one thread may be INVISIBLE to another — even after they happen. The most surprising aspect of modern CPU architecture.",
    tags=["intermediate","concept","code"],
    analogy_title="Drafts vs Published Documents",
    analogy="""<p>Imagine each person has a <strong>personal notebook</strong> (CPU cache) and there is one <strong>shared whiteboard</strong> (main memory).</p>
<ul><li>When you write, you write in your notebook first (fast)</li>
<li>The whiteboard is only updated <strong>later</strong> (when the system decides to sync)</li>
<li>Your colleague reads the whiteboard — they see the OLD value because your notebook has not been synced yet!</li></ul>
<p>This is memory visibility. Your thread wrote the value, but other threads cannot see it yet because it is still in your CPU's cache.</p>""",
    content="""
            <h2>Why Can't Other Threads See My Writes?</h2>
            <p>Modern CPUs have <strong>multiple levels of cache</strong> (L1, L2, L3). Each core has its own L1/L2 cache. When a thread writes a value, it goes to the local cache first — NOT to main memory immediately.</p>

            <h3>The Memory Hierarchy</h3>
            <table class="comparison-table">
                <thead><tr><th>Level</th><th>Speed</th><th>Shared?</th><th>Size</th></tr></thead>
                <tbody>
                    <tr><td><strong>L1 Cache</strong></td><td>~1ns</td><td>Per core</td><td>64KB</td></tr>
                    <tr><td><strong>L2 Cache</strong></td><td>~4ns</td><td>Per core</td><td>256KB</td></tr>
                    <tr><td><strong>L3 Cache</strong></td><td>~12ns</td><td>Shared across cores</td><td>8-32MB</td></tr>
                    <tr><td><strong>Main RAM</strong></td><td>~100ns</td><td>Shared</td><td>GBs</td></tr>
                </tbody>
            </table>

            <h2>The Visibility Problem Demonstrated</h2>
<pre><code><span class="token-keyword">import</span> threading, time

<span class="token-comment"># This can loop FOREVER in languages without a memory model (C/C++ without volatile)</span>
<span class="token-comment"># Python's GIL mostly prevents this, but the concept is critical for system design</span>

running = <span class="token-keyword">True</span>  <span class="token-comment"># Shared flag</span>

<span class="token-keyword">def</span> <span class="token-function">worker</span>():
    count = <span class="token-number">0</span>
    <span class="token-keyword">while</span> running:  <span class="token-comment"># May never see running=False without memory barrier!</span>
        count += <span class="token-number">1</span>
    print(<span class="token-string">f"Worker did {count} iterations"</span>)

<span class="token-keyword">def</span> <span class="token-function">stopper</span>():
    <span class="token-keyword">global</span> running
    time.sleep(<span class="token-number">1</span>)
    running = <span class="token-keyword">False</span>  <span class="token-comment"># Written to local cache — when does worker see it?</span>

t1 = threading.Thread(target=worker)
t2 = threading.Thread(target=stopper)
t1.start(); t2.start()
t1.join(); t2.join()</code></pre>

            <h2>Memory Barriers (Fences)</h2>
            <p>A <strong>memory barrier</strong> forces the CPU to sync its cache with main memory:</p>
            <ul>
                <li><strong>Store barrier</strong>: flush writes from cache to memory (make visible)</li>
                <li><strong>Load barrier</strong>: refresh reads from memory (see latest)</li>
                <li><strong>Full barrier</strong>: both — all writes visible AND all reads fresh</li>
            </ul>

<pre><code><span class="token-comment"># In Python, locks act as memory barriers</span>
lock = threading.Lock()
shared_value = <span class="token-number">0</span>

<span class="token-keyword">def</span> <span class="token-function">writer</span>():
    <span class="token-keyword">global</span> shared_value
    <span class="token-keyword">with</span> lock:  <span class="token-comment"># Release = store barrier (flushes writes)</span>
        shared_value = <span class="token-number">42</span>

<span class="token-keyword">def</span> <span class="token-function">reader</span>():
    <span class="token-keyword">with</span> lock:  <span class="token-comment"># Acquire = load barrier (refreshes reads)</span>
        print(shared_value)  <span class="token-comment"># Guaranteed to see 42 after writer releases</span></code></pre>

            <h2>CPU Reordering</h2>
            <div class="callout callout-danger">
                <div class="callout-title">CPUs Reorder Instructions!</div>
                <p>CPUs can execute instructions out of order for performance. Thread A writes x=1 then y=2. Thread B might see y=2 but x=0! Memory barriers prevent this reordering.</p>
            </div>

            <div class="industry-box">
                <h4>Industry Impact</h4>
                <ul>
                    <li><strong>Java volatile</strong> — Forces reads/writes through main memory with barriers</li>
                    <li><strong>C++ std::atomic</strong> — Provides memory_order options (relaxed, acquire, release, seq_cst)</li>
                    <li><strong>Linux kernel</strong> — mb(), rmb(), wmb() macros for explicit barriers</li>
                    <li><strong>ARM vs x86</strong> — ARM has weaker memory model (more reordering) than x86</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Each CPU core has its own cache — writes may not be immediately visible to other cores</li>
<li>Memory barriers force cache synchronization between cores</li>
<li>Locks provide implicit memory barriers (acquire = load barrier, release = store barrier)</li>
<li>CPUs reorder instructions for performance — barriers prevent this</li>
<li>Python's GIL provides some protection, but the concept matters for system design</li>
<li>Different architectures (ARM vs x86) have different memory ordering guarantees</li>
</ul>""",
    mental_model="""Core 1 Cache:  [x=42]  ← written here first
Main Memory:   [x=0]   ← stale!
Core 2 Cache:  [x=0]   ← reads stale value

After MEMORY BARRIER on Core 1:
Main Memory:   [x=42]  ← flushed!
After LOAD BARRIER on Core 2:
Core 2 Cache:  [x=42]  ← refreshed!""",
    mistakes="""<ul>
<li><strong>Assuming writes are instantly visible</strong> — They are NOT without barriers or synchronization.</li>
<li><strong>Relying on timing</strong> — "I wrote it 1ms ago so it must be visible" — NO guarantee.</li>
<li><strong>Ignoring reordering</strong> — x=1; y=2 may be seen as y=2; x=0 by another thread.</li>
<li><strong>Not understanding your platform</strong> — x86 is strongly ordered, ARM is weakly ordered.</li>
</ul>""",
    exercise="""<ol>
<li>Research: What memory ordering does your CPU architecture use? (x86 = TSO, ARM = relaxed)</li>
<li>In Java/C++: demonstrate that a flag set by one thread is not seen by another without volatile/atomic.</li>
<li>Show that Python locks act as memory barriers: write+release, then acquire+read.</li>
<li>Draw the cache hierarchy of a modern multi-core CPU and trace a write through all levels.</li>
</ol>""",
    prev_link="09-atomic-operations-cas.html", prev_title="Atomic Ops & CAS",
    next_link="11-happens-before.html", next_title="Happens-Before"
)

# Topic 11
write_topic("11-happens-before.html",
    title="Happens-Before Relationship",
    subtitle="The formal guarantee that one operation's effects are visible to another. Without this, concurrent programs are unpredictable.",
    tags=["intermediate","concept","theory"],
    analogy_title="Sending a Letter",
    analogy="""<p>If you <strong>mail a letter</strong> (write) and your friend <strong>receives it</strong> (read), there is a happens-before relationship: you wrote before they read.</p>
<p>But if you both write letters to each other at the same time, there is NO happens-before — neither can see the other's letter. The order is undefined.</p>
<p>In concurrency: if A happens-before B, then B is <strong>guaranteed</strong> to see everything A did. Without it, B might see stale data.</p>""",
    content="""
            <h2>What Is Happens-Before?</h2>
            <p>The <strong>happens-before</strong> relationship is a formal ordering guarantee between operations in different threads. If operation A happens-before operation B, then:</p>
            <ul>
                <li>All memory writes done by A are <strong>visible</strong> to B</li>
                <li>A is guaranteed to have <strong>completed</strong> before B starts</li>
            </ul>

            <h3>Rules That Establish Happens-Before</h3>
            <table class="comparison-table">
                <thead><tr><th>Rule</th><th>Description</th><th>Example</th></tr></thead>
                <tbody>
                    <tr><td><strong>Program order</strong></td><td>Within one thread, earlier statements HB later ones</td><td>x=1; y=2; → x=1 HB y=2</td></tr>
                    <tr><td><strong>Lock release → acquire</strong></td><td>Unlock HB next lock of same mutex</td><td>T1 unlocks → T2 locks = T2 sees T1's writes</td></tr>
                    <tr><td><strong>Thread start</strong></td><td>Starting a thread HB that thread's first action</td><td>t.start() HB first line in t's run()</td></tr>
                    <tr><td><strong>Thread join</strong></td><td>Thread's last action HB join() return</td><td>t.join() returns → you see all of t's writes</td></tr>
                    <tr><td><strong>Volatile write → read</strong></td><td>Write to volatile HB subsequent read</td><td>Java volatile, C++ atomic</td></tr>
                    <tr><td><strong>Transitivity</strong></td><td>If A HB B, and B HB C, then A HB C</td><td>Chain of guarantees</td></tr>
                </tbody>
            </table>

            <h2>Practical Implications</h2>
<pre><code><span class="token-keyword">import</span> threading

shared_data = {}
lock = threading.Lock()

<span class="token-keyword">def</span> <span class="token-function">writer</span>():
    shared_data[<span class="token-string">"result"</span>] = <span class="token-number">42</span>
    shared_data[<span class="token-string">"ready"</span>] = <span class="token-keyword">True</span>
    lock.release()  <span class="token-comment"># This creates a happens-before edge</span>

<span class="token-keyword">def</span> <span class="token-function">reader</span>():
    lock.acquire()  <span class="token-comment"># Matches writer's release = happens-before!</span>
    <span class="token-comment"># GUARANTEED to see result=42 and ready=True</span>
    assert shared_data[<span class="token-string">"ready"</span>] == <span class="token-keyword">True</span>
    assert shared_data[<span class="token-string">"result"</span>] == <span class="token-number">42</span>

<span class="token-comment"># Using join() for happens-before</span>
result = [<span class="token-keyword">None</span>]

<span class="token-keyword">def</span> <span class="token-function">compute</span>():
    result[<span class="token-number">0</span>] = heavy_calculation()

t = threading.Thread(target=compute)
t.start()
t.join()  <span class="token-comment"># Everything in compute() happens-before this line</span>
print(result[<span class="token-number">0</span>])  <span class="token-comment"># Guaranteed to see the computed value</span></code></pre>

            <h2>What Has NO Happens-Before?</h2>
<pre><code><span class="token-comment"># DANGER: No synchronization = no happens-before = no guarantee</span>
flag = <span class="token-keyword">False</span>
data = <span class="token-number">0</span>

<span class="token-keyword">def</span> <span class="token-function">writer_unsafe</span>():
    <span class="token-keyword">global</span> data, flag
    data = <span class="token-number">42</span>
    flag = <span class="token-keyword">True</span>  <span class="token-comment"># No lock, no barrier</span>

<span class="token-keyword">def</span> <span class="token-function">reader_unsafe</span>():
    <span class="token-keyword">if</span> flag:  <span class="token-comment"># Might see True...</span>
        print(data)  <span class="token-comment"># But data might still be 0! (reordering/visibility)</span>
    <span class="token-comment"># Without happens-before, seeing flag=True does NOT guarantee data=42</span></code></pre>

            <div class="industry-box">
                <h4>Language Memory Models</h4>
                <ul>
                    <li><strong>Java Memory Model (JMM)</strong> — Formally defines happens-before for synchronized, volatile, final fields</li>
                    <li><strong>C++ Memory Model</strong> — seq_cst (default) provides total ordering; relaxed allows reordering</li>
                    <li><strong>Go Memory Model</strong> — Channel send HB channel receive; sync ops establish HB</li>
                    <li><strong>Python</strong> — GIL + lock semantics provide implicit HB (but only through proper synchronization)</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Happens-before (HB) guarantees one operation's effects are visible to another</li>
<li>Without HB, there are NO guarantees about what another thread sees</li>
<li>Lock release HB next lock acquire (same lock) — the fundamental rule</li>
<li>Thread.join() establishes HB — after join, you see all of that thread's work</li>
<li>Transitivity: A HB B, B HB C → A HB C</li>
<li>No synchronization = no HB = potential visibility bugs</li>
</ul>""",
    mental_model="""HAPPENS-BEFORE CHAIN:
    T1: write(x=42) → release(lock)
                              ↓ (happens-before)
    T2:                acquire(lock) → read(x)  ← sees 42!

NO HAPPENS-BEFORE:
    T1: write(x=42)
    T2: read(x)  ← might see 0 or 42. UNDEFINED!""",
    mistakes="""<ul>
<li><strong>Assuming sequential consistency</strong> — Without sync, operations can appear in any order to other threads.</li>
<li><strong>Flag-based signaling without barriers</strong> — Setting a boolean flag without a lock does NOT guarantee visibility.</li>
<li><strong>Confusing program order with global order</strong> — Within YOUR thread, order is preserved. Across threads, anything goes.</li>
<li><strong>Thinking "it works in testing"</strong> — x86 has strong ordering that hides bugs. ARM/production may expose them.</li>
</ul>""",
    exercise="""<ol>
<li>Identify all happens-before relationships in a producer-consumer with locks.</li>
<li>Show code where flag=True is set by thread A, but thread B reads flag=True and still sees stale data.</li>
<li>Fix it with proper synchronization (lock or Event).</li>
<li>Draw a happens-before graph for a 3-thread scenario with two shared locks.</li>
</ol>""",
    prev_link="10-memory-visibility.html", prev_title="Memory Visibility",
    next_link="12-volatile-vs-synchronized.html", next_title="Volatile vs Synchronized"
)

# Topic 12
write_topic("12-volatile-vs-synchronized.html",
    title="Volatile vs Synchronized",
    subtitle="Two different tools for thread communication. Volatile ensures visibility; synchronized ensures both visibility AND atomicity.",
    tags=["intermediate","concept","code"],
    analogy_title="Megaphone vs Private Room",
    analogy="""<p><strong>Volatile (megaphone)</strong>: When you update a value, you shout it through a megaphone. Everyone hears the latest value immediately. But if two people shout at once, it is chaos.</p>
<p><strong>Synchronized (private room)</strong>: Only one person can enter the room. Inside, they can read and write freely. Others wait. Guarantees both visibility AND exclusive access.</p>""",
    content="""
            <h2>The Two Problems of Concurrency</h2>
            <table class="comparison-table">
                <thead><tr><th>Problem</th><th>Description</th><th>Solution</th></tr></thead>
                <tbody>
                    <tr><td><strong>Visibility</strong></td><td>Thread B doesn't see Thread A's writes</td><td>volatile / memory barriers</td></tr>
                    <tr><td><strong>Atomicity</strong></td><td>Compound operations get interleaved</td><td>synchronized / locks</td></tr>
                </tbody>
            </table>

            <h2>When Volatile Is Enough</h2>
<pre><code><span class="token-keyword">import</span> threading

<span class="token-comment"># Volatile-equivalent in Python: threading.Event or explicit barriers</span>
<span class="token-comment"># Use case: simple flag (one writer, many readers)</span>

stop_event = threading.Event()  <span class="token-comment"># Acts like a volatile boolean</span>

<span class="token-keyword">def</span> <span class="token-function">worker</span>():
    <span class="token-keyword">while</span> <span class="token-keyword">not</span> stop_event.is_set():  <span class="token-comment"># Always reads latest value</span>
        do_work()

<span class="token-keyword">def</span> <span class="token-function">controller</span>():
    time.sleep(<span class="token-number">5</span>)
    stop_event.set()  <span class="token-comment"># Immediately visible to all threads</span>

<span class="token-comment"># Volatile is sufficient when:</span>
<span class="token-comment"># 1. Only ONE thread writes, others only read</span>
<span class="token-comment"># 2. The write doesn't depend on the current value</span>
<span class="token-comment"># 3. No compound check-then-act operations</span></code></pre>

            <h2>When You Need Synchronized (Locks)</h2>
<pre><code><span class="token-keyword">import</span> threading

counter = <span class="token-number">0</span>
lock = threading.Lock()

<span class="token-comment"># Volatile would NOT fix this — it's a read-modify-write!</span>
<span class="token-keyword">def</span> <span class="token-function">increment</span>():
    <span class="token-keyword">global</span> counter
    <span class="token-keyword">with</span> lock:  <span class="token-comment"># Need atomicity AND visibility</span>
        counter += <span class="token-number">1</span>  <span class="token-comment"># READ + ADD + WRITE must be indivisible</span>

<span class="token-comment"># Synchronized needed when:</span>
<span class="token-comment"># 1. Multiple threads write to the same variable</span>
<span class="token-comment"># 2. Read-modify-write operations (counter++, check-then-act)</span>
<span class="token-comment"># 3. Multiple variables must be consistent together</span></code></pre>

            <h2>Comparison Table</h2>
            <table class="comparison-table">
                <thead><tr><th>Feature</th><th>Volatile</th><th>Synchronized/Lock</th></tr></thead>
                <tbody>
                    <tr><td>Visibility</td><td>Yes</td><td>Yes</td></tr>
                    <tr><td>Atomicity</td><td>Only for single read/write</td><td>Yes (entire block)</td></tr>
                    <tr><td>Blocking</td><td>Never blocks</td><td>Can block waiting threads</td></tr>
                    <tr><td>Performance</td><td>Fast (no lock overhead)</td><td>Slower (acquire/release)</td></tr>
                    <tr><td>Use case</td><td>Flags, status variables</td><td>Counters, state machines, compound ops</td></tr>
                </tbody>
            </table>

            <h2>Python Equivalents</h2>
<pre><code><span class="token-keyword">import</span> threading

<span class="token-comment"># "Volatile" equivalents in Python:</span>
<span class="token-comment"># - threading.Event (boolean flag)</span>
<span class="token-comment"># - queue.Queue (thread-safe communication)</span>
<span class="token-comment"># - Value from multiprocessing (with explicit lock)</span>

<span class="token-comment"># "Synchronized" equivalents:</span>
<span class="token-comment"># - threading.Lock / RLock</span>
<span class="token-comment"># - threading.Condition</span>
<span class="token-comment"># - threading.Semaphore</span>

<span class="token-comment"># Best practice: Use Event for simple signals, Lock for data protection</span>
<span class="token-keyword">class</span> <span class="token-class">SafePublisher</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self):
        self._data = <span class="token-keyword">None</span>
        self._ready = threading.Event()

    <span class="token-keyword">def</span> <span class="token-function">publish</span>(self, value):
        self._data = value
        self._ready.set()  <span class="token-comment"># Memory barrier + signal</span>

    <span class="token-keyword">def</span> <span class="token-function">consume</span>(self):
        self._ready.wait()  <span class="token-comment"># Blocks until set, with memory barrier</span>
        <span class="token-keyword">return</span> self._data  <span class="token-comment"># Guaranteed to see the published value</span></code></pre>

            <div class="industry-box">
                <h4>Language Implementations</h4>
                <ul>
                    <li><strong>Java volatile</strong> — Guarantees visibility, prevents reordering, does NOT provide atomicity for compound ops</li>
                    <li><strong>Java synchronized</strong> — Visibility + atomicity + mutual exclusion</li>
                    <li><strong>C++ volatile</strong> — Only prevents compiler optimization (NOT thread-safe! Use std::atomic instead)</li>
                    <li><strong>Go</strong> — No volatile keyword; use channels or sync/atomic package</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Volatile solves visibility (all threads see latest value) but NOT atomicity</li>
<li>Synchronized (locks) solve both visibility AND atomicity</li>
<li>Use volatile/Event for simple flags with one writer, many readers</li>
<li>Use locks for counter++, check-then-act, and multi-variable updates</li>
<li>C++ volatile is NOT thread-safe — it only prevents compiler optimizations</li>
<li>Python: threading.Event = volatile-like; threading.Lock = synchronized</li>
</ul>""",
    mental_model="""VOLATILE:    Thread A writes → ALL threads see new value immediately
             But: if two threads write simultaneously, last one wins (no ordering)

SYNCHRONIZED: Thread A enters → does work → exits
              Thread B enters → sees ALL of A's changes → does work → exits
              Ordering AND visibility guaranteed!

DECISION:
    Simple flag (stop/start)?  → Event (volatile)
    counter += 1?              → Lock (synchronized)
    check-then-act?            → Lock (synchronized)""",
    mistakes="""<ul>
<li><strong>Using volatile for counter++</strong> — Volatile does NOT make read-modify-write atomic!</li>
<li><strong>C++ volatile for threading</strong> — C++ volatile is for hardware registers, NOT threads. Use std::atomic.</li>
<li><strong>Over-synchronizing</strong> — Using locks when a simple Event/flag would suffice kills performance.</li>
<li><strong>Under-synchronizing</strong> — Using only a flag when compound atomicity is needed causes races.</li>
</ul>""",
    exercise="""<ol>
<li>Implement a stop flag using threading.Event — show it works correctly with 10 worker threads.</li>
<li>Try to use Event instead of Lock for a counter — show it fails.</li>
<li>Build a "double-checked locking" pattern: check flag, then lock, then check again.</li>
<li>Measure performance: Event.is_set() vs lock.acquire()/release() in a tight loop.</li>
</ol>""",
    prev_link="11-happens-before.html", prev_title="Happens-Before",
    next_link="13-false-sharing.html", next_title="False Sharing"
)

# Topic 13
write_topic("13-false-sharing.html",
    title="False Sharing",
    subtitle="When threads working on completely independent data accidentally slow each other down because of how CPU caches work. A hidden performance killer.",
    tags=["advanced","performance","hardware"],
    analogy_title="Roommates Sharing a Fridge Shelf",
    analogy="""<p>Imagine two roommates share one fridge shelf. Person A's food is on the left, Person B's on the right. They never touch each other's food.</p>
<p>But every time A rearranges their food, the <strong>entire shelf shakes</strong> and B has to check if their food moved. And vice versa.</p>
<p>They are not actually sharing anything, but the shared shelf (cache line) means every change forces the other to re-check. This is <strong>false sharing</strong>.</p>""",
    content="""
            <h2>What Is False Sharing?</h2>
            <p>CPUs load memory in chunks called <strong>cache lines</strong> (typically 64 bytes). If two threads modify different variables that happen to sit on the <strong>same cache line</strong>, the CPU must invalidate and reload the entire line for both cores — even though they don't actually share data.</p>

            <h3>Why It Kills Performance</h3>
            <p>Each write by Core 1 forces Core 2 to reload the cache line from memory (~100ns penalty). Multiply by millions of operations = massive slowdown.</p>

<pre><code><span class="token-keyword">import</span> threading
<span class="token-keyword">import</span> time
<span class="token-keyword">import</span> ctypes

<span class="token-comment"># Simulating false sharing impact</span>
<span class="token-comment"># Two counters side by side in memory (same cache line)</span>

<span class="token-keyword">class</span> <span class="token-class">FalseSharingDemo</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self):
        <span class="token-comment"># These are likely on the same cache line (adjacent in memory)</span>
        self.counter_a = <span class="token-number">0</span>
        self.counter_b = <span class="token-number">0</span>

    <span class="token-keyword">def</span> <span class="token-function">increment_a</span>(self):
        <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10_000_000</span>):
            self.counter_a += <span class="token-number">1</span>

    <span class="token-keyword">def</span> <span class="token-function">increment_b</span>(self):
        <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">10_000_000</span>):
            self.counter_b += <span class="token-number">1</span>

<span class="token-comment"># Fix: Add padding between variables</span>
<span class="token-keyword">class</span> <span class="token-class">NoPaddingCounters</span>(ctypes.Structure):
    _fields_ = [
        (<span class="token-string">"a"</span>, ctypes.c_long),  <span class="token-comment"># 8 bytes</span>
        (<span class="token-string">"b"</span>, ctypes.c_long),  <span class="token-comment"># 8 bytes — same cache line as 'a'!</span>
    ]

<span class="token-keyword">class</span> <span class="token-class">PaddedCounters</span>(ctypes.Structure):
    _fields_ = [
        (<span class="token-string">"a"</span>, ctypes.c_long),
        (<span class="token-string">"_pad1"</span>, ctypes.c_byte * <span class="token-number">56</span>),  <span class="token-comment"># Padding to fill cache line</span>
        (<span class="token-string">"b"</span>, ctypes.c_long),               <span class="token-comment"># Now on DIFFERENT cache line!</span>
    ]</code></pre>

            <h2>How to Detect False Sharing</h2>
            <table class="comparison-table">
                <thead><tr><th>Tool</th><th>Platform</th><th>What It Shows</th></tr></thead>
                <tbody>
                    <tr><td><code>perf c2c</code></td><td>Linux</td><td>Cache-to-cache transfers (false sharing indicator)</td></tr>
                    <tr><td><code>Intel VTune</code></td><td>All</td><td>Cache line contention analysis</td></tr>
                    <tr><td><code>perf stat</code></td><td>Linux</td><td>L1 cache miss rate</td></tr>
                </tbody>
            </table>

            <h2>Solutions</h2>
<pre><code><span class="token-comment"># Solution 1: Padding (most common)</span>
<span class="token-keyword">class</span> <span class="token-class">PaddedCounter</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self):
        self.value = <span class="token-number">0</span>
        self._padding = [<span class="token-number">0</span>] * <span class="token-number">7</span>  <span class="token-comment"># Fill rest of 64-byte cache line</span>

<span class="token-comment"># Solution 2: Thread-local accumulation</span>
<span class="token-keyword">def</span> <span class="token-function">worker_with_local_accumulator</span>(shared_result, lock):
    local_count = <span class="token-number">0</span>  <span class="token-comment"># Thread-local — no sharing!</span>
    <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">1_000_000</span>):
        local_count += <span class="token-number">1</span>
    <span class="token-comment"># Only touch shared state once at the end</span>
    <span class="token-keyword">with</span> lock:
        shared_result[<span class="token-number">0</span>] += local_count

<span class="token-comment"># Solution 3: Per-thread arrays with alignment</span>
<span class="token-keyword">import</span> numpy <span class="token-keyword">as</span> np
<span class="token-comment"># Each thread gets its own cache-line-aligned slot</span>
counters = np.zeros(<span class="token-number">64</span>, dtype=np.int64)  <span class="token-comment"># 64 slots, 8 bytes each</span>
<span class="token-comment"># Thread i uses counters[i * 8] — separated by 64 bytes (one cache line)</span></code></pre>

            <div class="industry-box">
                <h4>Real-World Impact</h4>
                <ul>
                    <li><strong>Java @Contended</strong> — Annotation that adds padding to prevent false sharing (used in ConcurrentHashMap)</li>
                    <li><strong>Linux kernel</strong> — ____cacheline_aligned macro pads structures to cache line boundaries</li>
                    <li><strong>LMAX Disruptor</strong> — Sequence counters are padded to avoid false sharing (critical for low-latency trading)</li>
                    <li><strong>Go runtime</strong> — Internal structures use padding to avoid false sharing between goroutines</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>False sharing: independent variables on the same cache line cause invalidation overhead</li>
<li>Cache lines are 64 bytes — variables within 64 bytes of each other share a line</li>
<li>Each write by one core invalidates the line for all other cores</li>
<li>Fix: padding (add dummy bytes), thread-local accumulation, cache-line alignment</li>
<li>Can cause 10-100x slowdown in tight loops on multi-core systems</li>
<li>Use perf c2c or Intel VTune to detect</li>
</ul>""",
    mental_model="""CACHE LINE (64 bytes):
    [counter_a | counter_b | ........... ]
         ↑            ↑
       Core 1       Core 2
    writes here    writes here

    Every write invalidates the ENTIRE line for the other core!

FIX WITH PADDING:
    [counter_a | padding................. ] ← Cache line 1 (Core 1 only)
    [counter_b | padding................. ] ← Cache line 2 (Core 2 only)

    No interference! Each core owns its cache line.""",
    mistakes="""<ul>
<li><strong>Ignoring cache line size</strong> — Putting frequently-written variables next to each other in structs.</li>
<li><strong>Over-padding</strong> — Wasting memory by padding everything. Only pad hot (frequently-written) data.</li>
<li><strong>Not measuring</strong> — Assuming false sharing without profiling. Always measure first.</li>
<li><strong>Python-specific</strong> — Due to GIL, false sharing is less impactful in CPython but critical in C extensions and multiprocessing.</li>
</ul>""",
    exercise="""<ol>
<li>Create two counters in adjacent memory. Increment each from a different thread. Measure time.</li>
<li>Add 64 bytes of padding between them. Measure again. Compare.</li>
<li>Use the thread-local accumulation pattern: accumulate locally, merge once at end. Measure improvement.</li>
<li>Research: what is your CPU's cache line size? (Usually 64 bytes, some ARM = 128 bytes)</li>
</ol>""",
    prev_link="12-volatile-vs-synchronized.html", prev_title="Volatile vs Synchronized",
    next_link="14-thread-pools.html", next_title="Thread Pools"
)

print("\n=== Module 2 (topics 09-13) generation complete ===")
