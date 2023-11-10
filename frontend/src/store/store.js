import { configureStore } from '@reduxjs/toolkit';
import storage from 'redux-persist/lib/storage';
import { persistReducer, persistStore } from 'redux-persist';
import userReducer from './userSlice';
import { encryptTransform } from 'redux-persist-transform-encrypt';

const secretKey = process.env.REACT_APP_SECRET_KEY;

const persistConfig = {
    key: 'root',
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
    reducer: persistedReducer, // Pass the persistedReducer directly
});

export const persistor = persistStore(store);
