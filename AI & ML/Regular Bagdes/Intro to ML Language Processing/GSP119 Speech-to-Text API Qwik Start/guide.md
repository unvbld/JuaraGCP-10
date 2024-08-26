#  Speech-to-Text API Qwik Start #

## Task 1. Create an API key ##

go to APIs & Services > Credentials

![img](asset/api.png)

after creating API key, go to Compute Engine and open SSH connection.

![img](asset/openSSH.png)

wait till SSH connection is established

![img](asset/SSH.png)

In the command line, enter in the following, replacing <YOUR_API_KEY>
```bash
export API_KEY=<YOUR_API_KEY>
```



## Task 2. Create your Speech-to-Text API request ##

copy this command in the SSH cli:

```bash
touch request.json
```
```bash
nano request.json
```
add this command to request.json

```bash
{
  "config": {
      "encoding":"FLAC",
      "languageCode": "en-US"
  },
  "audio": {
      "uri":"gs://cloud-samples-tests/speech/brooklyn.flac"
  }
}
```
Press control + x and then y to save and click Enter

## Task 3. Call the Speech-to-Text API ##

copy this command in the SSH cli again

```bash
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json \
"https://speech.googleapis.com/v1/speech:recognize?key=${API_KEY}"
```
```bash
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json \
"https://speech.googleapis.com/v1/speech:recognize?key=${API_KEY}" > result.json
```





