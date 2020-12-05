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
    },
    upload: {
      target: "temporary-public-storage",
    },
  },
};
