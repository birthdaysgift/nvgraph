M = {}


local cmd = [[ git log --all --pretty="format:%h%x00%p%x00%D%x00%s%x00%an" --max-count=100 --topo-order]]


function M.get_log()
  local io_handle = io.popen(cmd)
  assert(io_handle)

  local cmd_out = io_handle:read('*a')
  io_handle:close()
  return cmd_out
end


return M

