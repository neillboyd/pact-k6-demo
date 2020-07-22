import { check, group, sleep } from "k6";
import http from "k6/http";

let API_HOST = `${__ENV.API_HOST}`;
let API_PORT = `${__ENV.API_PORT}`;

export let options = {
    vus: 10,
    iterations: 2000
};

// Scenarios
export default function() {

    group ("single_api_call", function() {
        let res = http.get("http://" + API_HOST + ":" + API_PORT + "/users/K6User");
        check(res, {
        "is status 200": (r) => r.status === 200,
        "response time is < 100ms": (r) => r.timings.duration < 100
        });
    });
}