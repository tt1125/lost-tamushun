import { functions, storage } from "@/lib/Firebase";
import { httpsCallable } from "firebase/functions";
import { getStorage, ref, uploadBytes, getDownloadURL } from "firebase/storage";

export default class Upload {
  async uploadImg(file, option) {
    try {
      console.log("file", file.name);
      const storageRef = ref(storage, `org-imgs/${file.name}`);
      const snapshot = await uploadBytes(storageRef, file);
      const create = httpsCallable(functions, "create");
      await create({
        selections: option,
        add_prompt: "",

      })
      const downloadURL = await getDownloadURL(snapshot.ref);
      return downloadURL;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
}
