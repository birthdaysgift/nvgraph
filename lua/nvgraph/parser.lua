local utils = require("nvgraph.utils")


M = {}


function M.parse(log)
  local data = {}

  local lines = utils.strsplit(log, "\n")
  for _, line in ipairs(lines) do
    local line_data = utils.strsplit(line, "%z")

    table.insert(
      data,
      {
        hash = line_data[1],
        parents = line_data[2],
        refs = line_data[3],
        subject = line_data[4],
        author = line_data[5],
      }
    )
  end

  return data
end


return M
