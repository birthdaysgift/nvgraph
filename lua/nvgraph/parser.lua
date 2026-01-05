local utils = require("nvgraph.utils")


M = {}


local function parse_parents(parents_str)
  return utils.strsplit(parents_str, " ")
end


local function parse_refs(refs_str)
  return utils.strsplit(refs_str, ",%s")
end


function M.parse(log)
  local commits = {}
  local tree = {}

  local lines = utils.strsplit(log, "\n")
  for _, line in ipairs(lines) do
    local hash, parents, refs, subject, author = unpack(utils.strsplit(line, "%z"))

    table.insert(
      commits,
      {
        hash = hash,
        refs = parse_refs(refs),
        subject = subject,
        author = author,
      }
    )

    local parent_hashes = parse_parents(parents)
    if not tree[hash] then
      tree[hash] = {
        parents = parent_hashes,
        children = {},
      }
    else
      for _, parent in ipairs(parent_hashes) do
        table.insert(tree[hash]["parents"], parent)
      end
    end

    for _, parent_hash in ipairs(parent_hashes) do
      if not tree[parent_hash] then
        tree[parent_hash] = {
          parents = {},
          children = {hash}
        }
      else
        table.insert(tree[parent_hash]["children"], hash)
      end
    end

  end
  return {commits, tree}
end


return M
