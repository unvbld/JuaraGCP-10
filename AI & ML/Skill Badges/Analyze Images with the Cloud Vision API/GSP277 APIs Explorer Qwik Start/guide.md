# APIs Explorer: Qwik Start

copy this command on cloudshell

```bash
gcloud config set project $DEVSHELL_PROJECT_ID
gsutil mb gs://$DEVSHELL_PROJECT_ID-bucket
gsutil bucketpolicyonly set off gs://$DEVSHELL_PROJECT_ID-bucket
gsutil iam ch allUsers:objectViewer gs://$DEVSHELL_PROJECT_ID-bucket


wget "https://raw.githubusercontent.com/unvbld/JuaraGCP-10/main/AI%20&%20ML/Skill%20Badges/Analyze%20Images%20with%20the%20Cloud%20Vision%20API/GSP277%20APIs%20Explorer%20Qwik%20Start/demo-image.jpg"


gsutil cp demo-image.jpg  gs://$DEVSHELL_PROJECT_ID-bucket

gsutil acl ch -u allUsers:R gs://$DEVSHELL_PROJECT_ID-bucket/demo-image.jpg
```