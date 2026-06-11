#!/usr/bin/env node
// Spawns the Python FastMCP server via stdio
const { spawn } = require("child_process");
const path = require("path");

const serverPath = path.join(__dirname, "..", "server.py");
const child = spawn("python", [serverPath, ...process.argv.slice(2)], {
  stdio: "inherit",
  env: process.env,
});

child.on("exit", (code) => process.exit(code ?? 0));
