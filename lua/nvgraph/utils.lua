M = {}


function M.strsplit(s, sep, plain, n)
    -- this function is just copied from https://github.com/lunarmodules/Penlight

    local i1, ls = 1, {}
    if not sep then
        sep = '%s+'
    end

    if sep == '' then
        return {s}
    end

    while true do
        local i2, i3 = string.find(s, sep, i1, plain)
        if not i2 then
            local last = string.sub(s, i1)
            if last ~= '' then
                table.insert(ls, last)
            end
            if #ls == 1 and ls[1] == '' then
                return {}
            else
                return ls
            end
        end
        table.insert(ls, string.sub(s, i1, i2 - 1))
        if n and #ls == n then
            ls[#ls] = string.sub(s, i1)
            return ls
        end
        i1 = i3 + 1
    end
end


return M
