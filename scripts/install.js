#!/usr/bin/env node
// Post-install: ensures Python dependencies are installed
const { execSync } = require("child_process");
const path = require("path");

const req = path.join(__dirname, "..", "requirements.txt");
console.log("Installing Python dependencies for pbi-mcp-server...");
try {
  execSync(`pip install -r "${req}"`, { stdio: "inherit" });
  console.log("Python dependencies installed successfully.");
} catch (e) {
  console.warn("pip install failed. Run manually: pip install -r requirements.txt");
}
