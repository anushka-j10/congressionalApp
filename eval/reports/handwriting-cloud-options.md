# Dedicated handwriting OCR options — listed only, not configured

Checked October 21, 2026. These services advertise handwriting recognition;
none has been measured on this project's six intended handwriting photos.
No accounts, cloud resources, SDK integrations, or service credentials were
created. Approval is required before setting any of them up.

| Option | Published cost evidence | What leaves our server / privacy | Setup estimate |
| --- | --- | --- | --- |
| AWS Textract DetectDocumentText | AWS's US West (Oregon) example lists $0.0015/page for the first million pages, or $1.50/1,000; higher-volume rates differ. | Document image goes to AWS; synchronous byte-array input can avoid our own S3 bucket. AWS says it may store/use content to improve services unless the appropriate AWS Organizations opt-out policy is applied. | About 45–90 minutes with an already usable AWS account, billing, IAM permissions, and chosen region. |
| Google Document AI Enterprise Document OCR | The published standard tier lists $1.50/1,000 pages after the first 1,000 and through five million; the first 1,000 are listed free, with separate higher-volume/commitment tiers and OCR add-ons. | Document goes to Google Cloud. Google says content is used only to provide Document AI and not to train its models; batch documents can persist temporarily with a one-day failsafe TTL. | About 45–90 minutes with an existing billed project, API access, credentials, processor, and selected location. |
| Azure Document Intelligence Read | Public pricing lists 500 free pages/month. Paid Read pricing is region/tier dependent; the retrieved pricing page did not return its numeric paid quote, so it must be checked in Azure's calculator before selecting it. | Document goes to the Azure resource's region. Microsoft documents encrypted temporary storage of inputs/results for 24 hours, with an API available to delete results earlier. | About 30–60 minutes with an existing subscription, approved resource, region, endpoint, and authentication. |

Setup times are engineering estimates, not provider commitments, and exclude
account verification, billing approval, quota increases, and native-speaker or
handwriting accuracy evaluation. Prices exclude unrelated storage/network costs
and do not imply any free-tier eligibility for this account.

Before considering a switch, measure exactly the same images and ground truths.
Provider confidence, language lists, and handwriting claims cannot substitute
for measured key-token recall; privacy/retention must be reflected in the UI.

## Primary sources

- AWS handwriting/languages and byte-array support: [Textract FAQ](https://aws.amazon.com/textract/faqs/).
- AWS cost example: [Textract pricing](https://aws.amazon.com/textract/pricing/).
- Google product capabilities and version-specific handwriting styling: [Enterprise Document OCR](https://docs.cloud.google.com/document-ai/docs/enterprise-document-ocr).
- Google cost: [Document AI pricing](https://cloud.google.com/products/document-ai/pricing).
- Google training/retention commitments: [Document AI security](https://docs.cloud.google.com/document-ai/docs/security).
- Azure handwriting capability: [Document Intelligence Read](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/read?view=doc-intel-4.0.0).
- Azure cost: [Document Intelligence pricing](https://azure.microsoft.com/en-us/pricing/details/document-intelligence/).
- Azure retention: [Data privacy and security](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/document-intelligence/data-privacy-security).

This file is a comparison of dedicated cloud OCR options with sourced costs,
privacy details, and explicitly estimated setup time. It authorizes no setup and
does not claim that any option has passed this project's handwriting tests.
