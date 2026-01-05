M = {}


local function create_buffer(lines)
  local buf_id = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_buf_set_lines(buf_id, 0, -1, false, lines)
  return buf_id
end


function M.create(lines)
  local buf_id = create_buffer(lines)

  local ui = vim.api.nvim_list_uis()[1]
  local width = math.floor(ui.width * 0.9)
  local height = math.floor(ui.height * 0.9)
  local row = math.floor((ui.height - height) / 2)
  local col = math.floor((ui.width - width) / 2)

  local win_id = vim.api.nvim_open_win(
    buf_id,
    true,
    {
      relative = "editor",
      width = width,
      height = height,
      row = row,
      col = col,
      style = "minimal",
      border = "rounded",
    }
  )

  vim.keymap.set(
    "n",
    "<Esc>",
    function()
      vim.api.nvim_win_close(win_id, true)
    end,
    { buffer = true }
  )
end


return M
