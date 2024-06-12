import { firestore } from '@/lib/Firebase'
import {
    collection,
    getDocs,
    doc,
    setDoc,
    getDoc,
    deleteDoc,
} from 'firebase/firestore'
import { signInWithEmailAndPassword,createUserWithEmailAndPassword ,signOut } from '@firebase/auth'
import { auth } from '@/lib/Firebase'


export default class FetchUser {

    async loginWithEmail(email, password) {
        try {
            await signInWithEmailAndPassword(auth, email, password)
        } catch (error) {
            throw new Error(error.message)
        }
    }

    async logout() {
        try {
            await signOut(auth)
        } catch (error) {
            throw new Error(error.message)
        }
    }

    async createUser(name, email, password) {
        await createUserWithEmailAndPassword(auth, email, password)
            .then(async (userCredential) => {
                const { user } = userCredential
                const { uid } = user
                await setDoc(doc(firestore, 'user', uid), {
                    name,
                    email,
                })
            })
            .catch((error) => {
                throw new Error(error.message)
            })

    }

    async fetchUser(uid) {
        const userRef = doc(firestore, `user/${uid}`)
        const userSnap = await getDoc(userRef)
        if (userSnap.exists()) {
            const appUser = userSnap.data()
            return { ...appUser, uid: uid }
        } else {
            throw new Error('ユーザー情報が存在しません')
        }
    }

    async fetchUsers() {
        const userSnaps = await getDocs(collection(firestore, 'user'))
        return userSnaps.docs.map((userSnap) => ({
            uid: userSnap.id,
            ...(userSnap.data()),
        }))
    }

    async updateUser(uid, name) {
        const userRef = doc(firestore, `user/${uid}`);
        const userSnap = await getDoc(userRef);

        if (userSnap.exists()) {
            await setDoc(userRef, {
                ...(name !== undefined && { name }),
            }, { merge: true });
        } else {
            throw new Error('ユーザーが存在しません');
        }
    }

    async deleteUser(uid) {
        const body = {
            uid: uid
        }
        try {
            await deleteDoc(doc(firestore, `user/${uid}`))
            await fetch('/api/auth/deleteUser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body)
            })
        } catch (error) {
            throw new Error(error)
        }
    }

}