"""Generate topics 14-20: Concurrency Patterns"""
import sys
sys.path.insert(0, '.')
from gen_template import write_topic

# Topic 14
write_topic("14-thread-pools.html",
    title="Thread Pools",
    subtitle="Instead of creating a new thread for every task (expensive!), keep a pool of reusable worker threads ready to go. The backbone of every web server.",
    tags=["intermediate","pattern","code"],
    analogy_title="A Taxi Stand",
    analogy="""<p>A <strong>thread pool</strong> is like a taxi stand at an airport:</p>
<ul><li>There are 10 taxis waiting (worker threads in the pool)</li>
<li>Passengers arrive (tasks/requests) and take the next available taxi</li>
<li>When the ride is done, the taxi returns to the stand (thread returns to pool)</li>
<li>If all 10 are busy, passengers wait in line (task queue)</li></ul>
<p>You don't build a new taxi for every passenger — that would be absurd. Same with threads.</p>""",
    content="""
            <h2>Why Thread Pools?</h2>
            <table class="comparison-table">
                <thead><tr><th>Approach</th><th>Cost</th><th>Problem</th></tr></thead>
                <tbody>
                    <tr><td>New thread per task</td><td>~1ms + 1MB stack per thread</td><td>10K requests = 10GB RAM + OS overwhelmed</td></tr>
                    <tr><td>Thread pool (fixed)</td><td>Threads created once, reused</td><td>Bounded resources, predictable performance</td></tr>
                </tbody>
            </table>

            <h2>Python ThreadPoolExecutor</h2>
<pre><code><span class="token-keyword">from</span> concurrent.futures <span class="token-keyword">import</span> ThreadPoolExecutor, as_completed
<span class="token-keyword">import</span> time

<span class="token-keyword">def</span> <span class="token-function">fetch_url</span>(url):
    time.sleep(<span class="token-number">1</span>)  <span class="token-comment"># Simulate network I/O</span>
    <span class="token-keyword">return</span> <span class="token-string">f"Response from {url}"</span>

urls = [<span class="token-string">f"https://api.example.com/page/{i}"</span> <span class="token-keyword">for</span> i <span class="token-keyword">in</span> range(<span class="token-number">20</span>)]

<span class="token-comment"># Without pool: 20 seconds (sequential)</span>
<span class="token-comment"># With pool of 5: 4 seconds (5 concurrent)</span>
<span class="token-keyword">with</span> ThreadPoolExecutor(max_workers=<span class="token-number">5</span>) <span class="token-keyword">as</span> executor:
    futures = {executor.submit(fetch_url, url): url <span class="token-keyword">for</span> url <span class="token-keyword">in</span> urls}
    <span class="token-keyword">for</span> future <span class="token-keyword">in</span> as_completed(futures):
        url = futures[future]
        result = future.result()
        print(<span class="token-string">f"{url}: {result}"</span>)

<span class="token-comment"># Using map() for simpler cases</span>
<span class="token-keyword">with</span> ThreadPoolExecutor(max_workers=<span class="token-number">10</span>) <span class="token-keyword">as</span> executor:
    results = list(executor.map(fetch_url, urls))
    print(<span class="token-string">f"Got {len(results)} results"</span>)</code></pre>

            <h2>Pool Sizing: How Many Threads?</h2>
            <div class="callout callout-info">
                <div class="callout-title">The Golden Rules</div>
                <p><strong>CPU-bound work:</strong> threads = number of CPU cores<br>
                <strong>I/O-bound work:</strong> threads = cores * (1 + wait_time/compute_time)<br>
                Example: 4 cores, I/O takes 10x longer than compute → 4 * (1 + 10) = 44 threads</p>
            </div>

<pre><code><span class="token-keyword">import</span> os, multiprocessing

<span class="token-comment"># CPU-bound: use ProcessPoolExecutor with core count</span>
<span class="token-keyword">from</span> concurrent.futures <span class="token-keyword">import</span> ProcessPoolExecutor
cpu_count = os.cpu_count()  <span class="token-comment"># e.g., 8</span>

<span class="token-keyword">with</span> ProcessPoolExecutor(max_workers=cpu_count) <span class="token-keyword">as</span> executor:
    results = list(executor.map(heavy_computation, data))

<span class="token-comment"># I/O-bound: use ThreadPoolExecutor with higher count</span>
<span class="token-keyword">with</span> ThreadPoolExecutor(max_workers=cpu_count * <span class="token-number">10</span>) <span class="token-keyword">as</span> executor:
    results = list(executor.map(fetch_url, urls))</code></pre>

            <h2>Custom Thread Pool Implementation</h2>
<pre><code><span class="token-keyword">import</span> threading
<span class="token-keyword">from</span> queue <span class="token-keyword">import</span> Queue

<span class="token-keyword">class</span> <span class="token-class">SimpleThreadPool</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self, num_workers):
        self.task_queue = Queue()
        self.workers = []
        <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(num_workers):
            t = threading.Thread(target=self._worker, daemon=<span class="token-keyword">True</span>)
            t.start()
            self.workers.append(t)

    <span class="token-keyword">def</span> <span class="token-function">_worker</span>(self):
        <span class="token-keyword">while</span> <span class="token-keyword">True</span>:
            task = self.task_queue.get()
            <span class="token-keyword">if</span> task <span class="token-keyword">is</span> <span class="token-keyword">None</span>: <span class="token-keyword">break</span>
            func, args = task
            <span class="token-keyword">try</span>:
                func(*args)
            <span class="token-keyword">except</span> Exception <span class="token-keyword">as</span> e:
                print(<span class="token-string">f"Task error: {e}"</span>)
            <span class="token-keyword">finally</span>:
                self.task_queue.task_done()

    <span class="token-keyword">def</span> <span class="token-function">submit</span>(self, func, *args):
        self.task_queue.put((func, args))

    <span class="token-keyword">def</span> <span class="token-function">shutdown</span>(self):
        <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> self.workers:
            self.task_queue.put(<span class="token-keyword">None</span>)
        <span class="token-keyword">for</span> t <span class="token-keyword">in</span> self.workers:
            t.join()</code></pre>

            <div class="industry-box">
                <h4>Industry Usage</h4>
                <ul>
                    <li><strong>Nginx</strong> — Worker process pool (not threads, but same concept)</li>
                    <li><strong>Java Tomcat</strong> — Default 200-thread pool for handling HTTP requests</li>
                    <li><strong>Node.js libuv</strong> — 4-thread pool for file I/O operations</li>
                    <li><strong>PostgreSQL</strong> — Connection pool (pgbouncer) limits concurrent connections</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Thread pools reuse a fixed number of threads instead of creating new ones per task</li>
<li>Avoids thread creation overhead (1ms + 1MB per thread)</li>
<li>CPU-bound: pool size = number of cores</li>
<li>I/O-bound: pool size = cores * (1 + wait/compute ratio)</li>
<li>Python: ThreadPoolExecutor for I/O, ProcessPoolExecutor for CPU</li>
<li>All web servers, databases, and network services use thread/process pools</li>
</ul>""",
    mental_model="""THREAD POOL:
    Task Queue: [T1] [T2] [T3] [T4] [T5] [T6] ...
                  ↓    ↓    ↓
    Workers:   [W1]  [W2]  [W3]  [W4]  (idle)
                 ↓    ↓     ↓
              running running running

    W1 finishes → picks up T4 from queue
    W2 finishes → picks up T5 from queue

SIZING:
    CPU-bound: workers = cores (more = context switch overhead)
    I/O-bound: workers = cores * (1 + IO_time/CPU_time)""",
    mistakes="""<ul>
<li><strong>Too many threads</strong> — 1000 threads for CPU-bound work = massive context switching overhead.</li>
<li><strong>Too few threads</strong> — 2 threads for I/O-bound work with 100ms latency = most time spent waiting.</li>
<li><strong>Not handling exceptions</strong> — Unhandled exception in a pool thread kills that worker silently.</li>
<li><strong>Using ThreadPool for CPU-bound in Python</strong> — GIL means no parallelism. Use ProcessPoolExecutor.</li>
</ul>""",
    exercise="""<ol>
<li>Build a custom thread pool (queue + worker threads). Submit 100 tasks.</li>
<li>Benchmark ThreadPoolExecutor with 1, 4, 16, 64 workers fetching 100 URLs.</li>
<li>Show that ProcessPoolExecutor is faster for CPU-bound work (compute Fibonacci).</li>
<li>Implement graceful shutdown: finish current tasks, reject new ones, then stop.</li>
</ol>""",
    prev_link="13-false-sharing.html", prev_title="False Sharing",
    next_link="15-futures-promises-async.html", next_title="Futures & Async"
)

# Topic 15
write_topic("15-futures-promises-async.html",
    title="Futures, Promises &amp; Async/Await",
    subtitle="A way to say 'start this task now, I will collect the result later.' The foundation of non-blocking programming in every modern language.",
    tags=["intermediate","pattern","code"],
    analogy_title="Ordering Food at a Restaurant",
    analogy="""<p><strong>Future/Promise</strong>: You order food (submit a task). The waiter gives you a <strong>buzzer</strong> (the Future object). You can go do other things. When the buzzer goes off, your food is ready (result available).</p>
<p><strong>Async/Await</strong>: Same restaurant, but you say "I will wait here but let other customers order while my food cooks." You pause (await), others proceed, and you resume when ready.</p>""",
    content="""
            <h2>Futures: A Placeholder for a Result</h2>
<pre><code><span class="token-keyword">from</span> concurrent.futures <span class="token-keyword">import</span> ThreadPoolExecutor, Future
<span class="token-keyword">import</span> time

<span class="token-keyword">def</span> <span class="token-function">slow_api_call</span>(user_id):
    time.sleep(<span class="token-number">2</span>)
    <span class="token-keyword">return</span> {<span class="token-string">"id"</span>: user_id, <span class="token-string">"name"</span>: <span class="token-string">f"User {user_id}"</span>}

executor = ThreadPoolExecutor(max_workers=<span class="token-number">4</span>)

<span class="token-comment"># Submit returns a Future immediately (non-blocking)</span>
future = executor.submit(slow_api_call, <span class="token-number">42</span>)
print(<span class="token-string">f"Is done? {future.done()}"</span>)  <span class="token-comment"># False — still running</span>

<span class="token-comment"># Do other work while waiting...</span>
print(<span class="token-string">"Doing other things..."</span>)

<span class="token-comment"># Block until result is ready</span>
result = future.result(timeout=<span class="token-number">5</span>)  <span class="token-comment"># Waits up to 5s</span>
print(<span class="token-string">f"Got: {result}"</span>)

<span class="token-comment"># Callback approach (don't block at all)</span>
<span class="token-keyword">def</span> <span class="token-function">on_complete</span>(fut):
    print(<span class="token-string">f"Callback received: {fut.result()}"</span>)

future2 = executor.submit(slow_api_call, <span class="token-number">99</span>)
future2.add_done_callback(on_complete)</code></pre>

            <h2>Async/Await: Cooperative Multitasking</h2>
<pre><code><span class="token-keyword">import</span> asyncio

<span class="token-keyword">async</span> <span class="token-keyword">def</span> <span class="token-function">fetch_user</span>(user_id):
    print(<span class="token-string">f"Fetching user {user_id}..."</span>)
    <span class="token-keyword">await</span> asyncio.sleep(<span class="token-number">1</span>)  <span class="token-comment"># Non-blocking sleep (simulates I/O)</span>
    <span class="token-keyword">return</span> {<span class="token-string">"id"</span>: user_id, <span class="token-string">"name"</span>: <span class="token-string">f"User {user_id}"</span>}

<span class="token-keyword">async</span> <span class="token-keyword">def</span> <span class="token-function">fetch_order</span>(order_id):
    <span class="token-keyword">await</span> asyncio.sleep(<span class="token-number">1.5</span>)
    <span class="token-keyword">return</span> {<span class="token-string">"order"</span>: order_id, <span class="token-string">"total"</span>: <span class="token-number">99.99</span>}

<span class="token-keyword">async</span> <span class="token-keyword">def</span> <span class="token-function">main</span>():
    <span class="token-comment"># Run BOTH concurrently — total time: 1.5s (not 2.5s!)</span>
    user, order = <span class="token-keyword">await</span> asyncio.gather(
        fetch_user(<span class="token-number">1</span>),
        fetch_order(<span class="token-number">100</span>)
    )
    print(<span class="token-string">f"User: {user}, Order: {order}"</span>)

asyncio.run(main())</code></pre>

            <h2>Futures vs Async/Await</h2>
            <table class="comparison-table">
                <thead><tr><th>Feature</th><th>Futures (ThreadPool)</th><th>Async/Await</th></tr></thead>
                <tbody>
                    <tr><td>Concurrency model</td><td>Multi-threaded (OS threads)</td><td>Single-threaded (event loop)</td></tr>
                    <tr><td>Overhead per task</td><td>~1MB (thread stack)</td><td>~1KB (coroutine frame)</td></tr>
                    <tr><td>Max concurrency</td><td>~1000 threads</td><td>~100,000 coroutines</td></tr>
                    <tr><td>Best for</td><td>CPU-bound, blocking I/O libs</td><td>Many I/O-bound tasks</td></tr>
                    <tr><td>Complexity</td><td>Simpler (familiar threading)</td><td>Requires async ecosystem</td></tr>
                </tbody>
            </table>

            <h2>Error Handling in Async</h2>
<pre><code><span class="token-keyword">async</span> <span class="token-keyword">def</span> <span class="token-function">risky_operation</span>():
    <span class="token-keyword">await</span> asyncio.sleep(<span class="token-number">1</span>)
    <span class="token-keyword">raise</span> ValueError(<span class="token-string">"Something went wrong"</span>)

<span class="token-keyword">async</span> <span class="token-keyword">def</span> <span class="token-function">safe_main</span>():
    <span class="token-keyword">try</span>:
        result = <span class="token-keyword">await</span> risky_operation()
    <span class="token-keyword">except</span> ValueError <span class="token-keyword">as</span> e:
        print(<span class="token-string">f"Caught: {e}"</span>)

    <span class="token-comment"># With gather: exceptions are returned, not raised</span>
    results = <span class="token-keyword">await</span> asyncio.gather(
        fetch_user(<span class="token-number">1</span>),
        risky_operation(),
        return_exceptions=<span class="token-keyword">True</span>
    )
    <span class="token-keyword">for</span> r <span class="token-keyword">in</span> results:
        <span class="token-keyword">if</span> isinstance(r, Exception):
            print(<span class="token-string">f"Failed: {r}"</span>)
        <span class="token-keyword">else</span>:
            print(<span class="token-string">f"Success: {r}"</span>)</code></pre>

            <div class="industry-box">
                <h4>Industry Usage</h4>
                <ul>
                    <li><strong>FastAPI</strong> — async/await for handling thousands of concurrent HTTP requests</li>
                    <li><strong>Node.js</strong> — Entire runtime built on Promises and async/await</li>
                    <li><strong>Rust tokio</strong> — Async runtime handling millions of concurrent connections</li>
                    <li><strong>Java CompletableFuture</strong> — Chainable futures with thenApply(), thenCompose()</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Future: a placeholder for a result that will be available later</li>
<li>Async/await: cooperative multitasking on a single thread (event loop)</li>
<li>Futures use real OS threads (~1MB each); coroutines use ~1KB each</li>
<li>Use asyncio.gather() to run multiple async operations concurrently</li>
<li>Futures for blocking libraries; async for I/O-heavy async-compatible code</li>
<li>Always handle exceptions in futures (they are swallowed silently otherwise)</li>
</ul>""",
    mental_model="""FUTURE:
    submit(task) → [Future: pending...]
    ... do other work ...
    future.result() → [Future: DONE] → actual result

ASYNC/AWAIT:
    Event Loop: ─── run A ─── A awaits (pauses) ─── run B ─── B awaits ─── resume A ───
    Single thread, multiple tasks interleaved at await points.

    Sequential:    |--A (1s)--|--B (1s)--|  = 2s total
    Concurrent:    |--A--|
                   |--B--|                   = 1s total (overlapping I/O)""",
    mistakes="""<ul>
<li><strong>Blocking inside async function</strong> — time.sleep() blocks the entire event loop! Use await asyncio.sleep().</li>
<li><strong>Not awaiting coroutines</strong> — Calling async_func() without await = coroutine never runs.</li>
<li><strong>Mixing sync and async</strong> — Calling sync blocking code inside async without run_in_executor().</li>
<li><strong>Forgetting to check future exceptions</strong> — Exceptions in futures are lost unless you call .result().</li>
</ul>""",
    exercise="""<ol>
<li>Submit 10 tasks to ThreadPoolExecutor. Use as_completed() to print results as they finish.</li>
<li>Rewrite the same with asyncio: 10 async tasks with asyncio.gather().</li>
<li>Benchmark: ThreadPoolExecutor vs asyncio for 1000 simulated HTTP requests.</li>
<li>Implement a timeout: cancel a future if it takes more than 3 seconds.</li>
</ol>""",
    prev_link="14-thread-pools.html", prev_title="Thread Pools",
    next_link="16-producer-consumer.html", next_title="Producer-Consumer"
)

# Topic 16
write_topic("16-producer-consumer.html",
    title="Producer-Consumer Pattern",
    subtitle="One of the most important patterns in all of computing: one side creates work, the other side processes it, with a buffer in between.",
    tags=["intermediate","pattern","code"],
    analogy_title="The Assembly Line",
    analogy="""<p>A factory assembly line: one station <strong>makes parts</strong> (producer) and places them on a <strong>conveyor belt</strong> (queue). Another station <strong>assembles</strong> them (consumer).</p>
<ul><li>If the belt is full, the maker pauses (backpressure)</li>
<li>If the belt is empty, the assembler waits</li>
<li>The belt decouples production speed from consumption speed</li></ul>""",
    content="""
            <h2>The Pattern</h2>
<pre><code><span class="token-keyword">import</span> threading
<span class="token-keyword">from</span> queue <span class="token-keyword">import</span> Queue
<span class="token-keyword">import</span> time, random

<span class="token-keyword">def</span> <span class="token-function">producer</span>(q, name):
    <span class="token-keyword">for</span> i <span class="token-keyword">in</span> range(<span class="token-number">10</span>):
        item = <span class="token-string">f"{name}-item-{i}"</span>
        q.put(item)  <span class="token-comment"># Blocks if queue is full</span>
        print(<span class="token-string">f"[{name}] Produced: {item}"</span>)
        time.sleep(random.uniform(<span class="token-number">0.1</span>, <span class="token-number">0.5</span>))

<span class="token-keyword">def</span> <span class="token-function">consumer</span>(q, name):
    <span class="token-keyword">while</span> <span class="token-keyword">True</span>:
        item = q.get()  <span class="token-comment"># Blocks if queue is empty</span>
        <span class="token-keyword">if</span> item <span class="token-keyword">is</span> <span class="token-keyword">None</span>:  <span class="token-comment"># Poison pill = shutdown signal</span>
            <span class="token-keyword">break</span>
        print(<span class="token-string">f"  [{name}] Consumed: {item}"</span>)
        time.sleep(random.uniform(<span class="token-number">0.2</span>, <span class="token-number">0.8</span>))
        q.task_done()

<span class="token-comment"># Bounded queue (max 5 items) provides backpressure</span>
buffer = Queue(maxsize=<span class="token-number">5</span>)

<span class="token-comment"># Multiple producers and consumers</span>
producers = [threading.Thread(target=producer, args=(buffer, <span class="token-string">f"P{i}"</span>)) <span class="token-keyword">for</span> i <span class="token-keyword">in</span> range(<span class="token-number">3</span>)]
consumers = [threading.Thread(target=consumer, args=(buffer, <span class="token-string">f"C{i}"</span>)) <span class="token-keyword">for</span> i <span class="token-keyword">in</span> range(<span class="token-number">2</span>)]

<span class="token-keyword">for</span> t <span class="token-keyword">in</span> producers + consumers: t.start()
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> producers: t.join()

<span class="token-comment"># Send poison pills to stop consumers</span>
<span class="token-keyword">for</span> _ <span class="token-keyword">in</span> consumers: buffer.put(<span class="token-keyword">None</span>)
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> consumers: t.join()</code></pre>

            <h2>Bounded vs Unbounded Queues</h2>
            <table class="comparison-table">
                <thead><tr><th>Type</th><th>Behavior when full</th><th>Risk</th><th>Use case</th></tr></thead>
                <tbody>
                    <tr><td><strong>Bounded</strong></td><td>Producer blocks (backpressure)</td><td>Producer slowdown</td><td>Production systems (safe)</td></tr>
                    <tr><td><strong>Unbounded</strong></td><td>Never blocks, grows forever</td><td>OOM (out of memory)</td><td>Low-volume, trusted input</td></tr>
                </tbody>
            </table>

            <h2>Async Version</h2>
<pre><code><span class="token-keyword">import</span> asyncio

<span class="token-keyword">async</span> <span class="token-keyword">def</span> <span class="token-function">async_producer</span>(queue, name):
    <span class="token-keyword">for</span> i <span class="token-keyword">in</span> range(<span class="token-number">10</span>):
        <span class="token-keyword">await</span> queue.put(<span class="token-string">f"{name}-{i}"</span>)
        <span class="token-keyword">await</span> asyncio.sleep(<span class="token-number">0.1</span>)

<span class="token-keyword">async</span> <span class="token-keyword">def</span> <span class="token-function">async_consumer</span>(queue, name):
    <span class="token-keyword">while</span> <span class="token-keyword">True</span>:
        item = <span class="token-keyword">await</span> queue.get()
        <span class="token-keyword">if</span> item <span class="token-keyword">is</span> <span class="token-keyword">None</span>: <span class="token-keyword">break</span>
        print(<span class="token-string">f"[{name}] Processing: {item}"</span>)
        <span class="token-keyword">await</span> asyncio.sleep(<span class="token-number">0.2</span>)

<span class="token-keyword">async</span> <span class="token-keyword">def</span> <span class="token-function">main</span>():
    queue = asyncio.Queue(maxsize=<span class="token-number">5</span>)
    producers = [async_producer(queue, <span class="token-string">f"P{i}"</span>) <span class="token-keyword">for</span> i <span class="token-keyword">in</span> range(<span class="token-number">3</span>)]
    consumers = [async_consumer(queue, <span class="token-string">f"C{i}"</span>) <span class="token-keyword">for</span> i <span class="token-keyword">in</span> range(<span class="token-number">2</span>)]
    <span class="token-keyword">await</span> asyncio.gather(*producers)
    <span class="token-keyword">for</span> _ <span class="token-keyword">in</span> range(<span class="token-number">2</span>): <span class="token-keyword">await</span> queue.put(<span class="token-keyword">None</span>)
    <span class="token-keyword">await</span> asyncio.gather(*consumers)

asyncio.run(main())</code></pre>

            <div class="industry-box">
                <h4>Everywhere in Industry</h4>
                <ul>
                    <li><strong>Kafka</strong> — Producers publish messages, consumers process them (millions/sec)</li>
                    <li><strong>RabbitMQ/SQS</strong> — Message queues are exactly this pattern</li>
                    <li><strong>Web servers</strong> — Accept connections (producer) → worker pool processes (consumer)</li>
                    <li><strong>ETL pipelines</strong> — Extract (produce) → Transform/Load (consume)</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Producer creates data/tasks; consumer processes them; queue buffers in between</li>
<li>Bounded queue provides backpressure (producer slows down when consumer is slow)</li>
<li>Unbounded queue risks OOM — always prefer bounded in production</li>
<li>Use poison pill (None) or Event to signal shutdown</li>
<li>Python: queue.Queue (threads), asyncio.Queue (async)</li>
<li>Every message broker (Kafka, RabbitMQ, SQS) is this pattern at scale</li>
</ul>""",
    mental_model="""Producer → [Queue/Buffer] → Consumer

    P1 ──┐
    P2 ──┤──→ [ _ _ _ _ _ ] ──→ C1
    P3 ──┘    (bounded: 5)       C2

    Queue full?  → Producers BLOCK (backpressure)
    Queue empty? → Consumers BLOCK (wait for work)""",
    mistakes="""<ul>
<li><strong>Unbounded queue in production</strong> — If consumers are slower, queue grows until OOM crash.</li>
<li><strong>No shutdown mechanism</strong> — Consumers loop forever. Use poison pill or Event for graceful stop.</li>
<li><strong>Single consumer bottleneck</strong> — If processing is slow, add more consumers.</li>
<li><strong>Not calling task_done()</strong> — queue.join() will hang forever if task_done() is not called.</li>
</ul>""",
    exercise="""<ol>
<li>Build producer-consumer with 3 producers, 2 consumers, bounded queue of 5.</li>
<li>Add monitoring: print queue size every second to see backpressure in action.</li>
<li>Implement priority queue: urgent items processed before normal ones.</li>
<li>Add error handling: if consumer fails on an item, put it in a dead-letter queue.</li>
</ol>""",
    prev_link="15-futures-promises-async.html", prev_title="Futures & Async",
    next_link="17-blocking-vs-nonblocking.html", next_title="Blocking vs Non-Blocking"
)

# Topic 17
write_topic("17-blocking-vs-nonblocking.html",
    title="Blocking vs Non-Blocking I/O",
    subtitle="Should your thread wait for data or check and move on? The choice that determines whether your server handles 100 or 100,000 connections.",
    tags=["intermediate","concept","code"],
    analogy_title="Waiting for a Package",
    analogy="""<p><strong>Blocking</strong>: You sit by the door all day waiting for the delivery. You cannot do anything else until it arrives.</p>
<p><strong>Non-blocking</strong>: You check the door, see nothing, and go back to work. Check again in 5 minutes. Repeat.</p>
<p><strong>Async (event-driven)</strong>: You put a doorbell on. You do other work freely. When the package arrives, the bell rings and you go get it.</p>""",
    content="""
            <h2>I/O Models Compared</h2>
            <table class="comparison-table">
                <thead><tr><th>Model</th><th>Thread does while waiting</th><th>Max connections</th><th>Complexity</th></tr></thead>
                <tbody>
                    <tr><td><strong>Blocking</strong></td><td>Nothing (sleeps)</td><td>~1000 (one thread per conn)</td><td>Simple</td></tr>
                    <tr><td><strong>Non-blocking poll</strong></td><td>Checks repeatedly (busy wait)</td><td>~10K</td><td>Medium</td></tr>
                    <tr><td><strong>I/O Multiplexing</strong></td><td>Waits for ANY of many sockets</td><td>~100K (select/poll/epoll)</td><td>Complex</td></tr>
                    <tr><td><strong>Async (event loop)</strong></td><td>Processes other events</td><td>~1M</td><td>Highest</td></tr>
                </tbody>
            </table>

            <h2>Blocking I/O (Traditional)</h2>
<pre><code><span class="token-keyword">import</span> socket, threading

<span class="token-keyword">def</span> <span class="token-function">handle_client</span>(conn):
    <span class="token-keyword">while</span> <span class="token-keyword">True</span>:
        data = conn.recv(<span class="token-number">1024</span>)  <span class="token-comment"># BLOCKS until data arrives</span>
        <span class="token-keyword">if</span> <span class="token-keyword">not</span> data: <span class="token-keyword">break</span>
        conn.sendall(data.upper())  <span class="token-comment"># BLOCKS until sent</span>
    conn.close()

<span class="token-comment"># One thread per connection — doesn't scale past ~1000</span>
server = socket.socket()
server.bind((<span class="token-string">"0.0.0.0"</span>, <span class="token-number">8080</span>))
server.listen()
<span class="token-keyword">while</span> <span class="token-keyword">True</span>:
    conn, addr = server.accept()  <span class="token-comment"># BLOCKS until new connection</span>
    threading.Thread(target=handle_client, args=(conn,)).start()</code></pre>

            <h2>Non-Blocking with Select (I/O Multiplexing)</h2>
<pre><code><span class="token-keyword">import</span> select, socket

server = socket.socket()
server.setblocking(<span class="token-keyword">False</span>)
server.bind((<span class="token-string">"0.0.0.0"</span>, <span class="token-number">8080</span>))
server.listen()

sockets = [server]

<span class="token-keyword">while</span> <span class="token-keyword">True</span>:
    <span class="token-comment"># Wait for ANY socket to be ready (single thread, many connections!)</span>
    readable, _, _ = select.select(sockets, [], [], <span class="token-number">1.0</span>)
    <span class="token-keyword">for</span> sock <span class="token-keyword">in</span> readable:
        <span class="token-keyword">if</span> sock <span class="token-keyword">is</span> server:
            conn, addr = server.accept()
            conn.setblocking(<span class="token-keyword">False</span>)
            sockets.append(conn)
        <span class="token-keyword">else</span>:
            data = sock.recv(<span class="token-number">1024</span>)
            <span class="token-keyword">if</span> data:
                sock.sendall(data.upper())
            <span class="token-keyword">else</span>:
                sockets.remove(sock)
                sock.close()</code></pre>

            <h2>Async I/O (Modern Approach)</h2>
<pre><code><span class="token-keyword">import</span> asyncio

<span class="token-keyword">async</span> <span class="token-keyword">def</span> <span class="token-function">handle_client</span>(reader, writer):
    <span class="token-keyword">while</span> <span class="token-keyword">True</span>:
        data = <span class="token-keyword">await</span> reader.read(<span class="token-number">1024</span>)  <span class="token-comment"># Non-blocking read</span>
        <span class="token-keyword">if</span> <span class="token-keyword">not</span> data: <span class="token-keyword">break</span>
        writer.write(data.upper())
        <span class="token-keyword">await</span> writer.drain()  <span class="token-comment"># Non-blocking write</span>
    writer.close()

<span class="token-keyword">async</span> <span class="token-keyword">def</span> <span class="token-function">main</span>():
    server = <span class="token-keyword">await</span> asyncio.start_server(handle_client, <span class="token-string">"0.0.0.0"</span>, <span class="token-number">8080</span>)
    <span class="token-keyword">async</span> <span class="token-keyword">with</span> server:
        <span class="token-keyword">await</span> server.serve_forever()
<span class="token-comment"># Handles 100K+ connections with ONE thread!</span>
asyncio.run(main())</code></pre>

            <div class="industry-box">
                <h4>Industry Choices</h4>
                <ul>
                    <li><strong>Nginx</strong> — Event-driven, non-blocking (handles 10K+ connections per worker)</li>
                    <li><strong>Apache</strong> — Traditional blocking (one thread per connection, prefork/worker MPM)</li>
                    <li><strong>Node.js</strong> — Single-threaded event loop (non-blocking I/O)</li>
                    <li><strong>Go</strong> — Goroutines with non-blocking I/O under the hood (feels blocking, scales like non-blocking)</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Blocking: thread sleeps until I/O completes. Simple but wastes threads.</li>
<li>Non-blocking poll: check and retry. Wastes CPU cycles.</li>
<li>I/O multiplexing (select/epoll): one thread monitors many connections efficiently.</li>
<li>Async/event loop: one thread handles thousands of connections via callbacks/coroutines.</li>
<li>Blocking = ~1K connections. Async = ~100K+ connections.</li>
<li>Go gives the best of both: blocking syntax with non-blocking performance.</li>
</ul>""",
    mental_model="""BLOCKING (1 thread per connection):
    Thread 1: ── [wait for data] ────── [process] ── [wait] ──
    Thread 2: ── [wait for data] ── [process] ── [wait] ──────
    (1000 connections = 1000 threads = 1GB RAM)

ASYNC (1 thread, many connections):
    Event Loop: check A → nothing. check B → data! process B.
                check C → data! process C. check A → data! process A.
    (100K connections = 1 thread = minimal RAM)""",
    mistakes="""<ul>
<li><strong>Blocking calls in async code</strong> — One blocking call halts ALL connections on that event loop.</li>
<li><strong>Thread-per-connection at scale</strong> — Works for 100 connections, crashes at 10K.</li>
<li><strong>Busy-waiting (polling without sleep)</strong> — Burns 100% CPU doing nothing useful.</li>
<li><strong>Not using epoll/kqueue</strong> — select() is O(n) per call. epoll is O(1). Huge difference at scale.</li>
</ul>""",
    exercise="""<ol>
<li>Build a blocking echo server. Test with 100 simultaneous connections (telnet/nc).</li>
<li>Build the same with asyncio. Compare resource usage.</li>
<li>Implement a select-based server that handles multiple clients with one thread.</li>
<li>Benchmark: measure max connections before performance degrades for each approach.</li>
</ol>""",
    prev_link="16-producer-consumer.html", prev_title="Producer-Consumer",
    next_link="18-lock-free-wait-free.html", next_title="Lock-Free Algorithms"
)

# Topic 18
write_topic("18-lock-free-wait-free.html",
    title="Lock-Free &amp; Wait-Free Algorithms",
    subtitle="Data structures that work correctly under concurrency WITHOUT any locks. Maximum performance, maximum difficulty.",
    tags=["advanced","concept","code"],
    analogy_title="The Self-Service Gas Station",
    analogy="""<p><strong>Lock-based</strong>: Only one car can use the pump at a time. Others queue up.</p>
<p><strong>Lock-free</strong>: Multiple cars can try to pump simultaneously. If two grab the same nozzle, one retries. At least one always makes progress.</p>
<p><strong>Wait-free</strong>: Every car is GUARANTEED to finish pumping within a bounded number of steps. No starvation possible.</p>""",
    content="""
            <h2>Progress Guarantees</h2>
            <table class="comparison-table">
                <thead><tr><th>Level</th><th>Guarantee</th><th>Performance</th><th>Difficulty</th></tr></thead>
                <tbody>
                    <tr><td><strong>Blocking (locks)</strong></td><td>None — can deadlock</td><td>Good in low contention</td><td>Easy</td></tr>
                    <tr><td><strong>Lock-free</strong></td><td>At least ONE thread progresses</td><td>Great under contention</td><td>Hard</td></tr>
                    <tr><td><strong>Wait-free</strong></td><td>ALL threads progress in bounded steps</td><td>Best worst-case</td><td>Extremely hard</td></tr>
                </tbody>
            </table>

            <h2>Lock-Free Stack (using CAS)</h2>
<pre><code><span class="token-keyword">import</span> threading

<span class="token-keyword">class</span> <span class="token-class">Node</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self, value, next_node=<span class="token-keyword">None</span>):
        self.value = value
        self.next = next_node

<span class="token-keyword">class</span> <span class="token-class">LockFreeStack</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self):
        self._top = <span class="token-keyword">None</span>
        self._lock = threading.Lock()  <span class="token-comment"># Simulates CAS</span>

    <span class="token-keyword">def</span> <span class="token-function">_cas</span>(self, expected, new_value):
        <span class="token-keyword">with</span> self._lock:
            <span class="token-keyword">if</span> self._top <span class="token-keyword">is</span> expected:
                self._top = new_value
                <span class="token-keyword">return</span> <span class="token-keyword">True</span>
            <span class="token-keyword">return</span> <span class="token-keyword">False</span>

    <span class="token-keyword">def</span> <span class="token-function">push</span>(self, value):
        <span class="token-keyword">while</span> <span class="token-keyword">True</span>:
            old_top = self._top
            new_node = Node(value, old_top)
            <span class="token-keyword">if</span> self._cas(old_top, new_node):
                <span class="token-keyword">return</span>  <span class="token-comment"># Success!</span>
            <span class="token-comment"># CAS failed — someone else pushed. Retry.</span>

    <span class="token-keyword">def</span> <span class="token-function">pop</span>(self):
        <span class="token-keyword">while</span> <span class="token-keyword">True</span>:
            old_top = self._top
            <span class="token-keyword">if</span> old_top <span class="token-keyword">is</span> <span class="token-keyword">None</span>:
                <span class="token-keyword">return</span> <span class="token-keyword">None</span>
            new_top = old_top.next
            <span class="token-keyword">if</span> self._cas(old_top, new_top):
                <span class="token-keyword">return</span> old_top.value  <span class="token-comment"># Success!</span>
            <span class="token-comment"># CAS failed — retry</span></code></pre>

            <h2>When to Use Lock-Free</h2>
            <div class="callout callout-info">
                <div class="callout-title">Decision Guide</div>
                <p><strong>Use locks</strong> when: correctness matters more than speed, low contention, complex operations.<br>
                <strong>Use lock-free</strong> when: high contention, real-time requirements (cannot afford to block), simple operations (counter, stack, queue).</p>
            </div>

            <div class="industry-box">
                <h4>Industry Usage</h4>
                <ul>
                    <li><strong>Java ConcurrentLinkedQueue</strong> — Lock-free queue using CAS (Michael-Scott algorithm)</li>
                    <li><strong>LMAX Disruptor</strong> — Lock-free ring buffer for ultra-low-latency trading (millions msgs/sec)</li>
                    <li><strong>Linux kernel RCU</strong> — Read-Copy-Update: readers never block, writers do the work</li>
                    <li><strong>Intel TBB</strong> — Lock-free concurrent containers for C++</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Lock-free: at least one thread always makes progress (no deadlock possible)</li>
<li>Wait-free: ALL threads make progress in bounded steps (strongest guarantee)</li>
<li>Built on CAS (Compare-And-Swap) retry loops</li>
<li>Faster than locks under high contention but much harder to implement correctly</li>
<li>Use for simple structures: counters, stacks, queues</li>
<li>Not worth it for complex operations — locks are simpler and usually fast enough</li>
</ul>""",
    mental_model="""LOCK-BASED:
    Thread A: [acquire lock] → work → [release]
    Thread B: [waiting......] → [acquire] → work → [release]
    Risk: A holds lock forever = B stuck forever (deadlock)

LOCK-FREE (CAS loop):
    Thread A: read → compute → CAS(success!) → done
    Thread B: read → compute → CAS(FAIL! retry) → read → compute → CAS(success!) → done
    Guarantee: At least one thread always succeeds per round""",
    mistakes="""<ul>
<li><strong>Using lock-free when not needed</strong> — Locks are simpler and often fast enough. Profile first.</li>
<li><strong>ABA problem</strong> — CAS can succeed incorrectly if value changes A→B→A. Use version counters.</li>
<li><strong>Memory reclamation</strong> — When can you safely free a popped node? Other threads might still read it.</li>
<li><strong>Testing difficulty</strong> — Lock-free bugs are extremely rare and hard to reproduce. Formal verification needed.</li>
</ul>""",
    exercise="""<ol>
<li>Implement a lock-free counter using CAS retry loop. Test with 10 threads.</li>
<li>Implement a lock-free stack (push/pop). Verify correctness under contention.</li>
<li>Benchmark: lock-free stack vs lock-based stack with 10 threads, 1M operations.</li>
<li>Demonstrate ABA problem with a lock-free stack (hint: pop node, push it back).</li>
</ol>""",
    prev_link="17-blocking-vs-nonblocking.html", prev_title="Blocking vs Non-Blocking",
    next_link="19-read-write-locks.html", next_title="Read-Write Locks"
)

# Topic 19
write_topic("19-read-write-locks.html",
    title="Read-Write Locks",
    subtitle="Allow multiple readers simultaneously but only one writer at a time. Perfect when reads vastly outnumber writes (which is most systems!).",
    tags=["intermediate","pattern","code"],
    analogy_title="A Library Reading Room",
    analogy="""<p>A library reading room with a special book:</p>
<ul><li><strong>Many people can read</strong> the book simultaneously (readers don't conflict)</li>
<li>But when someone needs to <strong>edit/update</strong> the book, everyone else must leave the room</li>
<li>While the editor works, no readers are allowed in</li>
<li>Once done editing, readers can come back in</li></ul>""",
    content="""
            <h2>Why Read-Write Locks?</h2>
            <p>A regular mutex blocks everyone — even readers who could safely run together. Read-write locks (RWLock) exploit the fact that concurrent reads are safe.</p>

            <table class="comparison-table">
                <thead><tr><th>Scenario</th><th>Regular Lock</th><th>Read-Write Lock</th></tr></thead>
                <tbody>
                    <tr><td>5 readers, 0 writers</td><td>Sequential (slow)</td><td>All 5 simultaneous (fast!)</td></tr>
                    <tr><td>1 writer working</td><td>Others wait</td><td>Others wait (same)</td></tr>
                    <tr><td>95% reads, 5% writes</td><td>All sequential</td><td>95% concurrent!</td></tr>
                </tbody>
            </table>

<pre><code><span class="token-keyword">import</span> threading
<span class="token-keyword">import</span> time

<span class="token-keyword">class</span> <span class="token-class">ReadWriteLock</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self):
        self._readers = <span class="token-number">0</span>
        self._lock = threading.Lock()
        self._write_lock = threading.Lock()

    <span class="token-keyword">def</span> <span class="token-function">acquire_read</span>(self):
        <span class="token-keyword">with</span> self._lock:
            self._readers += <span class="token-number">1</span>
            <span class="token-keyword">if</span> self._readers == <span class="token-number">1</span>:
                self._write_lock.acquire()  <span class="token-comment"># First reader blocks writers</span>

    <span class="token-keyword">def</span> <span class="token-function">release_read</span>(self):
        <span class="token-keyword">with</span> self._lock:
            self._readers -= <span class="token-number">1</span>
            <span class="token-keyword">if</span> self._readers == <span class="token-number">0</span>:
                self._write_lock.release()  <span class="token-comment"># Last reader unblocks writers</span>

    <span class="token-keyword">def</span> <span class="token-function">acquire_write</span>(self):
        self._write_lock.acquire()

    <span class="token-keyword">def</span> <span class="token-function">release_write</span>(self):
        self._write_lock.release()

<span class="token-comment"># Usage</span>
rwlock = ReadWriteLock()
cache = {<span class="token-string">"key"</span>: <span class="token-string">"value"</span>}

<span class="token-keyword">def</span> <span class="token-function">reader</span>(name):
    rwlock.acquire_read()
    <span class="token-keyword">try</span>:
        print(<span class="token-string">f"[{name}] Reading: {cache}"</span>)
        time.sleep(<span class="token-number">0.5</span>)  <span class="token-comment"># Multiple readers here simultaneously!</span>
    <span class="token-keyword">finally</span>:
        rwlock.release_read()

<span class="token-keyword">def</span> <span class="token-function">writer</span>(name, value):
    rwlock.acquire_write()
    <span class="token-keyword">try</span>:
        cache[<span class="token-string">"key"</span>] = value
        print(<span class="token-string">f"[{name}] Wrote: {value}"</span>)
        time.sleep(<span class="token-number">0.2</span>)
    <span class="token-keyword">finally</span>:
        rwlock.release_write()</code></pre>

            <h2>Reader vs Writer Priority</h2>
            <div class="callout callout-warning">
                <div class="callout-title">Starvation Risk!</div>
                <p><strong>Reader-preferring</strong>: New readers keep entering → writer waits forever (writer starvation).<br>
                <strong>Writer-preferring</strong>: Waiting writer blocks new readers → readers starve.<br>
                <strong>Fair</strong>: Alternates between readers and writers (most complex).</p>
            </div>

            <div class="industry-box">
                <h4>Industry Usage</h4>
                <ul>
                    <li><strong>Database query caches</strong> — Many SELECT queries (read) vs occasional UPDATE (write)</li>
                    <li><strong>DNS caches</strong> — Millions of lookups (read) vs rare record updates (write)</li>
                    <li><strong>Configuration stores</strong> — Read constantly, update occasionally</li>
                    <li><strong>Go sync.RWMutex</strong> — Built-in read-write lock, writer-preferring</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>RWLock: multiple simultaneous readers OR one exclusive writer</li>
<li>Huge speedup when reads >> writes (90%+ reads = common case)</li>
<li>Writer starvation: continuous readers can block writers forever</li>
<li>Writer-preferring locks prevent writer starvation but may slow readers</li>
<li>Python: no built-in RWLock (use third-party or implement yourself)</li>
<li>Best for: caches, config stores, DNS, any read-heavy shared data</li>
</ul>""",
    mental_model="""REGULAR LOCK:    R1 | R2 | R3 | W1 | R4 | R5    (all sequential)
READ-WRITE LOCK: R1 R2 R3 | W1 | R4 R5 R6 R7   (readers overlap!)
                  ^^^^^^^^       ^^^^^^^^^^^^^
                  concurrent!    concurrent!

RULE:
    Readers: unlimited concurrent (they don't modify)
    Writer:  exclusive access (must be alone)""",
    mistakes="""<ul>
<li><strong>Using RWLock when writes are frequent</strong> — If writes are 50%, regular lock may be faster (less overhead).</li>
<li><strong>Upgrading read to write</strong> — Cannot do: acquire_read() then acquire_write() = deadlock. Must release read first.</li>
<li><strong>Not considering starvation</strong> — Reader-preferring locks can starve writers in read-heavy workloads.</li>
<li><strong>Holding read lock too long</strong> — Long reads still block writers. Keep read sections short.</li>
</ul>""",
    exercise="""<ol>
<li>Implement a ReadWriteLock. Test with 10 readers and 2 writers.</li>
<li>Show writer starvation: continuous readers that prevent any writer from executing.</li>
<li>Fix it with a writer-preferring variant.</li>
<li>Benchmark: RWLock vs regular Lock with 95% reads / 5% writes. Show the speedup.</li>
</ol>""",
    prev_link="18-lock-free-wait-free.html", prev_title="Lock-Free Algorithms",
    next_link="20-semaphore-latch-barrier.html", next_title="Semaphore/Latch/Barrier"
)

# Topic 20
write_topic("20-semaphore-latch-barrier.html",
    title="Semaphore, Latch &amp; Barrier",
    subtitle="Coordination primitives that control how many threads can access a resource (semaphore), wait for one-time events (latch), or synchronize at a meeting point (barrier).",
    tags=["intermediate","pattern","code"],
    analogy_title="Three Real-World Analogies",
    analogy="""<p><strong>Semaphore (Parking Lot)</strong>: A parking lot with 5 spots. Cars enter if spots available, wait if full. Each car leaving frees one spot.</p>
<p><strong>Latch (Starting Gate)</strong>: A race starting gate. All runners wait behind it. When the announcer fires the gun (count reaches zero), everyone runs. Gate never closes again.</p>
<p><strong>Barrier (Meeting Point)</strong>: A hiking group agrees to wait at the summit for everyone. Nobody continues until ALL members arrive. Then everyone descends together.</p>""",
    content="""
            <h2>Semaphore: Limited Access</h2>
<pre><code><span class="token-keyword">import</span> threading, time

<span class="token-comment"># Semaphore(n) = allow up to n threads simultaneously</span>
<span class="token-comment"># Mutex is just Semaphore(1)</span>
connection_pool = threading.Semaphore(<span class="token-number">3</span>)  <span class="token-comment"># Max 3 DB connections</span>

<span class="token-keyword">def</span> <span class="token-function">query_database</span>(thread_id):
    <span class="token-keyword">with</span> connection_pool:  <span class="token-comment"># Only 3 threads here at once</span>
        print(<span class="token-string">f"Thread {thread_id}: connected"</span>)
        time.sleep(<span class="token-number">1</span>)  <span class="token-comment"># Simulate query</span>
        print(<span class="token-string">f"Thread {thread_id}: done"</span>)

<span class="token-comment"># 10 threads, but only 3 run concurrently</span>
threads = [threading.Thread(target=query_database, args=(i,)) <span class="token-keyword">for</span> i <span class="token-keyword">in</span> range(<span class="token-number">10</span>)]
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.start()
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.join()</code></pre>

            <h2>CountDownLatch: Wait for N Events</h2>
<pre><code><span class="token-keyword">import</span> threading

<span class="token-keyword">class</span> <span class="token-class">CountDownLatch</span>:
    <span class="token-keyword">def</span> <span class="token-function">__init__</span>(self, count):
        self._count = count
        self._lock = threading.Lock()
        self._event = threading.Event()

    <span class="token-keyword">def</span> <span class="token-function">count_down</span>(self):
        <span class="token-keyword">with</span> self._lock:
            self._count -= <span class="token-number">1</span>
            <span class="token-keyword">if</span> self._count <= <span class="token-number">0</span>:
                self._event.set()

    <span class="token-keyword">def</span> <span class="token-function">wait</span>(self):
        self._event.wait()

<span class="token-comment"># Example: main thread waits for all workers to initialize</span>
latch = CountDownLatch(<span class="token-number">3</span>)

<span class="token-keyword">def</span> <span class="token-function">service</span>(name):
    time.sleep(<span class="token-number">1</span>)  <span class="token-comment"># Initialize</span>
    print(<span class="token-string">f"{name} ready!"</span>)
    latch.count_down()  <span class="token-comment"># Signal "I'm ready"</span>

<span class="token-keyword">for</span> name <span class="token-keyword">in</span> [<span class="token-string">"DB"</span>, <span class="token-string">"Cache"</span>, <span class="token-string">"Queue"</span>]:
    threading.Thread(target=service, args=(name,)).start()

latch.wait()  <span class="token-comment"># Block until all 3 services ready</span>
print(<span class="token-string">"All services initialized! Starting server..."</span>)</code></pre>

            <h2>Barrier: Everyone Waits for Everyone</h2>
<pre><code><span class="token-keyword">import</span> threading

<span class="token-comment"># Built-in Python barrier</span>
barrier = threading.Barrier(<span class="token-number">4</span>)  <span class="token-comment"># Wait for 4 threads</span>

<span class="token-keyword">def</span> <span class="token-function">parallel_phase</span>(thread_id):
    <span class="token-comment"># Phase 1: each thread does independent work</span>
    print(<span class="token-string">f"T{thread_id}: Phase 1 (computing...)"</span>)
    time.sleep(thread_id * <span class="token-number">0.5</span>)

    <span class="token-comment"># BARRIER: wait for ALL threads to finish Phase 1</span>
    barrier.wait()  <span class="token-comment"># Blocks until all 4 arrive</span>

    <span class="token-comment"># Phase 2: everyone proceeds together</span>
    print(<span class="token-string">f"T{thread_id}: Phase 2 (all synchronized!)"</span>)

threads = [threading.Thread(target=parallel_phase, args=(i,)) <span class="token-keyword">for</span> i <span class="token-keyword">in</span> range(<span class="token-number">4</span>)]
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.start()
<span class="token-keyword">for</span> t <span class="token-keyword">in</span> threads: t.join()</code></pre>

            <h2>Comparison</h2>
            <table class="comparison-table">
                <thead><tr><th>Primitive</th><th>Purpose</th><th>Reusable?</th><th>Who waits?</th></tr></thead>
                <tbody>
                    <tr><td><strong>Semaphore</strong></td><td>Limit concurrent access to N</td><td>Yes</td><td>Thread trying to acquire when count=0</td></tr>
                    <tr><td><strong>Latch</strong></td><td>Wait for N events to happen</td><td>No (one-shot)</td><td>Threads calling wait()</td></tr>
                    <tr><td><strong>Barrier</strong></td><td>Synchronize N threads at a point</td><td>Yes (resets)</td><td>All threads until last arrives</td></tr>
                </tbody>
            </table>

            <div class="industry-box">
                <h4>Industry Usage</h4>
                <ul>
                    <li><strong>Connection pooling</strong> — Semaphore limits concurrent DB/HTTP connections</li>
                    <li><strong>Rate limiting</strong> — Semaphore controls requests per second</li>
                    <li><strong>MapReduce</strong> — Barrier at end of map phase; all mappers finish before reduce starts</li>
                    <li><strong>Microservice startup</strong> — Latch: wait for all dependencies before accepting traffic</li>
                </ul>
            </div>""",
    summary="""<ul>
<li>Semaphore(N): allow up to N threads concurrently (generalized mutex)</li>
<li>CountDownLatch: block until N events occur (one-shot, not reusable)</li>
<li>Barrier: all N threads wait until the last one arrives, then all proceed</li>
<li>Semaphore for resource limiting, latch for startup coordination, barrier for phase sync</li>
<li>Python has built-in Semaphore and Barrier; CountDownLatch needs custom implementation</li>
</ul>""",
    mental_model="""SEMAPHORE(3):
    [T1 in] [T2 in] [T3 in] | T4 waits | T5 waits
    T1 exits → T4 enters
    Always max 3 inside.

LATCH(3):
    Count: 3 → 2 → 1 → 0 → [OPEN!]
    All waiters released. Cannot close again.

BARRIER(4):
    T1 arrives → wait
    T2 arrives → wait
    T3 arrives → wait
    T4 arrives → ALL GO! (last one triggers release)""",
    mistakes="""<ul>
<li><strong>Semaphore release without acquire</strong> — Increases count beyond max! Always pair acquire/release.</li>
<li><strong>Barrier with wrong count</strong> — If count is 5 but only 4 threads call wait(), hangs forever.</li>
<li><strong>Using latch when barrier needed</strong> — Latch is one-shot. For repeated synchronization, use barrier.</li>
<li><strong>Not handling BrokenBarrierError</strong> — If one thread crashes at barrier, others get this exception.</li>
</ul>""",
    exercise="""<ol>
<li>Use Semaphore(3) to limit concurrent file downloads to 3 at a time out of 20.</li>
<li>Implement CountDownLatch: main waits for 5 worker threads to finish initialization.</li>
<li>Use Barrier for parallel matrix computation: each thread computes its portion, barrier syncs, then next phase.</li>
<li>Combine: Semaphore for resource limits + Barrier for phase synchronization in a pipeline.</li>
</ol>""",
    prev_link="19-read-write-locks.html", prev_title="Read-Write Locks",
    next_link="21-cap-theorem.html", next_title="CAP Theorem"
)

print("\n=== Module 3 (topics 14-20) generation complete ===")
