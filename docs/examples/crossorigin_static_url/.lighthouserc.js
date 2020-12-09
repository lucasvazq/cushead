module.exports = {
  ci: {
    collect: {
      url: ["http://localhost:3000/"],
      startServerCommand: "node docs/examples/crossorigin_static_url/app.js",
      settings: {
        skipAudits: ["redirects-http"],
      },
    },
    assert: {
      preset: "lighthouse:all",
      assertions: {
        "long-tasks": "off",
        "redirects-http": "off",
      },
    },
    upload: {
      target: "temporary-public-storage",
    },
  },
};
