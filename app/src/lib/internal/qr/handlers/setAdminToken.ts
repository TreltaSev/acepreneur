import { set_preference } from "@internal"

export async function setAdminToken(token: string) {
    await set_preference("admin_token", token);
}