# Push to GitHub - Step by Step

## ⚠️ Important: GitHub Authentication

GitHub **no longer accepts passwords** for HTTPS authentication. You need a **Personal Access Token (PAT)**.

---

## Step 1: Create Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Fill in:
   - **Note**: "Armor Assignment Push"
   - **Expiration**: Choose 90 days or custom
   - **Select scopes**: Check ✅ **`repo`** (full control of private repositories)
4. Click **"Generate token"**
5. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## Step 2: Create Repository on GitHub

1. Go to: https://github.com/new
2. Fill in:
   - **Repository name**: `Armor-Assingment`
   - **Description**: "FastAPI Banking MCP Server - Assignment"
   - **Visibility**: Public or Private (your choice)
   - **⚠️ DO NOT** check "Add a README file" (we already have one)
   - **⚠️ DO NOT** check "Add .gitignore" (we already have one)
   - **⚠️ DO NOT** check "Choose a license"
3. Click **"Create repository"**

---

## Step 3: Push Your Code

After creating the repository, run these commands:

```powershell
# The remote is already added, so just push:
git push -u origin main
```

When prompted:
- **Username**: `anchaljethliya`
- **Password**: Paste your **Personal Access Token** (not your GitHub password!)

---

## Alternative: Use GitHub CLI (Easier)

If you have GitHub CLI installed:

```powershell
# Install GitHub CLI (if not installed)
winget install --id GitHub.cli

# Authenticate
gh auth login

# Create repo and push in one command
gh repo create Armor-Assingment --public --source=. --remote=origin --push
```

---

## Quick Commands

```powershell
# Check if remote is set
git remote -v

# Push to GitHub
git push -u origin main

# If you need to update the remote URL
git remote set-url origin https://github.com/anchaljethliya/Armor-Assingment.git
```

---

## After Successful Push

Your repository will be available at:
**https://github.com/anchaljethliya/Armor-Assingment**

You can:
- View your code online
- Share the repository URL
- Use it for deployment to cloud platforms
- Continue development with version control

---

## Troubleshooting

### "Repository not found"
- Make sure you created the repository on GitHub first
- Check the repository name matches exactly: `Armor-Assingment`

### "Authentication failed"
- Use Personal Access Token, not password
- Make sure token has `repo` scope
- Token might have expired - generate a new one

### "Permission denied"
- Check your GitHub username is correct: `anchaljethliya`
- Verify the token has the right permissions

