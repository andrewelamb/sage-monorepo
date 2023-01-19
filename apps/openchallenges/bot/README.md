# Challenge Bot

This GitHub App automates tasks in this repository.

## Preparation

```console
nx prepare challenge-bot
```

## Deploying locally

TODO

## Deploying to AWS

1. Create an IAM user named `challenge-bot` (deployment user).
    - Store the access key ID and secret access key in a secure place.

2. Assign [this policy](docs/challenge-bot-dev-us-east-1-policy.json) to the deployment user.
    - Replace the string `ACCOUNT` by your AWS account ID (e.g. `123456789012`).
    - This policy has been generated with the [Serverless policy generator], which has then been
      manually updated to successfully deploy the app.

3. Configure your AWS profile with the credentials you received by running this command in your
   terminal. This [guide] provides alternate methods to use AWS credentials.

    ```console
    serverless config credentials \
      --provider aws \
      --key <access key ID> \
      --secret <secret access key>
    ```

4. In your AWS parameter store, create and store values for the environment variables used in
   `serverless.yml` that are prefixed with `ssm:/` (see [Configuration](#configuration)).

5. Login with Serverless.

    ```console
    serverless login
    ```

6. Deploy the app.

    ```console
      nx deploy challenge-bot
    ```

## Configuration

TODO

<!-- ## Setup

## Docker

```sh
# 1. Build container
docker build -t challengebot .

# 2. Start container
docker run -e APP_ID=<app-id> -e PRIVATE_KEY=<pem-value> challengebot
```
 -->

## Testing locally

Send a request to an HTTP route:

```console
curl -i -X GET http://localhost:3000/api/hello-world

HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: application/json; charset=utf-8
Content-Length: 7
ETag: W/"7-n4nHQM60bXQYySSnisV5QdXpZSA"
Date: Sat, 22 Oct 2022 14:02:30 GMT
Connection: keep-alive
Keep-Alive: timeout=5

{"a":1}
```

## Notes

- https://github.com/probot/probot/discussions/1608
  - Discussion about how to start Probot app with Server.

## Contributing

If you have suggestions for how challengebot could be improved, or want to report a bug, open an
issue! We'd love all and any contributions.

For more, check out the [Contributing Guide](../../.github/CONTRIBUTING.md).

## License

[ISC](LICENSE.md) © 2022 Thomas Schaffter

<!-- Links -->

[Serverless policy generator]: https://github.com/dancrumb/generator-serverless-policy
[guide]: https://www.serverless.com/framework/docs/providers/aws/guide/credentials/