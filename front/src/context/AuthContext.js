'use client'

import React, {
    createContext,
    useState,
    useContext,
    useEffect,
} from 'react'
import { auth } from '@/lib/Firebase'
import FetchUser from '@/fetch/user'
import Login from '@/component/Login'
import { dividerClasses } from '@mui/material'

// コンテキストの作成
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);

    const fetchUser = new FetchUser();

    useEffect(() => {
        const unsubscribe = auth.onAuthStateChanged(async (firebaseUser) => {
            if (firebaseUser) {
                const userInfo = await fetchUser.fetchUser(firebaseUser.uid);
                setUser(userInfo);
            } else {
                setUser(null);
            }
        });
        return () => unsubscribe();
    }, []);

    const getUser = async () => {
        const userInfo = await fetchUser.fetchUser(user?.uid ?? '');
        setUser(userInfo);
    };

    return (
        <AuthContext.Provider value={{ user, fetchUser }}>
            {user ? children : user === null ? <Login /> : <div>loading ...</div>}
        </AuthContext.Provider>
    );
}

// コンテキストを使うためのカスタムフック
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
