
import { firestore, functions } from "@/lib/Firebase";
import {
  collection,
  getDocs,
  doc,
  setDoc,
  getDoc,
  deleteDoc,
  query,
  where,
} from "firebase/firestore";

import {httpsCallable} from "firebase/functions";

export default class FetchPost {
  async createPost(title, genImgUrl, orgImgUrl, description, uid , file) {
 await setDoc(doc(firestore, "post", id), {
      uid,
      title,
      genImgUrl,
      orgImgUrl,
      description,
    });

  }

  async fetchUserPosts(uid) {
    if (!uid) {
      throw new Error("ユーザーIDがありません");
    }
    const userPostsQuery = query(
      collection(firestore, "post"),
      where("uid", "==", uid)
    );
    const postSnaps = await getDocs(userPostsQuery);
    return postSnaps.docs.map((postSnap) => ({
      id: postSnap.id,
      ...postSnap.data(),
    }));
  }

  async fetchPost(id) {
    const postRef = doc(firestore, `post/${id}`);
    const postSnap = await getDoc(postRef);
    if (postSnap.exists()) {
      const appPost = postSnap.data();
      return { ...appPost, id: id };
    } else {
      throw new Error("ポスト情報が存在しません");
    }
  }

  async fetchPosts() {
    const postSnaps = await getDocs(collection(firestore, "post"));
    return postSnaps.docs.map((postSnap) => ({
      id: postSnap.id,
      ...postSnap.data(),
    }));
  }

  async updatePost(id, datas) {
    try {
      const postRef = doc(firestore, `post/${id}`);
      await setDoc(postRef, datas);
    } catch (error) {
      throw new Error(error);
    }
  }

  async deletePost(id) {
    try {
      await deleteDoc(doc(firestore, `post/${id}`));
    } catch (error) {
      throw new Error(error);
    }
  }
}
