"""
Simple AI Coding Harness
Uses NVIDIA API + permission system for safe file operations.
"""

import inspect
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests
from dotenv import load_dotenv

load_dotenv()

# --- Logging Setup ---
LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG").upper()

logger = logging.getLogger("coding_agent")
logger.setLevel(getattr(logging, LOG_LEVEL, logging.DEBUG))

_log_handler = logging.StreamHandler(sys.stderr)
_log_handler.setFormatter(logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(funcName)-22s | %(message)s",
    datefmt="%H:%M:%S",
))
logger.addHandler(_log_handler)
logger.propagate = False

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_MODEL = os.environ.get("NVIDIA_MODEL", "google/gemma-4-31b-it")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
ENABLE_THINKING = os.environ.get("ENABLE_THINKING", "false").lower() in ("1", "true", "yes")

logger.info("Configuration loaded — model=%s, thinking=%s, log_level=%s",
            NVIDIA_MODEL, ENABLE_THINKING, LOG_LEVEL)

# Terminal colors (respect NO_COLOR convention)
_USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None
YOU = "\033[94m" if _USE_COLOR else ""
BOT = "\033[93m" if _USE_COLOR else ""
WARN = "\033[91m" if _USE_COLOR else ""
OK = "\033[92m" if _USE_COLOR else ""
REASON = "\033[90m" if _USE_COLOR else ""  # dim gray for reasoning
RST = "\033[0m" if _USE_COLOR else ""

# --- Permission System ---
PERMISSIONS = {
    "read_file": "auto",   # no approval needed
    "list_files": "auto",  # no approval needed
    "edit_file": "ask",    # ask before executing
}


def ask_permission(tool_name: str, args: dict) -> bool:
    logger.debug("ENTER ask_permission(tool=%s, args=%s)", tool_name, args)
    if PERMISSIONS.get(tool_name) == "auto":
        logger.debug("Auto-approved tool=%s", tool_name)
        return True
    print(f"\n{WARN}[PERMISSION] The agent wants to run:{RST}")
    print(f"  Tool: {tool_name}")
    print(f"  Args: {json.dumps(args, indent=2)}")
    answer = input(f"{WARN}Allow? (y/n): {RST}").strip().lower()
    granted = answer in ("y", "yes")
    logger.info("Permission %s for tool=%s", "GRANTED" if granted else "DENIED", tool_name)
    return granted


# --- Path Utility ---
def resolve_path(path_str: str) -> Path:
    logger.debug("ENTER resolve_path(path_str=%s)", path_str)
    path = Path(path_str).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    logger.debug("EXIT  resolve_path -> %s", path)
    return path


# --- Tools ---
def read_file(filename: str) -> Dict[str, Any]:
    """
    Read the full content of a file.
    :param filename: Path to the file to read.
    :return: Dict with file_path and content.
    """
    logger.info("ENTER read_file(filename=%s)", filename)
    full_path = resolve_path(filename)
    if not full_path.exists():
        logger.warning("EXIT  read_file -> file not found: %s", full_path)
        return {"error": f"File not found: {full_path}"}
    content = full_path.read_text(encoding="utf-8")
    logger.info("EXIT  read_file -> read %d chars from %s", len(content), full_path)
    return {"file_path": str(full_path), "content": content}


def list_files(path: str) -> Dict[str, Any]:
    """
    List files and directories at the given path.
    :param path: Directory path to list.
    :return: Dict with path and list of files.
    """
    logger.info("ENTER list_files(path=%s)", path)
    full_path = resolve_path(path)
    if not full_path.is_dir():
        logger.warning("EXIT  list_files -> not a directory: %s", full_path)
        return {"error": f"Not a directory: {full_path}"}
    items = [
        {"name": item.name, "type": "file" if item.is_file() else "dir"}
        for item in full_path.iterdir()
    ]
    logger.info("EXIT  list_files -> found %d items in %s", len(items), full_path)
    return {"path": str(full_path), "files": items}


def edit_file(path: str, old_str: str, new_str: str) -> Dict[str, Any]:
    """
    Edit a file. If old_str is empty, create/overwrite with new_str.
    Otherwise replace first occurrence of old_str with new_str.
    :param path: File path to edit.
    :param old_str: Text to find (empty = create new file).
    :param new_str: Replacement text or new file content.
    :return: Dict with path and action taken.
    """
    logger.info("ENTER edit_file(path=%s, old_str_len=%d, new_str_len=%d)",
                path, len(old_str), len(new_str))
    full_path = resolve_path(path)
    if old_str == "":
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(new_str, encoding="utf-8")
        logger.info("EXIT  edit_file -> created %s (%d chars)", full_path, len(new_str))
        return {"path": str(full_path), "action": "created"}
    if not full_path.exists():
        logger.warning("EXIT  edit_file -> file not found: %s", full_path)
        return {"path": str(full_path), "action": "error: file not found"}
    original = full_path.read_text(encoding="utf-8")
    if old_str not in original:
        logger.warning("EXIT  edit_file -> old_str not found in %s", full_path)
        return {"path": str(full_path), "action": "error: old_str not found"}
    full_path.write_text(original.replace(old_str, new_str, 1), encoding="utf-8")
    logger.info("EXIT  edit_file -> edited %s", full_path)
    return {"path": str(full_path), "action": "edited"}


TOOL_REGISTRY = {
    "read_file": read_file,
    "list_files": list_files,
    "edit_file": edit_file,
}

# --- System Prompt ---
def build_system_prompt() -> str:
    logger.info("ENTER build_system_prompt()")
    tool_docs = ""
    for name, fn in TOOL_REGISTRY.items():
        tool_docs += f"TOOL\n===\nName: {name}\nDescription: {fn.__doc__}\nSignature: {inspect.signature(fn)}\n{'='*20}\n"
        logger.debug("Registered tool: %s (sig=%s)", name, inspect.signature(fn))
    logger.info("EXIT  build_system_prompt -> %d tools registered, prompt_len=%d",
                len(TOOL_REGISTRY), len(tool_docs))
    return f"""You are a coding assistant. You help users with coding tasks by reading, listing, and editing files.

You have these tools:
{tool_docs}

When you need a tool, reply with exactly one line: tool: TOOL_NAME({{"arg": "value"}})
Use compact single-line JSON with double quotes. After receiving a tool_result, continue.
If no tool is needed, respond normally in plain text."""


# --- Tool Call Parser ---
def parse_tool_calls(text: str) -> List[Tuple[str, Dict[str, Any]]]:
    logger.debug("ENTER parse_tool_calls(text_len=%d)", len(text) if text else 0)
    calls = []
    if not text:
        logger.debug("EXIT  parse_tool_calls -> empty text, no calls")
        return calls
    for line in text.splitlines():
        line = line.strip()
        idx = line.find("tool:")
        if idx == -1:
            continue
        try:
            after = line[idx + len("tool:"):].strip()
            name, rest = after.split("(", 1)
            name = name.strip()
            logger.debug("Parsing tool call: name=%s, raw_args=%s", name, rest)
            if not rest.endswith(")"):
                logger.debug("Skipping malformed tool call (no closing paren)")
                continue
            args = json.loads(rest[:-1].strip())
            if name in TOOL_REGISTRY:
                calls.append((name, args))
                logger.info("Parsed valid tool call: %s(%s)", name, args)
            else:
                logger.warning("Unknown tool in LLM response: %s", name)
        except Exception as exc:
            logger.debug("Failed to parse tool line: %s — %s", line, exc)
            continue
    logger.debug("EXIT  parse_tool_calls -> %d calls found", len(calls))
    return calls


# --- LLM Call via NVIDIA API ---
def call_llm(conversation: List[Dict[str, str]], stream_print: bool = True) -> str:
    """Call NVIDIA LLM. If stream_print=True, prints reasoning + content live."""
    logger.info("ENTER call_llm(messages=%d, stream_print=%s)", len(conversation), stream_print)
    logger.debug("Conversation payload: %s",
                 json.dumps(conversation, default=str)[:2000])
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Accept": "text/event-stream",
    }
    payload = {
        "model": NVIDIA_MODEL,
        "messages": conversation,
        "max_tokens": 4096,
        "temperature": 0.6,
        "top_p": 0.95,
        "stream": True,
    }

    if ENABLE_THINKING:
        payload["extra_body"] = {
            "chat_template_kwargs": {"enable_thinking": True, "clear_thinking": False}
        }
        logger.debug("Thinking mode enabled in payload")

    logger.debug("POST %s  model=%s", NVIDIA_URL, NVIDIA_MODEL)
    resp = requests.post(NVIDIA_URL, headers=headers, json=payload, stream=True, timeout=120)
    print(f"this is the response header object {RST}", resp.headers)
    print(f"this is the response  {RST}", resp.text)
    logger.info("NVIDIA API response: status=%d", resp.status_code)
    if resp.status_code != 200:
        logger.error("NVIDIA API error %d: %s", resp.status_code, resp.text[:500])
        raise RuntimeError(f"NVIDIA API {resp.status_code}: {resp.text[:500]}")

    full_content = ""
    in_reasoning = False
    chunk_count = 0
    for line in resp.iter_lines():
        if not line:
            continue
        decoded = line.decode("utf-8")
        logger.debug("Stream line: %s", decoded[:200])
        if not decoded.startswith("data: "):
            continue
        data_str = decoded[len("data: "):]
        if data_str.strip() == "[DONE]":
            logger.debug("Stream finished ([DONE] received)")
            break
        try:
            chunk = json.loads(data_str)
            chunk_count += 1
            delta = chunk["choices"][0].get("delta", {})
            # Handle reasoning_content (thinking/chain-of-thought)
            reasoning = delta.get("reasoning_content") or delta.get("reasoning", "")
            if reasoning and stream_print:
                if not in_reasoning:
                    print(f"\n{REASON}[Thinking]{RST}")
                    in_reasoning = True
                print(f"{REASON}{reasoning}{RST}", end="", flush=True)
            # Handle regular content
            text = delta.get("content", "")
            if text:
                if in_reasoning:
                    in_reasoning = False
                    print(f"\n{REASON}[/Thinking]{RST}\n")
                if stream_print:
                    print(text, end="", flush=True)
                full_content += text
        except (json.JSONDecodeError, KeyError, IndexError) as exc:
            logger.debug("Chunk parse error: %s", exc)
            continue
    if stream_print and in_reasoning:
        print(f"\n{REASON}[/Thinking]{RST}\n")
    if stream_print:
        print()  # final newline
    logger.info("EXIT  call_llm -> %d chunks, %d chars received", chunk_count, len(full_content))
    logger.debug("LLM response text: %s", full_content[:500])
    return full_content or ""


# --- Execute a Tool ---
def run_tool(name: str, args: dict) -> dict:
    logger.info("ENTER run_tool(name=%s, args=%s)", name, args)
    fn = TOOL_REGISTRY[name]
    if name == "read_file":
        result = fn(args.get("filename", args.get("path", ".")))
    elif name == "list_files":
        result = fn(args.get("path", "."))
    elif name == "edit_file":
        result = fn(args.get("path", "."), args.get("old_str", ""), args.get("new_str", ""))
    else:
        logger.error("Unknown tool requested: %s", name)
        return {"error": "unknown tool"}
    logger.info("EXIT  run_tool -> %s", {k: v for k, v in result.items() if k != "content"})
    return result


# --- Main Loop ---
def main():
    logger.info("ENTER main()")
    if not NVIDIA_API_KEY:
        print(f"{WARN}Set NVIDIA_API_KEY in .env or environment.{RST}")
        logger.error("NVIDIA_API_KEY not set — aborting")
        return

    print(f"{OK}AI Coding Harness (NVIDIA: {NVIDIA_MODEL}){RST}")
    print(f"{OK}Checking LLM connection...{RST}", end=" ", flush=True)
    logger.info("Testing LLM connectivity...")
    try:
        test_reply = call_llm([{"role": "user", "content": "Say OK"}], stream_print=False)
        print(f"{OK}Connected! LLM says: {test_reply.strip()}{RST}")
        logger.info("LLM connectivity test passed")
    except Exception as e:
        print(f"{WARN}FAILED: {e}{RST}")
        logger.error("LLM connectivity test failed: %s", e)
        return
    print(f"{OK}Permissions: read/list=auto, edit=ask. Type 'quit' to exit.{RST}\n")

    conversation = [{"role": "system", "content": build_system_prompt()}]
    logger.info("System prompt initialized (len=%d)", len(conversation[0]["content"]))
    print(f"{OK}System prompt initialized. You can start chatting with the agent!{RST}\n")

    turn = 0
    while True:
        try:
            user_input = input(f"{YOU}You: {RST}").strip()
        except (KeyboardInterrupt, EOFError):
            logger.info("User interrupted input — exiting")
            break
        if user_input.lower() in ("quit", "exit"):
            logger.info("User typed quit/exit")
            break
        if not user_input:
            continue

        turn += 1
        logger.info("=== Turn %d === user_input_len=%d", turn, len(user_input))
        logger.debug("User input: %s", user_input[:300])
        conversation.append({"role": "user", "content": user_input})

        # Inner loop: keep calling LLM until no more tool requests
        iteration = 0
        while True:
            iteration += 1
            logger.info("--- Turn %d, LLM iteration %d ---", turn, iteration)
            print(f"{BOT}Agent: {RST}", end="", flush=True)
            reply = call_llm(conversation, stream_print=True)
            tool_calls = parse_tool_calls(reply)

            if not tool_calls:
                logger.info("No tool calls — appending assistant reply (len=%d)", len(reply))
                conversation.append({"role": "assistant", "content": reply})
                break

            logger.info("Tool calls detected: %d", len(tool_calls))
            conversation.append({"role": "assistant", "content": reply})
            for name, args in tool_calls:
                if not ask_permission(name, args):
                    result = {"denied": f"{name} was blocked by user"}
                    print(f"{WARN}[DENIED] {name}{RST}")
                    logger.warning("Tool denied by user: %s", name)
                else:
                    result = run_tool(name, args)
                    print(f"{OK}[RAN] {name} -> {result.get('action', 'ok')}{RST}")
                logger.debug("Tool result keys: %s", list(result.keys()))
                conversation.append({
                    "role": "user",
                    "content": f"tool_result({json.dumps(result)})"
                })
    logger.info("Session ended — total turns=%d, conversation_messages=%d", turn, len(conversation))
    print("Goodbye.")


if __name__ == "__main__":
    main()
