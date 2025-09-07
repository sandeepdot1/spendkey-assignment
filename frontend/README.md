# E-Commerce Frontend (React)

This is the React frontend for the e-commerce backend running at `http://localhost:5000`.

## Requirements

- Node.js (16.x or 18.x recommended)
- npm (comes with Node) or yarn (optional)

### Install Node (recommended approach: nvm)

#### macOS / Linux
```bash
# Install nvm (if not installed)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
# restart shell or:
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install Node LTS
nvm install 18
nvm use 18
node -v
npm -v
```

#### Run app
```bash
npm install
npm start
```
