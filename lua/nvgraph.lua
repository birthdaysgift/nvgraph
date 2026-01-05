local cmd = require("nvgraph.cmd")
local utils = require("nvgraph.utils")
local window = require("nvgraph.window")


M = {}


function M.open()
  local log = cmd.get_log()
  local lines = utils.strsplit(log, "\n")

  window.create(lines)
end


return M
