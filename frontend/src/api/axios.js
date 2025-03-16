import axios from "axios";
import { BACKEND_ADDRESS } from "../config";

export default axios.create({
    baseURL: BACKEND_ADDRESS,
    headers: {
        "Content-Type": "application/json",
    },
});
