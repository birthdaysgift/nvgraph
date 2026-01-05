M = {}


function M.strsplit(str, sep)
    local t = {}
    -- default separator is whitespace
    sep = sep or "%s"
    for field in str:gmatch("([^" .. sep .. "]+)") do
        table.insert(t, field)
    end
    return t
end


return M
