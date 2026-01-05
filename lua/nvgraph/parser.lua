local utils = require("nvgraph.utils")


M = {}


local function parse_parents(parents_str)
  return utils.strsplit(parents_str, " ")
end


local function parse_refs(refs_str)
  return utils.strsplit(refs_str, ",%s")
end


function M.parse(log)
  local data = {}

  local lines = utils.strsplit(log, "\n")
  for _, line in ipairs(lines) do
    local hash, parents, refs, subject, author = unpack(utils.strsplit(line, "%z"))

    table.insert(
      data,
      {
        hash = hash,
        parents = parse_parents(parents),
        refs = parse_refs(refs),
        subject = subject,
        author = author,
      }
    )
  end

  return data
end


return M
