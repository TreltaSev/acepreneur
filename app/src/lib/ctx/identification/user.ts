import { get_local, has_local, set_local } from "@root/lib/internal";
import { authform, fetch_backend, jsonform } from "@root/lib/internal/fetch";

export class User {

    constructor() {

    }

    /**
     * Requests a user id from the backend server only if there is no specified user-id
     */
    public async request_identity() {
        if (has_local("identification") && get_local("identification") != "undefined") {
            console.info(`[user] Present user-id, skipping request identity`, get_local("identification"))
            return;
        }

        // Identification not specified, request a new one
        const response = await fetch_backend("/user", jsonform("POST"));    


        console.log(response)

        if (response.status != 200) {
            console.error("Failed to request identity", response.data)
            return;
        }

        set_local("identification", response.data.id)
    }

    public async get_events() {
        const response = await fetch_backend("/events", authform("GET"))
        console.log(response)
    }
}

