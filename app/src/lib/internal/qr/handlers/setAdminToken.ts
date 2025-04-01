import { set_preference } from "@internal"

export async function setAdminToken(token: string) {
    console.log("setting admin token", token)
    await set_preference("admin_token", token);
}