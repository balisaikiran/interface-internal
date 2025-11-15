import DataLoader from "dataloader";
import { GetSecretValueCommand, SecretsManagerClient } from "@aws-sdk/client-secrets-manager";

const client = new SecretsManagerClient({ region: process.env.REGION});
const env = process.env.env;
const secretsNamespace = process.env.SECRETS_NAMESPACE;

async function get_secret(secretId: string) {
    var secret: String = "";
    try {
        const response = await client.send(new GetSecretValueCommand({ SecretId: secretId }));
        secret = response.SecretString
    } catch (error) {
        console.log(error);
        if (error.code === 'ResourceNotFoundException')
            console.log(`The requested secret ${secretId} was not found`);
        else if (error.code === 'InvalidRequestException')
            console.log(`The request was invalid due to: ${error.message}`);
        else if (error.code === 'InvalidParameterException')
            console.log(`The request had invalid params: ${error.message}`);
        secret = "";
    }
    return secret;
}

async function getbatchsecrests(keys: readonly unknown[]) {
    const secrets = await Promise.all(keys.map(async (key) => {
        const secret_name = key as string;
        const secretId = secretsNamespace + secret_name;
        console.log(secretId);
        const secret: String = await get_secret(secretId);
        return secret;
    }));
    return secrets;
}

export const keys = new DataLoader(keys => getbatchsecrests(keys));
