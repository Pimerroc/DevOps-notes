-- Livecoding logger for Neovim.
-- Writes metadata-only JSONL events. It does not record buffer contents or full commands.
--
-- Capture strategy:
--   * VimEnter -> start
--   * timer every 500 ms -> buffer delta snapshots (reliable even if TextChanged is skipped)
--   * TextChanged/TextChangedI/InsertLeave -> immediate buffer flush
--   * vim.on_key -> aggregate keystroke counters (flushed once per second)
--   * BufWritePost, CmdlineLeave, ModeChanged, DiagnosticChanged, Focus*, VimLeavePre
local log_path = vim.env.LIVECODING_LOG
if not log_path or log_path == "" then
  return
end

local uv = vim.uv or vim.loop
local start_ms = math.floor(uv.hrtime() / 1000000)
local snapshots = {}
local last_tick = {}
local key_ns = uv.hrtime()

local pending = {
  keys = 0,
  typed = 0,
}

local severity_name = {
  [vim.diagnostic.severity.ERROR] = "ERROR",
  [vim.diagnostic.severity.WARN] = "WARN",
  [vim.diagnostic.severity.INFO] = "INFO",
  [vim.diagnostic.severity.HINT] = "HINT",
}

local function now_ms()
  return math.floor(uv.hrtime() / 1000000)
end

local function iso_now()
  return os.date("!%Y-%m-%dT%H:%M:%SZ")
end

local function write_event(ev)
  ev.ts = iso_now()
  ev.ms = now_ms()
  ev.session = vim.env.LIVECODING_SESSION
  local ok, encoded = pcall(vim.json.encode, ev)
  if not ok then
    return
  end
  local f = io.open(log_path, "a")
  if not f then
    return
  end
  f:write(encoded, "\n")
  f:close()
end

local function buf_stats(buf)
  local lines = vim.api.nvim_buf_get_lines(buf, 0, -1, false)
  local chars = 0
  for _, line in ipairs(lines) do
    chars = chars + #line + 1
  end
  return chars, #lines
end

local function snapshot(buf)
  local chars, lines = buf_stats(buf)
  snapshots[buf] = { chars = chars, lines = lines }
  last_tick[buf] = vim.api.nvim_buf_get_changedtick(buf)
end

local function flush_buffer(buf)
  if not vim.api.nvim_buf_is_valid(buf) or not vim.api.nvim_buf_is_loaded(buf) then
    return
  end
  local tick = vim.api.nvim_buf_get_changedtick(buf)
  if last_tick[buf] == tick then
    return
  end
  last_tick[buf] = tick
  local chars, lines = buf_stats(buf)
  local prev = snapshots[buf]
  if not prev then
    snapshot(buf)
    return
  end
  local delta = chars - prev.chars
  if delta ~= 0 then
    write_event({
      event = "edit",
      buf = buf,
      file = vim.api.nvim_buf_get_name(buf),
      delta = delta,
      chars = chars,
      lines = lines,
      mode = vim.api.nvim_get_mode().mode,
    })
  end
  snapshots[buf] = { chars = chars, lines = lines }
end

local function flush_all_buffers()
  for _, buf in ipairs(vim.api.nvim_list_bufs()) do
    flush_buffer(buf)
  end
end

local function flush_keys()
  if pending.keys == 0 and pending.typed == 0 then
    return
  end
  write_event({
    event = "keys",
    keys = pending.keys,
    typed = pending.typed,
    mode = vim.api.nvim_get_mode().mode,
  })
  pending.keys = 0
  pending.typed = 0
end

local function on_buf_enter(buf)
  if not vim.api.nvim_buf_is_valid(buf) then
    return
  end
  local name = vim.api.nvim_buf_get_name(buf)
  if name == "" then
    return
  end
  flush_buffer(buf)
  snapshot(buf)
  write_event({
    event = "buf_enter",
    buf = buf,
    file = name,
    filetype = vim.bo[buf].filetype,
    lines = vim.api.nvim_buf_line_count(buf),
  })
end

local group = vim.api.nvim_create_augroup("LivecodingLogger", { clear = true })

local function log_start()
  write_event({
    event = "start",
    cwd = vim.fn.getcwd(),
    file = vim.fn.expand("%:p"),
    version = vim.version().major .. "." .. vim.version().minor .. "." .. vim.version().patch,
  })
end

-- In headless mode VimEnter is not guaranteed before -c commands run, so log
-- start immediately. The real file is captured by BufEnter right after loading.
log_start()

vim.api.nvim_create_autocmd("BufEnter", {
  group = group,
  callback = function(args)
    on_buf_enter(args.buf)
  end,
})

vim.api.nvim_create_autocmd("BufWritePost", {
  group = group,
  callback = function(args)
    flush_buffer(args.buf)
    write_event({
      event = "save",
      file = vim.api.nvim_buf_get_name(args.buf),
      lines = vim.api.nvim_buf_line_count(args.buf),
    })
  end,
})

vim.api.nvim_create_autocmd({ "TextChanged", "TextChangedI", "InsertLeave" }, {
  group = group,
  callback = function(args)
    flush_buffer(args.buf)
  end,
})

vim.api.nvim_create_autocmd("CmdlineLeave", {
  group = group,
  callback = function()
    local cmd = vim.fn.getcmdline()
    local first = cmd:match("^%s*(%S+)") or ""
    -- Only the command name is stored, never its arguments.
    write_event({
      event = "cmdline",
      cmdtype = vim.fn.getcmdtype(),
      cmd = first,
      len = #cmd,
    })
  end,
})

vim.api.nvim_create_autocmd("ModeChanged", {
  group = group,
  callback = function()
    write_event({
      event = "mode",
      mode = vim.api.nvim_get_mode().mode,
    })
  end,
})

vim.api.nvim_create_autocmd("DiagnosticChanged", {
  group = group,
  callback = function()
    local counts = { ERROR = 0, WARN = 0, INFO = 0, HINT = 0 }
    for _, d in ipairs(vim.diagnostic.get(0)) do
      local name = severity_name[d.severity] or "UNKNOWN"
      counts[name] = (counts[name] or 0) + 1
    end
    write_event({ event = "diagnostics", counts = counts })
  end,
})

vim.api.nvim_create_autocmd({ "FocusGained", "FocusLost" }, {
  group = group,
  callback = function(args)
    write_event({ event = "focus", state = args.event })
  end,
})

vim.api.nvim_create_autocmd("VimLeavePre", {
  group = group,
  callback = function()
    flush_all_buffers()
    flush_keys()
    write_event({
      event = "stop",
      duration_ms = now_ms() - start_ms,
      cwd = vim.fn.getcwd(),
    })
  end,
})

vim.on_key(function(_, typed)
  pending.keys = pending.keys + 1
  if typed and #typed > 0 then
    pending.typed = pending.typed + #typed
  end
end, key_ns)

local timer = uv.new_timer()
timer:start(
  500,
  500,
  vim.schedule_wrap(function()
    flush_all_buffers()
    flush_keys()
  end)
)

vim.api.nvim_create_autocmd("VimLeavePre", {
  group = group,
  callback = function()
    timer:stop()
    timer:close()
    vim.on_key(nil, key_ns)
  end,
})
