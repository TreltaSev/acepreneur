import { set_preference } from "@internal"

export async function setUserId(id: string) {
    await set_preference("identity", id);
}