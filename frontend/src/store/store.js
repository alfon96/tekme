import { configureStore } from "@reduxjs/toolkit";
import storage from "redux-persist/lib/storage";
import { persistReducer, persistStore } from "redux-persist";
import { encryptTransform } from "redux-persist-transform-encrypt";
import userReducer from "./userSlice";
import editingSlice from "./editingSlice";
import classesSlice from "./classesSlice";

const secretKey = process.env.REACT_APP_SECRET_KEY;

const persistConfig = {
  key: "root",
  storage,
  transforms: [
    encryptTransform({
      secretKey, // Assuming secretKey is defined and valid
      onError: function (error) {
        // Handle the encryption error
        console.error("Encryption error:", error);
      },
    }),
  ],
};

// Since you only have one reducer, pass it directly to persistReducer
const persistedReducer = persistReducer(persistConfig, userReducer);

export const store = configureStore({
  reducer: {
    auth: persistedReducer,
    editing: editingSlice,
    classes: classesSlice,
  },
});

export const persistor = persistStore(store);
