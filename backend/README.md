# AI Salary Prediction API

## Render settings
- Root Directory: `backend` (if this folder is inside the repository)
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

## Environment variable
After deploying the frontend, set `NETLIFY_URL` in Render to your Netlify
site origin, for example `https://your-site.netlify.app`.
For a temporary first deployment, the app currently allows all origins
when `NETLIFY_URL` is not set. Restrict it to your actual Netlify URL
before sharing the production site.

## API routes
- `GET /` - API status
- `GET /health` - health check
- `GET /options` - dropdown values
- `POST /predict` - salary prediction

Example JSON for `POST /predict`:
{
  "age": 25,
  "gender": "Male",
  "education": "Bachelor's",
  "job": "Data Analyst",
  "experience": 2
}

The saved model was serialized with scikit-learn 1.9.0, so the dependency
is pinned to that version to avoid the version mismatch seen when loading
it with a different scikit-learn release.
