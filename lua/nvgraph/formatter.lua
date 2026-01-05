M = {}


local function format_parents(parents)
  return " [" .. table.concat(parents, ", ") .. "] "
end


local function format_refs(refs)
  return " (" .. table.concat(refs, ", ") .. ") "
end


function M.format_lines(graph_data)
  local lines = {}
  local branches = 0
  local main_commit = nil

  local commits, tree = unpack(graph_data)
  for _, data in ipairs(commits) do

    local current_hash = data["hash"]


    if #tree[current_hash]["children"] > 0 then
      branches = branches - (#tree[current_hash]["children"] - 1)
    end

    if #tree[current_hash].children == 0 and main_commit then
      branches = branches + 1
    end


    local refs = format_refs(data["refs"])

    if main_commit and current_hash == main_commit then
      local line = " * " .. current_hash .. refs
      table.insert(lines, line)
    else
      local line = string.rep(" | ", branches) .. " * " .. current_hash .. refs
      table.insert(lines, line)
    end

    if #tree[current_hash]["parents"] == 2 then
      branches = branches + 1
      main_commit = tree[current_hash]["parents"][1]
    end

  end

  return lines
end


return M

