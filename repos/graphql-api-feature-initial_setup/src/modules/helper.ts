export const status_mapping = {
    "SUCCESS": [{"from": 200, "to": 299}],
    // Retry 429 code precendence over failed
    "RETRY": [{"from": 500, "to": 599}, {"equal": 429}],
    // Trying not to include 429 in failed, as it is a retryable error
    "FAILED": [{"from": 300, "to": 428}, {"from": 430, "to": 499}],
}

export function getstatusstring(status_mapping: Record<string, any>){
    const getstatus = (status: number) => {
        for (const [key, value] of Object.entries(status_mapping)) {
            for (const range of value) {
                if ("from" in range && "to" in range) {
                    if (status >= range["from"] && status <= range["to"]) {
                        return key;
                    }
                }
                else if ("equal" in range) {
                    if (status == range["equal"]) {
                        return key;
                    }
                }
            }
        }
        return "FAILED";
    }
    return getstatus
}