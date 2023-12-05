// userSlice.js
import { createSlice } from "@reduxjs/toolkit";

export const classesSlice = createSlice({
  name: "classes",
  initialState: {
    class_id: null,
    grade: 0,
    name: "",
    type: [],
    details: [],
    students_details: [],
    teachers_details: [],
    presences: [],
  },
  reducers: {
    setClassesData: (state, action) => {
      const { id, grade, name, type, students_details, teachers_details } =
        action.payload;

      state.class_id = id;
      state.grade = grade;
      state.name = name;
      state.type = type;
      state.students_details = students_details;
      state.teachers_details = teachers_details;
      state.presences = [];
    },
    setPresences: (state, action) => {
      state.presences = action.payload;
    },
  },
});

export const { setClassesData } = classesSlice.actions;

export default classesSlice.reducer;
