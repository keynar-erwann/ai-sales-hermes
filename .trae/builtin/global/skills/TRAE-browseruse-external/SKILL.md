---
name: "TRAE-browseruse-external"
description: "Automate tasks in the user's own browser (Chrome on their machine). Invoke when the user says things like 'use my browser', 'open in my Chrome', 'use the browser on my computer', or wants to browse/interact/test web pages in their local Chrome."
user-invocable: false
---

# External Browser Use Guide

Browser tools that operate the user's **external Chrome browser** via the TRAE Chrome extension. All tools below are aliases of the standard browseruse tools, automatically routed to the external Chrome browser (native mode).

Most browser operations are executed through the Exec tool (V8 sandbox), but some tools **must** be called as standalone toolcalls. See [Tool Calling Mode Reference](#tool-calling-mode-reference) for the complete classification.

---

## Tool Calling Mode Reference

### Tools callable via Exec (`await tools.*`)

These tools **MUST** be called inside Exec using `await tools.<name>(args)`:

| Category | Tools |
|----------|-------|
| Navigation | `external_browser_navigate`, `external_browser_navigate_back`, `external_browser_tabs` |
| Observation | `external_browser_snapshot`, `external_browser_take_screenshot`, `external_browser_get_attribute`, `external_browser_console_messages`, `external_browser_network_requests` |
| Interaction | `external_browser_click`, `external_browser_type`, `external_browser_hover`, `external_browser_scroll`, `external_browser_press_key`, `external_browser_select_option`, `external_browser_drag`, `external_browser_upload_file`, `external_browser_handle_dialog` |
| Advanced | `external_browser_evaluate`, `external_browser_wait_for` |
| Lock/Unlock | `external_browser_lock`, `external_browser_unlock` |

### Tools that MUST be called alone (one per turn)

| Tool | Reason |
|------|--------|
| `browser_connect_plugin` | Connectivity check. Must run before any other browser tools in a session. You need its result to decide the next step. |
| `browser_setup_plugin` | Requires user interaction (confirm/skip). You need its result to decide whether to use external or built-in browser. |

> **Rule**: These tools MUST be the **only** tool call in that turn. Do NOT combine them with other tool calls in the same response. These tools do NOT use the `external_` prefix.

---

## CRITICAL - Tool Naming Convention

When operating the user's **external Chrome browser**, you MUST always use the `external_browser_*` prefix for ALL operational browseruse tool calls (e.g., `external_browser_navigate`, `external_browser_click`, `external_browser_snapshot`).

- **DO NOT** use `browser_navigate`, `browser_click`, or any unprefixed `browser_*` form for operational tools — those may target the built-in browser, NOT the user's external Chrome.
- Even if error messages or tool descriptions mention `browser_xxx` without the prefix, you must still use `external_browser_xxx` for operational tools to route the call to the external browser.
- The `external_` prefix is the **sole routing signal** that distinguishes external Chrome operations from built-in browser operations.

---

## CRITICAL - First-time Connection Check

Before using any external browser tools for the first time in a session, you MUST:

1. Call `browser_connect_plugin` to verify the Chrome extension is reachable.
2. If `browser_connect_plugin` returns `connected: false`, immediately call `browser_setup_plugin` to guide the user through setup.
3. Only proceed with browser operations after `browser_connect_plugin` succeeds or `browser_setup_plugin` completes.

If `browser_setup_plugin` returns that the user chose the built-in browser, stop using `external_*` tools and follow the `TRAE-browseruse` skill for standard browser usage.

> **CRITICAL**: `browser_connect_plugin` and `browser_setup_plugin` MUST each be called **alone** in a single turn — do NOT combine them with any other tool calls in the same response. Mixing them with other tools causes judgment issues because the AI cannot properly evaluate the connection/initialization result before deciding the next step.

> **NEVER** call `browser_waiting_for_user_interaction` when `connected: false`. That tool is for handing browser control to the user during an active session — it cannot fix a missing extension. The ONLY correct response to `connected: false` is `browser_setup_plugin`.

---

## CRITICAL - Before interacting with any page

1. Use `external_browser_tabs` with action `"list"` to see open tabs and their URLs.
2. Use `external_browser_snapshot` to get the page structure and element refs before any interaction (click, type, hover, etc.).

## IMPORTANT - Waiting strategy

When waiting for page changes (navigation, content loading, animations, etc.), prefer short incremental waits (1-3 seconds) with `external_browser_snapshot` checks in between rather than a single long wait. For example, instead of waiting 10 seconds, do: wait 2s → snapshot → check if ready → if not, wait 2s more → snapshot again. This allows you to proceed as soon as the page is ready rather than always waiting the maximum time.

## Notes

- If two browser actions need to be performed sequentially, they should not be called in parallel.
- Iframe content is not accessible — only elements outside iframes can be interacted with.
- For nested scroll containers, use `external_browser_scroll` with `scrollIntoView: true` before clicking elements that may be obscured.

---

## Code Execution Tool

You have access to a code execution tool that runs JavaScript in an isolated V8 sandbox.

### CRITICAL: Always prefer Exec when the available tools can accomplish the task.

- ANY tool listed below MUST be called via `await tools.<name>(args)` inside Exec, NOT as a direct tool call.
- Use direct tool calls ONLY for tools that are NOT available inside Exec.
- Even for a single-step task, use Exec if that step involves an available tool.
- For multi-step tasks, always use a single Exec call.
- Exec gives you full programmatic control: loops, conditionals, parallel calls, error handling — use it.

### Call format

```
run_mcp(server_name="integrated_code_mode", tool_name="Exec", args={"code": "<your_js_code>"})
```

### Runtime environment

- Only ECMAScript standard built-ins are available (Array, Object, Math, JSON, Promise, etc.).
- The ONLY non-standard globals are: `tools`, `text`, `exit`.
- There is NO `console`, NO `fetch`, NO `require`, NO `process`, NO `setTimeout`, and NO file system or network access.
- Any attempt to call an undefined identifier will throw a ReferenceError.

### Instructions

- Use `await tools.<tool_name>(args)` to call tools — multiple calls in sequence are encouraged.
- Use `Promise.all([tools.a(x), tools.b(y)])` for concurrent tool calls.
- Use `text(value)` to output results to LLM (value will be stringified via JSON.stringify if not a string).
- Use `exit()` to stop execution early (already-produced text output is preserved).

### Error handling

- Tool call errors cause the Promise to reject — use `try/catch` to handle them gracefully.
- Unhandled exceptions terminate the script and return the error message as the result.
- If the script exceeds the execution time limit, it is forcibly terminated and an error is returned.
- `text()` output produced before an unhandled error is preserved in the response.

---

## Available Browser Functions

### Page Navigation

#### `external_browser_navigate` — Navigate to a URL and return a snapshot

```typescript
interface ExternalBrowserNavigateParams {
  url: string;
  viewId?: string;
  newTab?: boolean;
  position?: "active" | "side";
  extraHeaders?: Record<string, string>;
}
```

#### `external_browser_navigate_back` — Go back in browser history, return a snapshot

```typescript
interface ExternalBrowserNavigateBackParams {
  viewId?: string;
}
```

#### `external_browser_tabs` — Manage browser tabs (list/new/close/select/activate)

```typescript
interface ExternalBrowserTabsParams {
  action: "list" | "new" | "close" | "select" | "activate";
  index?: number;
}
```

### Page Observation (prefer snapshot over screenshot)

#### `external_browser_snapshot` — Get page accessibility snapshot

```typescript
interface ExternalBrowserSnapshotParams {
  viewId?: string;
  strategy?: "dom" | "cdp";
  maxDepth?: number;
  maxNodes?: number;
  includeIgnored?: boolean;
  interactive?: boolean;
  compact?: boolean;
  selector?: string;
  includeDiff?: boolean;
}
```

#### `external_browser_take_screenshot` — Take a screenshot

```typescript
interface ExternalBrowserTakeScreenshotParams {
  filename?: string;
  fullPage?: boolean;
  ref?: string;
  viewId?: string;
}
```

#### `external_browser_get_attribute` — Get an element attribute value

```typescript
interface ExternalBrowserGetAttributeParams {
  ref: string;
  name: string;
  viewId?: string;
}
```

#### `external_browser_console_messages` — Get browser console log messages

```typescript
interface ExternalBrowserConsoleMessagesParams {
  viewId?: string;
}
```

#### `external_browser_network_requests` — Get captured network requests

```typescript
interface ExternalBrowserNetworkRequestsParams {
  viewId?: string;
}
```

### Element Interaction

#### `external_browser_click` — Click an element by ref, returns snapshot

```typescript
interface ExternalBrowserClickParams {
  ref: string;
  doubleClick?: boolean;
  button?: "left" | "right" | "middle";
  modifiers?: string[];
  viewId?: string;
}
```

#### `external_browser_type` — Type text into an input element, returns snapshot

```typescript
interface ExternalBrowserTypeParams {
  ref: string;
  text: string;
  submit?: boolean;
  slowly?: boolean;
  viewId?: string;
}
```

#### `external_browser_hover` — Hover over an element, returns snapshot

```typescript
interface ExternalBrowserHoverParams {
  ref: string;
  viewId?: string;
}
```

#### `external_browser_scroll` — Scroll the page or a specific element, returns snapshot

```typescript
interface ExternalBrowserScrollParams {
  ref?: string;
  direction?: "up" | "down" | "left" | "right";
  amount?: number;
  deltaX?: number;
  deltaY?: number;
  scrollIntoView?: boolean;
  viewId?: string;
}
```

#### `external_browser_press_key` — Dispatch a keyboard event

```typescript
interface ExternalBrowserPressKeyParams {
  key: string;
  viewId?: string;
}
```

#### `external_browser_select_option` — Select option(s) in a dropdown, returns snapshot

```typescript
interface ExternalBrowserSelectOptionParams {
  ref: string;
  values: string[];
  viewId?: string;
}
```

#### `external_browser_drag` — Drag from one element to another

```typescript
interface ExternalBrowserDragParams {
  sourceRef: string;
  targetRef?: string;
  targetX?: number;
  targetY?: number;
  viewId?: string;
}
```

#### `external_browser_upload_file` — Upload a file to a file input element

```typescript
interface ExternalBrowserUploadFileParams {
  ref: string;
  element?: string;
  filePath: string;
  viewId?: string;
}
```

#### `external_browser_handle_dialog` — Handle a browser dialog

```typescript
interface ExternalBrowserHandleDialogParams {
  action?: "accept" | "dismiss";
  promptText?: string;
  viewId?: string;
}
```

### Advanced

#### `external_browser_evaluate` — Execute JavaScript in the page context

```typescript
interface ExternalBrowserEvaluateParams {
  script: string;
  viewId?: string;
}
```

#### `external_browser_wait_for` — Wait for a condition

```typescript
interface ExternalBrowserWaitForParams {
  time?: number;
  text?: string;
  textGone?: string;
  selector?: string;
  state?: string;
  timeout?: number;
  viewId?: string;
}
```

#### `external_browser_lock` — Lock the browser for exclusive control

```typescript
interface ExternalBrowserLockParams {
  viewId?: string;
}
```

#### `external_browser_unlock` — Unlock the browser, release control

```typescript
interface ExternalBrowserUnlockParams {
  viewId?: string;
  handOverToUser?: boolean;
}
```

---

## Workflow Best Practices

### Snapshot-Driven Approach
1. **Snapshot first**: Always call `tools.external_browser_snapshot()` to understand the page before acting.
2. **Click by ref**: Use `tools.external_browser_click({ ref: N })` with the `[ref=N]` from snapshot output.
3. **Verify after action**: Snapshot again after critical actions to confirm the page state changed.
4. **Use evaluate() for data**: When you need structured data, prefer `tools.external_browser_evaluate({ script })` over parsing snapshot text.

### After Navigation
Always wait after navigating before interacting:
```javascript
await tools.external_browser_navigate({ url: "https://example.com" });
await tools.external_browser_wait_for({ time: 2 });
const snap = await tools.external_browser_snapshot();
```

### Multi-Step Orchestration
```javascript
await tools.external_browser_navigate({ url: "https://example.com" });
await tools.external_browser_wait_for({ time: 2 });
const snap = await tools.external_browser_snapshot();
await tools.external_browser_click({ ref: "3" });
await tools.external_browser_type({ ref: "3", text: "search query", submit: true });
await tools.external_browser_wait_for({ time: 2 });
const result = await tools.external_browser_snapshot();
text(result);
```

---

## Safety Rules
- Never submit forms with sensitive data without user approval.
- Never bypass security prompts (CAPTCHAs, "site not secure" warnings).
- Never delete or modify user data without explicit approval.
