import { configureStore } from "@reduxjs/toolkit";
import storage from "redux-persist/lib/storage";
import { persistReducer, persistStore } from "redux-persist";
import { encryptTransform } from "redux-persist-transform-encrypt";
import userReducer from "./userSlice";
import selectorSlice from "./selectorSlice";
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

const persistedUserAuthenticationReducer = persistReducer(
  persistConfig,
  userReducer
);
const persistedClassesInfoReducer = persistReducer(persistConfig, classesSlice);

export const store = configureStore({
  reducer: {
    auth: persistedUserAuthenticationReducer,
    selector: selectorSlice,
    classes: persistedClassesInfoReducer,
  },
});

export const persistor = persistStore(store);
