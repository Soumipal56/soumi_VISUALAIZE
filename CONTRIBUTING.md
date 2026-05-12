# Contributing to VisualAIze Pro

Thank you for your interest in contributing to **VisualAIze Pro**! 🎉

This project is participating in **[GirlScript Summer of Code (GSSOC)](https://gssoc.girlscript.tech/)** and we warmly welcome contributions from the community. Whether you're fixing a bug, suggesting a feature, improving documentation, or helping with design – every contribution matters!

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Fork & Clone](#fork--clone)
  - [Local Setup](#local-setup)
- [Making Changes](#making-changes)
  - [Branching Strategy](#branching-strategy)
  - [Commit Messages](#commit-messages)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Issue Guidelines](#issue-guidelines)
- [GSSOC Contributors](#gssoc-contributors)

---

## Code of Conduct

Please read our [Code of Conduct](./CODE_OF_CONDUCT.md) before contributing. All participants are expected to uphold it.

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

| Tool | Version |
|------|---------|
| [Node.js](https://nodejs.org/) | v18 or above |
| [Python](https://www.python.org/) | v3.10 or above |
| [Git](https://git-scm.com/) | Latest |
| [Docker](https://www.docker.com/) *(optional)* | Latest |

You will also need a **Google Gemini API Key**. Get one for free at [Google AI Studio](https://aistudio.google.com/app/apikey).

---

### Fork & Clone

1. **Fork** this repository by clicking the **Fork** button at the top right of the repository page on GitHub.

2. **Clone** your fork to your local machine:

   ```bash
   git clone https://github.com/<your-username>/VISUALAIZE.git
   cd VISUALAIZE
   ```

3. Add the original repository as an **upstream** remote so you can keep your fork up to date:

   ```bash
   git remote add upstream https://github.com/priyanshu5ingh/VISUALAIZE.git
   ```

---

### Local Setup

The project has two parts: a **Next.js frontend** and a **Python (FastAPI) backend**.

#### Backend Setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create your environment file
cp .env.example .env
# Open .env and add your GEMINI_API_KEY
```

Start the backend server:

```bash
uvicorn main:app --reload --port 8000
```

#### Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Create your environment file
cp .env.example .env.local
# Open .env.local and add NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the frontend dev server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser. 🚀

#### Docker (Alternative)

If you prefer Docker, run everything with a single command:

```bash
docker-compose up --build
```

---

## Making Changes

### Branching Strategy

Always create a new branch from the latest `master` before making changes. **Direct pushes to `master` are strictly forbidden.**

1. **Fork** the repository.
2. **Clone** your fork.
3. **Create a branch** using the following naming convention:
   - `feat/issue-#` (for new features)
   - `fix/issue-#` (for bug fixes)
   - `docs/issue-#` (for documentation)

```bash
# Example
git checkout -b feat/issue-42
```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
feat: add PNG export for diagrams
fix: resolve canvas pan on mobile devices
docs: update README with Docker instructions
```

---

## Submitting a Pull Request

1. Push your branch to your fork:

   ```bash
   git push origin feat/your-feature-name
   ```

2. Go to your fork on GitHub and click **"Compare & pull request"**.

3. Fill in the **Pull Request template** completely:
   - Describe what you changed and why.
   - Link the related issue (e.g., `Closes #42`).
   - Confirm you have tested your changes locally.

4. Wait for a maintainer to review your PR. Be ready to address feedback and make changes.

5. Once approved, your PR will be merged! 🎉

---

## Issue Guidelines

- **Search existing issues** before opening a new one to avoid duplicates.
- Use the provided **issue templates** (Bug Report / Feature Request).
- Be clear and descriptive. Include screenshots or screen recordings where helpful.
- Add relevant labels (e.g., `bug`, `enhancement`, `good first issue`, `gssoc`).

---

## GSSOC Contributors

This project is part of **GirlScript Summer of Code (GSSOC)**. If you are a GSSOC participant:

- Look for issues labeled **`gssoc`** and **`good first issue`** for beginner-friendly tasks.
- Comment on the issue you want to work on and wait for it to be assigned to you before starting.
- Mention **"GSSOC"** in your PR description so your contribution gets properly tracked.
- Join the discussion in the comments if you have any questions — maintainers are here to help!

> **First time contributing to open source?** Check out [this guide](https://opensource.guide/how-to-contribute/) to get started!

---

We are thrilled to have you on board. Happy coding! 💻✨
