module.exports = {
  ci: {
    collect: {
      staticDistDir: "docs/example/dist",
      settings: {
        skipAudits: ["redirects-http"],
      },
    },
    upload: {
      target: "temporary-public-storage",
    },
  },
};
