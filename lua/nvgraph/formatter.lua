M = {}


local function format_parents(parents)
  return " [" .. table.concat(parents, ", ") .. "] "
end


local function format_refs(refs)
  return " (" .. table.concat(refs, ", ") .. ") "
end


function M.format_lines(graph_data)
  local lines = {}
  for _, data in ipairs(graph_data) do
    local parents = format_parents(data["parents"])
    local refs = format_refs(data["refs"])
    local line = " * " .. data["hash"] .. parents .. refs
    table.insert(lines, line)
  end
  return lines
end


return M

