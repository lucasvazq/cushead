module.exports = {
  ci: {
    collect: {
      staticDistDir: "docs/example/dist",
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
