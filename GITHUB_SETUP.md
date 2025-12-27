# GitHub Setup Guide

## ✅ Local Git Repository Ready!

Your code has been committed locally. Now let's push it to GitHub.

---

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in the details:
   - **Repository name**: `Armor-Assingment` (or any name you prefer)
   - **Description**: "FastAPI Banking MCP Server - Assignment"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

---

## Step 2: Copy the Repository URL

After creating the repository, GitHub will show you a page with commands. You'll see a URL like:

- **HTTPS**: `https://github.com/yourusername/Armor-Assingment.git`
- **SSH**: `git@github.com:yourusername/Armor-Assingment.git`

Copy the HTTPS URL.

---

## Step 3: Add Remote and Push

Run these commands in PowerShell (replace `YOUR_USERNAME` and `REPO_NAME` with your actual values):

```powershell
# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Example:**
```powershell
git remote add origin https://github.com/anchal/Armor-Assingment.git
git branch -M main
git push -u origin main
```

---

## Step 4: Authenticate

When you push, GitHub will ask for authentication:

- **If using HTTPS**: You'll need a Personal Access Token (not your password)
  - Go to: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  - Generate new token with `repo` permissions
  - Use this token as your password when pushing

- **If using SSH**: Make sure your SSH key is set up in GitHub

---

## Alternative: Using GitHub Desktop

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Sign in with your GitHub account
3. File → Add Local Repository
4. Select: `C:\Users\ancha\OneDrive\Desktop\Armor-Assingment`
5. Click "Publish repository" button

---

## Quick Commands Reference

```powershell
# Check current status
git status

# View remote repositories
git remote -v

# Push changes (after first push)
git push

# Pull latest changes
git pull

# View commit history
git log --oneline
```

---

## Troubleshooting

### "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### "Authentication failed"
- Make sure you're using a Personal Access Token, not your password
- Or set up SSH keys

### "Branch 'main' does not exist"
```powershell
git branch -M main
```

---

## ✅ Success!

Once pushed, your repository will be available at:
`https://github.com/YOUR_USERNAME/REPO_NAME`

You can share this URL or use it for deployment!

