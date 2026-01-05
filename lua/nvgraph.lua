local cmd = require("nvgraph.cmd")
local formatter = require("nvgraph.formatter")
local parser = require("nvgraph.parser")
local window = require("nvgraph.window")


M = {}


function M.open()
  local log = cmd.get_log()
  local data = parser.parse(log)
  local lines = formatter.format_lines(data)

  window.create(lines)
end


return M
