# ESPN-FFL

gcloud functions deploy TenderKnob-FFL --trigger-http --gen1 --region=us-central1 --runtime=python310 --entry-point=main --timeout=120s --memory=128Mi --no-allow-unauthenticated