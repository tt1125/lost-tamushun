import { initializeApp, getApps, FirebaseApp } from 'firebase/app'
import { getFirestore, Firestore, connectFirestoreEmulator } from 'firebase/firestore'
import { getAuth, Auth, connectAuthEmulator } from 'firebase/auth'
import { getStorage, FirebaseStorage, connectStorageEmulator } from 'firebase/storage'
import { getFunctions, connectFunctionsEmulator } from 'firebase/functions'

const firebaseConfig = {
    apiKey: "AIzaSyAAbcoJux_DTnbTEAT6yzGVdFHqKL4HefE",
    authDomain: "lost-tamushun-63dc1.firebaseapp.com",
    projectId: "lost-tamushun-63dc1",
    storageBucket: "lost-tamushun-63dc1.appspot.com",
    messagingSenderId: "173376715412",
    appId: "1:173376715412:web:db2f6895c0c28408179281",
    measurementId: "G-7H2FL8K9LG"
};

let firebaseApp, auth, firestore, storage, functions

// サーバーサイドでレンダリングするときにエラーが起きないようにするための記述
if (typeof window !== 'undefined' && !getApps().length) {
    firebaseApp = initializeApp(firebaseConfig)
    auth = getAuth(firebaseApp)
    firestore = getFirestore(firebaseApp)
    storage = getStorage(firebaseApp)
    functions = getFunctions(firebaseApp)
}

if (process.env.NODE_ENV == "development") {
    connectAuthEmulator(auth, 'http://localhost:9099')
    connectStorageEmulator(storage, 'localhost', 9199)
    connectFunctionsEmulator(functions, 'localhost', 5001)
    connectFirestoreEmulator(firestore, 'localhost', 8080)
}

export { firebaseApp, auth, firestore, storage }