"""Workbench 스타일 SQL 에디터 (Streamlit Custom Component v2)

- Ctrl+Enter          : 선택 영역, 선택이 없으면 커서가 있는 문장 실행
- Ctrl+Shift+Enter    : 선택 영역, 선택이 없으면 전체 실행
- Ctrl+S              : 제출(채점) — 대상은 Ctrl+Enter 와 같음
- Tab                 : 공백 4칸

문장 분리는 파이썬(split_statements)에서 한 번만 처리해 JS 와 규칙이 어긋나지 않게 한다.
"""

import re

import streamlit as st

_HTML = """
<div class="ed">
  <div class="bar">
    <button type="button" data-act="current">▶ 실행 <kbd>Ctrl+Enter</kbd></button>
    <button type="button" data-act="all">▶▶ 전체 실행 <kbd>Ctrl+Shift+Enter</kbd></button>
    <button type="button" data-act="submit" class="primary">✓ 제출 <kbd>Ctrl+S</kbd></button>
    <span class="hint"></span>
  </div>
  <div class="wrap">
    <pre class="hl" aria-hidden="true"><code></code></pre>
    <textarea spellcheck="false" wrap="off" autocomplete="off" autocapitalize="off"
              aria-label="SQL 에디터" placeholder="SELECT ...  (여러 문장은 ; 로 구분)"></textarea>
  </div>
</div>
"""

_CSS = """
.ed { font-family: var(--st-font); }
.bar { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-bottom: 6px; }
.bar button {
  font: inherit; font-size: 0.85rem; cursor: pointer;
  padding: 4px 10px; border-radius: var(--st-button-radius, 8px);
  border: 1px solid var(--st-border-color); background: var(--st-background-color);
  color: var(--st-text-color);
}
.bar button:hover { border-color: var(--st-primary-color); color: var(--st-primary-color); }
.bar button.primary { background: var(--st-primary-color); border-color: var(--st-primary-color); color: #fff; }
.bar button.primary:hover { filter: brightness(1.08); color: #fff; }
.bar kbd { font-size: 0.7rem; opacity: 0.75; margin-left: 4px; font-family: var(--st-font); }
.hint { font-size: 0.8rem; opacity: 0.7; margin-left: auto; }
.wrap {
  position: relative; height: 300px; min-height: 120px; resize: vertical; overflow: hidden;
  border: 1px solid var(--st-border-color); border-radius: var(--st-base-radius, 8px);
  background: var(--st-code-background-color, var(--st-secondary-background-color));
}
.wrap:focus-within { border-color: var(--st-primary-color); }
.hl, textarea {
  position: absolute; inset: 0; margin: 0; box-sizing: border-box;
  padding: 10px 12px; border: 0; outline: none;
  font-family: var(--st-code-font, ui-monospace, Consolas, monospace);
  font-size: 14px; line-height: 21px; tab-size: 4;
  white-space: pre; overflow: auto; overflow-wrap: normal;
}
.hl { pointer-events: none; color: var(--st-code-text-color, var(--st-text-color)); overflow: hidden; }
textarea {
  resize: none; background: transparent; color: transparent;
  caret-color: var(--st-text-color);
}
textarea::placeholder { color: var(--st-text-color); opacity: 0.4; }
textarea::selection { background: rgba(37, 99, 235, 0.28); color: transparent; }
.k { color: #2563eb; font-weight: 600; }
.f { color: #9333ea; }
.s { color: #16a34a; }
.n { color: #d97706; }
.c { color: #6b7280; font-style: italic; }
"""

_JS = """
const KEYWORDS = new Set(("select from where and or not in is null like between exists join inner left right " +
  "outer cross full on using group by order having limit offset as distinct union all intersect except case " +
  "when then else end with recursive over partition rows range unbounded preceding following current row " +
  "window asc desc insert update delete into values set create table view lateral true false interval " +
  "rollup any some desc describe show explain").split(" "));
const FUNCS = new Set(("count sum avg min max round floor ceil truncate concat concat_ws coalesce ifnull nullif " +
  "if date date_format datediff timestampdiff date_add date_sub year month day hour minute dayname dayofweek " +
  "last_day str_to_date cast left right substring substring_index length char_length lower upper replace " +
  "locate lpad rpad trim group_concat row_number rank dense_rank ntile lag lead first_value last_value " +
  "nth_value percent_rank cume_dist greatest least find_in_set field stddev_pop stddev_samp variance grouping " +
  "format mod abs now curdate").split(" "));
const TOKEN = /(--[^\\n]*|#[^\\n]*|\\/\\*[\\s\\S]*?(?:\\*\\/|$))|('(?:[^'\\\\]|\\\\.|'')*'?|"(?:[^"\\\\]|\\\\.)*"?|`[^`]*`?)|(\\b\\d+(?:\\.\\d+)?\\b)|([A-Za-z_][A-Za-z0-9_]*)/g;

function esc(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function highlight(text) {
  let out = "", last = 0, m;
  TOKEN.lastIndex = 0;
  while ((m = TOKEN.exec(text)) !== null) {
    out += esc(text.slice(last, m.index));
    const t = esc(m[0]);
    if (m[1]) out += `<span class="c">${t}</span>`;
    else if (m[2]) out += `<span class="s">${t}</span>`;
    else if (m[3]) out += `<span class="n">${t}</span>`;
    else {
      const w = m[4].toLowerCase();
      const next = text.slice(TOKEN.lastIndex).match(/^\\s*\\(/);
      if (KEYWORDS.has(w)) out += `<span class="k">${t}</span>`;
      else if (FUNCS.has(w) && next) out += `<span class="f">${t}</span>`;
      else out += t;
    }
    last = TOKEN.lastIndex;
  }
  // 마지막 줄바꿈 뒤에도 높이가 맞도록 한 줄을 더 둔다
  return out + esc(text.slice(last)) + "\\n";
}

export default function (component) {
  const { data, parentElement } = component;
  const ta = parentElement.querySelector("textarea");
  const code = parentElement.querySelector(".hl code");
  const pre = parentElement.querySelector(".hl");
  const hint = parentElement.querySelector(".hint");
  const wrap = parentElement.querySelector(".wrap");
  if (!ta || !code) return;

  // 핸들러는 요소당 한 번만 붙이고, 최신 component 객체는 요소에 보관해 참조한다
  ta._cmp = component;
  const render = () => { code.innerHTML = highlight(ta.value); syncScroll(); };
  const syncScroll = () => { pre.scrollTop = ta.scrollTop; pre.scrollLeft = ta.scrollLeft; };
  const updateHint = () => {
    hint.textContent = ta.selectionEnd > ta.selectionStart ? "선택 영역 실행" : "커서 위치 문장 실행";
  };
  const send = (action) => {
    const cmp = ta._cmp;
    cmp.setStateValue("value", ta.value);
    cmp.setTriggerValue("run", {
      action, text: ta.value,
      sel_start: ta.selectionStart, sel_end: ta.selectionEnd, nonce: Date.now(),
    });
  };

  if (!ta.dataset.ready) {
    ta.dataset.ready = "1";
    ta.value = data?.value ?? "";
    ta.dataset.version = String(data?.version ?? 0);
    if (data?.height) wrap.style.height = `${data.height}px`;
    render();
    ta.addEventListener("input", render);
    ta.addEventListener("scroll", syncScroll);
    ["keyup", "mouseup", "select", "focus"].forEach((ev) => ta.addEventListener(ev, updateHint));
    ta.addEventListener("blur", () => ta._cmp.setStateValue("value", ta.value));
    ta.addEventListener("keydown", (e) => {
      const mod = e.ctrlKey || e.metaKey;
      if (mod && e.key === "Enter") {
        e.preventDefault();
        send(e.shiftKey ? "all" : "current");
      } else if (mod && (e.key === "s" || e.key === "S")) {
        e.preventDefault();
        send("submit");
      } else if (e.key === "Tab" && !mod && !e.shiftKey) {
        e.preventDefault();
        document.execCommand("insertText", false, "    ");
      }
    });
    parentElement.querySelectorAll(".bar button").forEach((b) => {
      // 버튼을 눌러도 textarea 의 선택 영역이 사라지지 않게 포커스 이동을 막는다
      b.addEventListener("mousedown", (e) => e.preventDefault());
      b.addEventListener("click", () => send(b.dataset.act));
    });
    updateHint();
  } else if (String(data?.version ?? 0) !== ta.dataset.version) {
    // 파이썬 쪽에서 내용을 바꾼 경우(예: 초기화)에만 덮어쓴다
    ta.dataset.version = String(data?.version ?? 0);
    ta.value = data?.value ?? "";
    render();
  }
}
"""

_COMPONENT = st.components.v2.component("sql_editor", html=_HTML, css=_CSS, js=_JS)


def sql_editor(*, key: str, value: str, version: int = 0, height: int = 300) -> tuple[dict | None, str | None]:
    """에디터를 그리고 (실행 요청, 마지막으로 저장된 텍스트) 를 돌려준다.

    실행 요청은 {"action": "current"|"all"|"submit", "text", "sel_start", "sel_end"} 또는 None.
    """
    result = _COMPONENT(
        key=key,
        data={"value": value, "version": version, "height": height},
        on_run_change=lambda: None,
        on_value_change=lambda: None,
    )
    return result.run, result.value


# ---------- 문장 분리 ----------

_COMMENT_ONLY = re.compile(r"^(\s|--[^\n]*|#[^\n]*|/\*.*?\*/)*$", re.S)


def split_statements(text: str) -> list[tuple[int, int, str]]:
    """세미콜론으로 문장을 나눈다. 문자열·백틱·주석 안의 ; 는 무시한다.

    (시작 위치, 끝 위치(; 다음), 문장) 목록을 돌려준다. 빈 문장도 포함한다.
    """
    out, start, i, n = [], 0, 0, len(text)
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if ch in "'\"`":
            i += 1
            while i < n and text[i] != ch:
                i += 2 if text[i] == "\\" and ch != "`" else 1
        elif ch == "-" and nxt == "-" or ch == "#":
            while i < n and text[i] != "\n":
                i += 1
        elif ch == "/" and nxt == "*":
            end = text.find("*/", i + 2)
            i = n if end < 0 else end + 1
        elif ch == ";":
            out.append((start, i + 1, text[start:i]))
            start = i + 1
        i += 1
    if start < n:
        out.append((start, n, text[start:]))
    return out


def is_empty(sql: str) -> bool:
    return bool(_COMMENT_ONLY.match(sql))


def pick_statements(text: str, sel_start: int, sel_end: int, action: str) -> list[str]:
    """실행할 문장 목록을 정한다. 선택 영역 > (전체 실행이면 전체) > 커서 위치 문장."""
    if sel_end > sel_start:
        return [s for _, _, s in split_statements(text[sel_start:sel_end]) if not is_empty(s)]
    stmts = split_statements(text)
    if action == "all":
        return [s for _, _, s in stmts if not is_empty(s)]
    filled = [(a, b, s) for a, b, s in stmts if not is_empty(s)]
    if not filled:
        return []
    # 커서가 문장 범위 안이면 그 문장, 문장 사이 공백이면 바로 앞 문장(없으면 다음 문장)
    for a, b, s in filled:
        if a <= sel_start <= b:
            return [s]
    before = [x for x in filled if x[1] <= sel_start]
    return [(before[-1] if before else filled[0])[2]]
