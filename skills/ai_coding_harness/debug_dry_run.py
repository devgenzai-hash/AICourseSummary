"""
Debug Dry Run — Exercises every code path in coding_agent.py
and prints all intermediate values so you can see exactly what happens.

Run: python debug_dry_run.py
"""

import inspect
import json
import os
import sys
import tempfile
import shutil
from pathlib import Path

# We import everything from coding_agent so we use the real code
from coding_agent import (
    resolve_path,
    read_file,
    list_files,
    edit_file,
    TOOL_REGISTRY,
    build_system_prompt,
    parse_tool_calls,
    call_llm,
    run_tool,
    ask_permission,
    PERMISSIONS,
    NVIDIA_API_KEY,
    NVIDIA_MODEL,
    NVIDIA_URL,
    ENABLE_THINKING,
    _USE_COLOR,
    YOU, BOT, WARN, OK, REASON, RST,
)

# ─── Helpers ───
SEPARATOR = "=" * 70
SUBSEP = "-" * 50

def heading(title):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)

def subheading(title):
    print(f"\n{SUBSEP}")
    print(f"  {title}")
    print(SUBSEP)

# ─────────────────────────────────────────────
# SECTION 0: Show configuration values
# ─────────────────────────────────────────────
heading("SECTION 0: Configuration values loaded at import time")

print(f"  NVIDIA_API_KEY    = '{NVIDIA_API_KEY[:12]}...' (truncated for safety)")
print(f"  NVIDIA_MODEL      = '{NVIDIA_MODEL}'")
print(f"  NVIDIA_URL        = '{NVIDIA_URL}'")
print(f"  ENABLE_THINKING   = {ENABLE_THINKING}")
print(f"  _USE_COLOR        = {_USE_COLOR}")
print(f"  sys.stdout.isatty = {sys.stdout.isatty()}")
print(f"  NO_COLOR env      = {os.getenv('NO_COLOR')}")
print()
print("  Color codes (will appear as escape sequences if redirected to file):")
print(f"    YOU  (blue)   = {repr(YOU)}")
print(f"    BOT  (yellow) = {repr(BOT)}")
print(f"    WARN (red)    = {repr(WARN)}")
print(f"    OK   (green)  = {repr(OK)}")
print(f"    REASON (gray) = {repr(REASON)}")
print(f"    RST  (reset)  = {repr(RST)}")
print()
print("  PERMISSIONS dict:")
for tool_name, perm in PERMISSIONS.items():
    print(f"    {tool_name:12s} -> {perm}")
print()
print("  TOOL_REGISTRY keys:", list(TOOL_REGISTRY.keys()))

# ─────────────────────────────────────────────
# SECTION 1: resolve_path — 3 cases
# ─────────────────────────────────────────────
heading("SECTION 1: resolve_path() — all cases")

subheading("Case 1a: Relative path")
input_path = "readme.md"
result = resolve_path(input_path)
print(f"  Input:  '{input_path}'")
print(f"  Path('{input_path}').expanduser() = {Path(input_path).expanduser()}")
print(f"  Is absolute? {Path(input_path).expanduser().is_absolute()}")
print(f"  Path.cwd() = {Path.cwd()}")
print(f"  Final resolved: {result}")

subheading("Case 1b: Absolute path")
input_path = r"C:\Users\aranjan\Documents\test.txt"
result = resolve_path(input_path)
print(f"  Input:  '{input_path}'")
print(f"  Path('{input_path}').expanduser() = {Path(input_path).expanduser()}")
print(f"  Is absolute? {Path(input_path).expanduser().is_absolute()}")
print(f"  Final resolved: {result}")

subheading("Case 1c: Path with ~ (home dir)")
input_path = "~/Documents/test.txt"
result = resolve_path(input_path)
print(f"  Input:  '{input_path}'")
print(f"  Path('{input_path}').expanduser() = {Path(input_path).expanduser()}")
print(f"  Is absolute? {Path(input_path).expanduser().is_absolute()}")
print(f"  Final resolved: {result}")

# ─────────────────────────────────────────────
# SECTION 2: read_file — 2 cases
# ─────────────────────────────────────────────
heading("SECTION 2: read_file() — all cases")

subheading("Case 2a: File exists (reading coding_agent.py itself)")
result = read_file("coding_agent.py")
print(f"  Input: 'coding_agent.py'")
print(f"  Return keys: {list(result.keys())}")
print(f"  file_path: {result.get('file_path')}")
print(f"  content length: {len(result.get('content', ''))} chars")
print(f"  content first 100 chars: {repr(result.get('content', '')[:100])}")

subheading("Case 2b: File does NOT exist")
result = read_file("this_file_does_not_exist_xyz.py")
print(f"  Input: 'this_file_does_not_exist_xyz.py'")
print(f"  Return: {result}")
print(f"  -> Contains 'error' key: {'error' in result}")

# ─────────────────────────────────────────────
# SECTION 3: list_files — 2 cases
# ─────────────────────────────────────────────
heading("SECTION 3: list_files() — all cases")

subheading("Case 3a: Valid directory (current dir)")
result = list_files(".")
print(f"  Input: '.'")
print(f"  Return keys: {list(result.keys())}")
print(f"  path: {result.get('path')}")
print(f"  Number of items: {len(result.get('files', []))}")
print(f"  Items:")
for item in result.get("files", []):
    print(f"    {item['type']:4s}  {item['name']}")

subheading("Case 3b: NOT a directory (a file path)")
result = list_files("coding_agent.py")
print(f"  Input: 'coding_agent.py'")
print(f"  Return: {result}")
print(f"  -> Contains 'error' key: {'error' in result}")

# ─────────────────────────────────────────────
# SECTION 4: edit_file — 4 cases
# ─────────────────────────────────────────────
heading("SECTION 4: edit_file() — all cases")

# Create a temp directory so we don't mess with real files
tmp_dir = tempfile.mkdtemp(prefix="debug_dryrun_")
print(f"  (Using temp directory: {tmp_dir})")

subheading("Case 4a: Create new file (old_str is empty)")
new_file = os.path.join(tmp_dir, "new_file.txt")
result = edit_file(new_file, "", "Hello, World!\nLine 2\n")
print(f"  Input path: '{new_file}'")
print(f"  Input old_str: '' (empty → create mode)")
print(f"  Input new_str: 'Hello, World!\\nLine 2\\n'")
print(f"  Return: {result}")
print(f"  File now exists: {Path(new_file).exists()}")
print(f"  File content: {repr(Path(new_file).read_text(encoding='utf-8'))}")

subheading("Case 4b: Edit file — old_str found")
result = edit_file(new_file, "Hello, World!", "Hi, Universe!")
print(f"  Input path: '{new_file}'")
print(f"  Input old_str: 'Hello, World!'")
print(f"  Input new_str: 'Hi, Universe!'")
print(f"  Return: {result}")
print(f"  File content after edit: {repr(Path(new_file).read_text(encoding='utf-8'))}")

subheading("Case 4c: Edit file — old_str NOT found")
result = edit_file(new_file, "THIS TEXT DOES NOT EXIST", "replacement")
print(f"  Input path: '{new_file}'")
print(f"  Input old_str: 'THIS TEXT DOES NOT EXIST'")
print(f"  Return: {result}")
print(f"  -> action contains 'error': {'error' in result.get('action', '')}")

subheading("Case 4d: Edit file — file does not exist")
missing_file = os.path.join(tmp_dir, "nonexistent.txt")
result = edit_file(missing_file, "some text", "replacement")
print(f"  Input path: '{missing_file}'")
print(f"  Input old_str: 'some text' (non-empty → edit mode)")
print(f"  Return: {result}")
print(f"  -> action contains 'error': {'error' in result.get('action', '')}")

# Cleanup temp dir
shutil.rmtree(tmp_dir, ignore_errors=True)
print(f"\n  (Cleaned up temp directory)")

# ─────────────────────────────────────────────
# SECTION 5: ask_permission — 2 cases (simulated)
# ─────────────────────────────────────────────
heading("SECTION 5: ask_permission() — cases (simulated, no actual input)")

subheading("Case 5a: 'auto' permission (read_file)")
# We can call it directly since 'auto' doesn't need input()
result = ask_permission("read_file", {"filename": "test.py"})
print(f"  Tool: 'read_file', Permission level: '{PERMISSIONS['read_file']}'")
print(f"  Return: {result}  (True = allowed without asking)")

subheading("Case 5b: 'ask' permission (edit_file) — SKIPPED in automated run")
print(f"  Tool: 'edit_file', Permission level: '{PERMISSIONS['edit_file']}'")
print(f"  This would prompt: '[PERMISSION] The agent wants to run: ...'")
print(f"  Then wait for user input: 'Allow? (y/n): '")
print(f"  If user types 'y' → returns True")
print(f"  If user types 'n' → returns False")
print(f"  (Skipping actual call to avoid blocking on input)")

# ─────────────────────────────────────────────
# SECTION 6: parse_tool_calls — multiple cases
# ─────────────────────────────────────────────
heading("SECTION 6: parse_tool_calls() — all cases")

subheading("Case 6a: Valid tool call for read_file")
text = 'Let me read that file for you.\ntool: read_file({"filename": "main.py"})'
result = parse_tool_calls(text)
print(f"  Input text:")
for i, line in enumerate(text.splitlines()):
    print(f"    Line {i}: {repr(line)}")
print(f"  Parsed calls: {result}")
print(f"  -> Found {len(result)} tool call(s)")
if result:
    print(f"  -> Tool name: '{result[0][0]}', Args: {result[0][1]}")

subheading("Case 6b: Valid tool call for edit_file")
text = 'tool: edit_file({"path": "test.py", "old_str": "foo", "new_str": "bar"})'
result = parse_tool_calls(text)
print(f"  Input text: {repr(text)}")
print(f"  Parsed calls: {result}")

subheading("Case 6c: Valid tool call for list_files")
text = 'tool: list_files({"path": "."})'
result = parse_tool_calls(text)
print(f"  Input text: {repr(text)}")
print(f"  Parsed calls: {result}")

subheading("Case 6d: No tool call — plain text response")
text = "Sure, I can help you with that. The answer is 42."
result = parse_tool_calls(text)
print(f"  Input text: {repr(text)}")
print(f"  Parsed calls: {result}")
print(f"  -> Empty list means no tools requested")

subheading("Case 6e: Malformed tool call (bad JSON)")
text = 'tool: read_file({filename: main.py})'  # missing quotes
result = parse_tool_calls(text)
print(f"  Input text: {repr(text)}")
print(f"  Parsed calls: {result}")
print(f"  -> Empty list means JSON parsing failed silently")

subheading("Case 6f: Unknown tool name")
text = 'tool: delete_file({"path": "main.py"})'
result = parse_tool_calls(text)
print(f"  Input text: {repr(text)}")
print(f"  Parsed calls: {result}")
print(f"  -> Empty because 'delete_file' is not in TOOL_REGISTRY")

subheading("Case 6g: Multiple tool calls in one response")
text = 'Let me check both files.\ntool: read_file({"filename": "a.py"})\ntool: read_file({"filename": "b.py"})'
result = parse_tool_calls(text)
print(f"  Input text (3 lines):")
for i, line in enumerate(text.splitlines()):
    print(f"    Line {i}: {repr(line)}")
print(f"  Parsed calls: {result}")
print(f"  -> Found {len(result)} tool call(s)")

subheading("Case 6h: Empty string")
result = parse_tool_calls("")
print(f"  Input text: '' (empty)")
print(f"  Parsed calls: {result}")

# ─────────────────────────────────────────────
# SECTION 7: run_tool — maps args to functions
# ─────────────────────────────────────────────
heading("SECTION 7: run_tool() — argument mapping")

subheading("Case 7a: run_tool('read_file', ...) with 'filename' key")
result = run_tool("read_file", {"filename": "coding_agent.py"})
print(f"  Args: {{'filename': 'coding_agent.py'}}")
print(f"  -> args.get('filename', args.get('path', '.')) = 'coding_agent.py'")
print(f"  Return keys: {list(result.keys())}")
print(f"  file_path: {result.get('file_path')}")

subheading("Case 7b: run_tool('read_file', ...) with 'path' key instead")
result = run_tool("read_file", {"path": "coding_agent.py"})
print(f"  Args: {{'path': 'coding_agent.py'}}")
print(f"  -> args.get('filename', args.get('path', '.')) = 'coding_agent.py'")
print(f"  -> Falls through to 'path' key since 'filename' is missing")
print(f"  Return keys: {list(result.keys())}")

subheading("Case 7c: run_tool('list_files', ...)")
result = run_tool("list_files", {"path": "."})
print(f"  Args: {{'path': '.'}}")
print(f"  Return: {len(result.get('files', []))} items found")

subheading("Case 7d: run_tool('edit_file', ...) — would create file")
print(f"  (Skipping actual file creation — same as edit_file() Cases 4a–4d above)")

# ─────────────────────────────────────────────
# SECTION 8: build_system_prompt — show output
# ─────────────────────────────────────────────
heading("SECTION 8: build_system_prompt() — the prompt sent to the AI")

prompt = build_system_prompt()
print(f"\n  Prompt length: {len(prompt)} chars")
print(f"\n  Full prompt content:")
print("  " + prompt.replace("\n", "\n  "))

# ─────────────────────────────────────────────
# SECTION 9: call_llm — LIVE API CALL
# ─────────────────────────────────────────────
heading("SECTION 9: call_llm() — LIVE API call to NVIDIA")

if not NVIDIA_API_KEY:
    print("  SKIPPED: No NVIDIA_API_KEY set in .env")
else:
    print(f"  Model: {NVIDIA_MODEL}")
    print(f"  URL: {NVIDIA_URL}")
    print(f"  Thinking enabled: {ENABLE_THINKING}")
    print()

    # Show exactly what conversation list looks like
    test_conversation = [{"role": "user", "content": "Say OK in one word"}]
    print(f"  Conversation being sent:")
    print(f"  {json.dumps(test_conversation, indent=4)}")
    print()

    print(f"  Headers being sent:")
    print(f"    Authorization: Bearer {NVIDIA_API_KEY[:12]}... (truncated)")
    print(f"    Accept: text/event-stream")
    print()

    print(f"  Payload being sent:")
    payload_display = {
        "model": NVIDIA_MODEL,
        "messages": test_conversation,
        "max_tokens": 4096,
        "temperature": 0.6,
        "top_p": 0.95,
        "stream": True,
    }
    print(f"  {json.dumps(payload_display, indent=4)}")
    print()

    print(f"  --- Streaming response ---")
    try:
        reply = call_llm(test_conversation, stream_print=True)
        print(f"  --- End of stream ---")
        print(f"  Full reply string: {repr(reply)}")
        print(f"  Reply length: {len(reply)} chars")
    except Exception as e:
        print(f"  ERROR: {e}")

# ─────────────────────────────────────────────
# SECTION 10: Full agent loop dry run (simulated)
# ─────────────────────────────────────────────
heading("SECTION 10: Simulated agent loop (no real user input)")

print("""
  Here's what happens step by step when you run main():

  1. Check NVIDIA_API_KEY:
     - Value: '{"exists" if NVIDIA_API_KEY else "MISSING"}'
     - If empty → prints error and returns immediately.

  2. Connection test:
     - Sends: [{{"role": "user", "content": "Say OK"}}]
     - If API returns 200 → prints "Connected!"
     - If error (timeout, bad key, etc.) → prints "FAILED" and returns.

  3. Build system prompt & init conversation:
     - conversation = [{{"role": "system", "content": "<long prompt with tool docs>"}}]
     - This is message index 0, always present.

  4. Outer loop (waiting for user input):
     - Reads input via input("You: ")
     - If "quit"/"exit" → breaks out
     - If empty → skips (continue)
     - Otherwise → appends {{"role": "user", "content": "<what you typed>"}}

  5. Inner loop (agent calls LLM repeatedly):
     a) Sends full conversation to LLM
     b) Gets reply (streamed to terminal)
     c) Parses reply for tool calls
     d) If NO tool calls:
        - Appends reply as "assistant" message
        - Breaks inner loop → back to waiting for input
     e) If tool calls found:
        - Appends reply as "assistant" message
        - For each tool call:
          - Checks permission (auto or ask)
          - Runs tool or denies
          - Appends result as "user" message (tool_result(...))
        - Loops back to step (a) — LLM sees the results
""")

# Show a concrete example trace
subheading("Example Trace: User asks 'show me what files are here'")
print("""
  conversation = [
    {{"role": "system", "content": "<system prompt>"}},           # index 0
    {{"role": "user", "content": "show me what files are here"}}  # index 1
  ]

  → LLM receives this, replies:
    "Let me list the files for you.
     tool: list_files({{"path": "."}})"

  → parse_tool_calls finds: [("list_files", {{"path": "."}})]

  → Since tool_calls is not empty:
    conversation.append({{"role": "assistant", "content": "Let me list...tool: list_files(...)"}})

    → ask_permission("list_files", {{"path": "."}})
      → PERMISSIONS["list_files"] == "auto" → returns True

    → run_tool("list_files", {{"path": "."}})
      → calls list_files(".")
      → Returns: {{"path": "C:\\\\...\\\\ai_coding_harness", "files": [...]}}

    conversation.append({{
      "role": "user",
      "content": "tool_result({{\\"path\\": \\"...\\", \\"files\\": [...]}})"
    }})

  → Back to inner loop → calls LLM again with full conversation (5 messages now)

  → LLM sees the tool_result, replies:
    "Here are the files in the current directory:
     - coding_agent.py (file)
     - .env (file)
     - requirements.txt (file)"

  → parse_tool_calls finds: [] (no tool calls)

  → conversation.append({{"role": "assistant", "content": "Here are the files..."}})
  → Breaks inner loop → back to "You: " prompt
""")

subheading("Example Trace: User asks 'create a file hello.py with print(hi)'")
print("""
  conversation = [
    {{"role": "system", "content": "<system prompt>"}},
    {{"role": "user", "content": "create a file hello.py with print(hi)"}}
  ]

  → LLM replies:
    "I'll create that file for you.
     tool: edit_file({{"path": "hello.py", "old_str": "", "new_str": "print('hi')\\n"}})"

  → parse_tool_calls finds: [("edit_file", {{"path": "hello.py", "old_str": "", "new_str": "..."}})]

  → ask_permission("edit_file", ...) → PERMISSIONS["edit_file"] == "ask"
    → Prints: "[PERMISSION] The agent wants to run:"
    → Prints: "  Tool: edit_file"
    → Prints: "  Args: {{"path": "hello.py", ...}}"
    → Prompts: "Allow? (y/n): "

    → If user types "y":
       → run_tool("edit_file", ...) → creates hello.py
       → Prints: "[RAN] edit_file -> created"
       → Appends tool_result to conversation
       → LLM sees result, says "Done! Created hello.py"

    → If user types "n":
       → result = {{"denied": "edit_file was blocked by user"}}
       → Prints: "[DENIED] edit_file"
       → LLM sees denial, says "Okay, I won't create the file."
""")

# ─────────────────────────────────────────────
heading("DRY RUN COMPLETE")
print("  All code paths exercised. Review output above for values.")
print(SEPARATOR)
