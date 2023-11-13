import { createSlice, current } from '@reduxjs/toolkit';

const initialState = {
    dataTitle: '',
    currentData: [],
    selectedElements: [],
    history: [[]],
    currentIndex: 0,
    disableUndo: true,
    disableRedo: true,
    disableEdit: true,
    error: null,
    editableData: null,
};

const updateDisabledStates = (state) => {
    state.disableUndo = state.currentIndex <= 0;
    state.disableRedo = state.currentIndex >= state.history.length - 1;

    // Disable save if there are no modifications
    state.disableSave = state.history.length === 1 &&
        JSON.stringify(state.currentData) === JSON.stringify(state.history[0]);

    // Disable delete if no elements are selected
    state.disableDel = state.selectedElements.length === 0;
    // Disable edit if not exactly one element is selected
    state.disableEdit = state.selectedElements.length !== 1;
};

const isObjectEqual = (obj1, obj2) => {
    const excludedKeys = ['index', 'id', 'parents'];
    const keys1 = Object.keys(obj1).filter(key => !excludedKeys.includes(key));
    const keys2 = Object.keys(obj2).filter(key => !excludedKeys.includes(key));

    if (keys1.length !== keys2.length) {
        return false;
    }

    for (const key of keys1) {

        if (obj1[key] !== obj2[key]) {
            return false;
        }
    }

    return true;
};

const isDuplicateData = (currentData, newData) => {

    // Ensure newData is always treated as an array
    const newDataArray = Array.isArray(newData) ? newData : [newData];

    // Check only the last element of currentData if length >= 1
    if (currentData.length >= 1) {
        const lastItem = currentData[currentData.length - 1];

        return newDataArray.some(newItem => isObjectEqual(lastItem, newItem));
    }

};


export const editingSlice = createSlice({
    name: 'data',
    initialState,
    reducers: {
        setDataTitle: (state, action) => {
            state.dataTitle = action.payload;
            state.currentData = [];
            state.selectedElements = [];
            state.history = [[]];
            state.currentIndex = 0;
            updateDisabledStates(state);
        },

        updateData: (state, action) => {
            if (!isDuplicateData(state.currentData, action.payload)) {
                // If history only has the initial empty state, replace it
                if (state.history.length === 1 && state.history[0].length === 0) {
                    state.history[0] = [action.payload];
                } else {
                    state.history = state.history.slice(0, state.currentIndex + 1);
                    state.history.push([...state.currentData, action.payload]);
                }
                state.currentData = [...state.currentData, action.payload];
                state.currentIndex = state.history.length - 1;
                state.error = null;
            } else {
                state.error = "Tried to insert duplicated data.";
            }
            updateDisabledStates(state);
        },

        toggleSelectElement: (state, action) => {
            const elementId = action.payload.id; // Assuming each element has a unique 'id' property
            const elementIndex = state.selectedElements.findIndex(el => el.id === elementId);
            if (elementIndex >= 0) {
                state.selectedElements.splice(elementIndex, 1);
                // Disable editing if the user clicks away
                if (state.editableData.id === elementId) {
                    state.disableEdit = true;
                    state.editableData = null;
                }
            } else {
                state.selectedElements.push(action.payload);
            }
            updateDisabledStates(state);
        },

        resetError: (state) => {
            state.error = null;
        },

        del: (state) => {
            // Filter out selected elements from currentData
            state.currentData = state.currentData.filter(
                currentEl => !state.selectedElements.some(
                    selectedEl => selectedEl.id === currentEl.id
                )
            );

            // Clear the selectedElements array after deletion
            state.selectedElements = [];

            // Update history with the new currentData
            state.history = state.history.slice(0, state.currentIndex + 1);
            state.history.push([...state.currentData]);

            // Update currentIndex to point to the latest state
            state.currentIndex = state.history.length - 1;

            // Update disableUndo, disableRedo, and other related states
            updateDisabledStates(state);
        },

        undo: (state) => {
            if (state.currentIndex > 0) {
                state.currentIndex--;
                state.currentData = state.history[state.currentIndex];
            }
            updateDisabledStates(state);
        },

        redo: (state) => {
            if (state.currentIndex < state.history.length - 1) {
                state.currentIndex++;
                state.currentData = state.history[state.currentIndex];
            }
            updateDisabledStates(state);
        },

        startEdit: (state) => {
            // If the edit mode is already active and the selected element is the same
            // as the one that is currently being edited, toggle the edit mode off.
            if (state.editableData && state.selectedElements.length === 1 &&
                state.selectedElements[0].id === state.editableData.id) {
                state.editableData = null;
            } else if (state.selectedElements.length === 1) {
                // Otherwise, if exactly one item is selected, start editing that item.
                state.editableData = state.selectedElements[0];
            } else {
                // If no items are selected, or more than one are selected,
                // do not start editing and set an error message.
                state.editableData = null;
                state.error = 'Please select exactly one item to edit.';
            }
            updateDisabledStates(state);
            // Additionally, you might want to toggle the `disableEdit` state
            // based on whether `editableData` is null.
            state.disableEdit = !state.editableData;

        },


        // Apply the edited data to the currentData
        applyEdit: (state, action) => {
            const { id, ...updatedData } = action.payload;
            console.log("DOWN");
            console.log(id);
            console.log("UP");
            const index = state.currentData.findIndex(item => item.id === id);
            console.log(index);
            if (index !== -1) {
                console.log("Id found");
                state.currentData[index] = { id, ...updatedData };
                state.history = state.history.slice(0, state.currentIndex + 1);
                state.history.push([...state.currentData]);
                state.currentIndex = state.history.length - 1;
                state.selectedElements = [];
            } else {
                state.error = "The item to update doesn't exist.";
            }
            updateDisabledStates(state);
        },
    },
});

export const { setDataTitle, updateData, toggleSelectElement, del, undo, redo, resetError, startEdit, applyEdit } = editingSlice.actions;

export default editingSlice.reducer;
