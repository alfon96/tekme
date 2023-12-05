// userSlice.js
import { createSlice } from "@reduxjs/toolkit";

export const selectorSlice = createSlice({
  name: "selector",
  initialState: {
    activeComponentIndex: 0,
  },
  reducers: {
    setActiveComponentIndex: (state, action) => {
      const { activeComponentIndex } = action.payload;
      state.activeComponentIndex = activeComponentIndex;
    },
  },
});

export const { setActiveComponentIndex } = selectorSlice.actions;

export default selectorSlice.reducer;
