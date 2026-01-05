M = {}


function M.format_lines(graph_data)
  local lines = {}
  for _, data in ipairs(graph_data) do
    local line = " * " .. data["hash"] .. " [" .. data["parents"] .. "] (" .. data["refs"] .. ") "
    table.insert(lines, line)
  end
  return lines
end


return M

