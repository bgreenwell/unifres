# GitHub Pages Setup Guide

## Quick Setup (5 minutes)

Your repository is now live at: https://github.com/bgreenwell/unifres

Follow these steps to enable the documentation website:

### 1. Enable GitHub Pages

1. Go to: https://github.com/bgreenwell/unifres/settings/pages
2. Under **Source**, select: **GitHub Actions**
3. Click **Save**

That's it! The `quarto-publish.yml` workflow will automatically deploy your site.

### 2. Wait for Workflows to Complete

The following workflows should run automatically:

- ✅ **R-CMD-check** - Tests R package on multiple platforms
- ✅ **Python Tests** - Tests Python package
- ✅ **Test Coverage** - Generates coverage reports
- ✅ **Quarto Publish** - Builds and deploys website

Check progress at: https://github.com/bgreenwell/unifres/actions

### 3. Access Your Website

Once the Quarto workflow completes, your site will be live at:

**https://bgreenwell.github.io/unifres/**

---

## Optional: Add Codecov (for coverage badges)

### Step 1: Sign up for Codecov

1. Go to https://codecov.io/
2. Sign in with GitHub
3. Add the `bgreenwell/unifres` repository

### Step 2: Add Secret to GitHub

1. Go to: https://github.com/bgreenwell/unifres/settings/secrets/actions
2. Click **New repository secret**
3. Name: `CODECOV_TOKEN`
4. Value: (copy from Codecov dashboard)
5. Click **Add secret**

### Step 3: Verify Coverage Reporting

After the next push, coverage reports will be uploaded to Codecov and badges will work!

---

## Verify Everything Works

### Check Website Build

1. Go to: https://github.com/bgreenwell/unifres/actions
2. Look for "Quarto Publish" workflow
3. Verify it completes successfully
4. Visit https://bgreenwell.github.io/unifres/

### Check R Package

1. Look for "R-CMD-check" workflow
2. Should pass on Ubuntu, macOS, and Windows
3. Green checkmark ✅ means success

### Check Python Package

1. Look for "Python Tests" workflow
2. Should pass on Python 3.8-3.12
3. Green checkmark ✅ means success

### Check Code Coverage

1. Look for "R Test Coverage" workflow
2. Should upload coverage to Codecov
3. Coverage badge will update in README

---

## Troubleshooting

### Website not building?

- Check workflow logs: https://github.com/bgreenwell/unifres/actions
- Ensure GitHub Pages is enabled in Settings → Pages
- Verify `quarto-publish.yml` workflow file is present

### Badges not showing?

- Give it a few minutes after first workflow run
- Check that workflows have completed successfully
- For Codecov badge, ensure CODECOV_TOKEN is set

### R CMD check failing?

- Check the workflow logs for specific errors
- Most common: missing suggested packages
- Fix by updating DESCRIPTION file

### Python tests failing?

- Check the workflow logs
- Verify all dependencies are in pyproject.toml
- Ensure tests run locally first

---

## Next Steps

Once everything is running:

1. ✅ Website is live at https://bgreenwell.github.io/unifres/
2. ✅ CI/CD runs on every push
3. ✅ Code coverage tracked
4. ✅ README badges show status

You're all set! 🎊

---

## Need Help?

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Quarto Publishing**: https://quarto.org/docs/publishing/github-pages.html
- **Codecov Setup**: https://docs.codecov.com/docs/quick-start

---

*This guide was generated for the unifres v0.1.0 release.*
