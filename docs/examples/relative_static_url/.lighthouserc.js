module.exports = {
  ci: {
    collect: {
      staticDistDir: "docs/examples/relative_static_url/example/output",
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
