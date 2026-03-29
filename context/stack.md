# MonkeyDo Tech Stack (AWS-Native)

## Frontend
- **Framework:** Next.js (React)
- **Deployment:** **AWS Amplify Hosting**. 
    - *Why:* It's the AWS version of Vercel. It connects to your GitHub, builds
    your Next.js app, and hosts it on a global CDN automatically.

## Backend
- **Framework:** FastAPI (Python 3.12+)
- **Deployment:** **AWS App Runner**.
    - *Why:* It's the simplest way to run a container. It handles the Load
    Balancer and "Auto-scaling" out of the box. You don't have to manage
    servers.

## Database
- **Engine:** PostgreSQL 16
- **Provider:** **AWS RDS**.
    - *Why:* Reliable, managed backups, and fits in the Free Tier for 12
    months.

## Infrastructure
- **Storage:** AWS S3 (For storing processed audio/transcripts later).
- **Domain/SSL:** Managed automatically by Amplify and App Runner.
