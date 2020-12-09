const express = require("express");

const app_3000 = express();
const app_3001 = express();
const serveStatic = require("serve-static");

app_3000.use("/", serveStatic("docs/examples/crossorigin_static_url/example/output/"));
app_3000.listen(3000);

app_3001.use("/", serveStatic("docs/examples/crossorigin_static_url/example/output/"));
app_3001.listen(3001);
