// userSlice.js
import { createSlice } from "@reduxjs/toolkit";

export const userSlice = createSlice({
  name: "user",
  initialState: {
    user_id: null,
    role: null,
    token: null,
    fullName: "",
  },
  reducers: {
    login: (state, action) => {
      const { user_id, role, token, fullName } = action.payload;
      state.user_id = user_id;
      state.role = role;
      state.token = token;
      state.fullName = fullName;
    },
    logout: (state) => {
      state.user_id = null;
      state.role = null;
      state.token = null;
      state.fullName = "";
    },
  },
});

export const { login, logout } = userSlice.actions;

export default userSlice.reducer;
