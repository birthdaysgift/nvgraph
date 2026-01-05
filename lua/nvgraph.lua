local window = require("nvgraph.window")

M = {}


function M.open()
  window.create({"This is", "your plugin window."})
end


return M
