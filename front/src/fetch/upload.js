import { storage } from "@/lib/Firebase";
import { getStorage, ref, uploadBytes, getDownloadURL } from "firebase/storage";

export default class Upload {
  async uploadImg(file) {
    try {
      console.log("file", file.name);
      const storageRef = ref(storage, `org-imgs/${file.name}`);
      const snapshot = await uploadBytes(storageRef, file);
      const downloadURL = await getDownloadURL(snapshot.ref);
      return downloadURL;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
}
